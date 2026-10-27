#!/usr/bin/env python3
"""Build the Batch 01 lecture from the selected narration clips.

The slides, exact text-to-speech inputs, and cached audio-aligned caption timings
are stored in notes/. A separate automatic recognition pass checked the audio;
there has been no human verbatim review, and model timings can still be off.
This build reuses the user's selected voice clips and never calls a speech service.
All examples are hypothetical. See Batch-01-Guide.md for legal scope and sources.

Setup: python3 -m pip install Pillow imageio-ffmpeg markdown
       python3 build_batch_01.py --audit
       python3 build_batch_01.py --preview
       python3 build_batch_01.py --build
Use FFMPEG_BIN to select an ffmpeg with libx264, AAC, libmp3lame and libass, or install
imageio-ffmpeg. Temporary frames and PCM are kept in a temporary directory.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / 'notes' / 'lesson-data.json'
ALIGNMENT = HERE / 'notes' / 'caption-alignment.json'
ASSETS = HERE / 'assets'
W, H = 1920, 1080
BG = '#070d1b'
SURFACE = '#101b30'
INK = '#f2f6ff'
MUTED = '#a5b6cb'
BLUE = '#34c6ff'
TEAL = '#22d6ac'
PURPLE = '#bc78ff'
GOLD = '#ffcc4a'
PALETTE = [BLUE, GOLD, TEAL, PURPLE]


def ffmpeg_path() -> str:
    if os.environ.get('FFMPEG_BIN'):
        return os.environ['FFMPEG_BIN']
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        found = shutil.which('ffmpeg')
        if found:
            return found
        raise SystemExit('Install imageio-ffmpeg or set FFMPEG_BIN to an ffmpeg with libass.')


def load_data() -> dict:
    return json.loads(DATA.read_text(encoding='utf-8'))


def audit(data: dict) -> None:
    errors: list[str] = []
    chapters = data.get('sections', [])
    if not chapters:
        errors.append('At least one narration section is required')
    audio_names: set[str] = set()
    for n, section in enumerate(chapters, 1):
        audio = section.get('audio', '')
        if not (HERE / 'audio' / audio).is_file():
            errors.append(f'Section {n}: missing audio {audio!r}')
        if audio in audio_names:
            errors.append(f'Section {n}: duplicate audio {audio!r}')
        audio_names.add(audio)
        if not section.get('source'):
            errors.append(f'Section {n}: no source identifier')
        if len(section.get('beats', [])) != 2:
            errors.append(f'Section {n}: expected two beats')
        for b, beat in enumerate(section.get('beats', []), 1):
            for field in ['heading', 'rule', 'example', 'trap', 'key', 'lines']:
                if not beat.get(field):
                    errors.append(f'Section {n}, beat {b}: missing {field}')
            if len(beat.get('cards', [])) != 4:
                errors.append(f'Section {n}, beat {b}: expected four cards')
            if any(len(card) != 2 for card in beat.get('cards', [])):
                errors.append(f'Section {n}, beat {b}: each card needs a label and note')
    for required in ['NotoSans.ttf', 'NotoSansDevanagari.ttf']:
        if not (ASSETS / required).is_file() or (ASSETS / required).stat().st_size < 100:
            errors.append(f'Missing font: {required}')
    for required in ['OFL-NotoSans.txt', 'OFL-NotoSansDevanagari.txt']:
        if not (HERE / 'licenses' / required).is_file():
            errors.append(f'Missing font licence: {required}')
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f'Audit OK: {len(chapters)} sections; {sum(len(s["beats"]) for s in chapters)} illustrated beats; '
          f'each beat has an example, a caution and a source-bearing section.')
    print('Examples are hypothetical; further topics remain explicitly pending.')


def font(size: int, bold: bool = False):
    from PIL import ImageFont
    f = ImageFont.truetype(str(ASSETS / 'NotoSans.ttf'), size)
    if bold:
        f.set_variation_by_name('Bold')
    return f


def wrapped(draw, text: str, f, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ''
    for word in words:
        proposal = (current + ' ' + word).strip()
        if current and draw.textlength(proposal, font=f) > max_width:
            lines.append(current)
            current = word
        else:
            current = proposal
    if current:
        lines.append(current)
    return lines


def fit_lines(draw, text: str, max_width: int, max_lines: int, start: int, minimum: int, bold=False):
    for size in range(start, minimum - 1, -1):
        f = font(size, bold)
        lines = wrapped(draw, text, f, max_width)
        if len(lines) <= max_lines and all(draw.textlength(line, font=f) <= max_width for line in lines):
            return f, lines
    raise ValueError(f'Text does not fit a slide: {text!r}')


def text_lines(draw, xy: tuple[int, int], lines: list[str], f, color: str, line_height: int) -> None:
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=f, fill=color)
        y += line_height


def slide(section: dict, beat: dict, chapter_num: int, beat_num: int, dest: Path,
          total_chapters: int) -> None:
    from PIL import Image, ImageDraw
    im = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(im)
    # Shell and top metadata mirror the provided lecture-player reference.
    d.rectangle((0, 0, W, 68), fill='#0a1325')
    d.line((0, 67, W, 67), fill='#293a60', width=2)
    d.rounded_rectangle((44, 16, 206, 52), radius=14, fill='#21163d', outline=PURPLE, width=2)
    d.text((62, 19), 'BATCH 01', font=font(23, True), fill=PURPLE)
    d.text((230, 18), 'TRAVELLING ALLOWANCE  /  CIVILIAN', font=font(23, True), fill='#d9e6f9')
    d.rounded_rectangle((1400, 16, 1728, 52), radius=14, fill='#0b2530', outline='#139b9a', width=2)
    d.text((1418, 20), 'CITY HINGLISH VOICE', font=font(20, True), fill='#70e5cf')
    d.text((1754, 19), f'{chapter_num:02d} / {total_chapters:02d}', font=font(22, True), fill='#c0d0e5')
    d.text((45, 91), beat['heading'], font=font(25, True), fill=PURPLE)
    title_f, title_lines = fit_lines(d, section['title'], 1750, 1, 46, 38, True)
    text_lines(d, (45, 127), title_lines, title_f, INK, 52)
    # Four overview cards.
    x0, gap, top = 45, 18, 210
    card_width = (W - 2 * x0 - 3 * gap) // 4
    for idx, (label, note) in enumerate(beat['cards']):
        x = x0 + idx * (card_width + gap)
        col = PALETTE[idx]
        d.rounded_rectangle((x, top, x + card_width, top + 130), radius=20,
                            fill=SURFACE, outline=col, width=2)
        f1, l1 = fit_lines(d, label, card_width - 42, 1, 29, 21, True)
        f2, l2 = fit_lines(d, note, card_width - 42, 2, 25, 19)
        text_lines(d, (x + 21, top + 23), l1, f1, col, 30)
        text_lines(d, (x + 21, top + 62), l2, f2, '#d7e2f2', 30)
    # Explanation and application strips. Every frame has an explicit example.
    for idx, (label, field, color) in enumerate([
        ('RULE', 'rule', BLUE), ('EXAMPLE', 'example', TEAL), ('WATCH OUT', 'trap', PURPLE)
    ]):
        y = 364 + idx * 125
        d.rounded_rectangle((45, y, 1875, y + 108), radius=17,
                            fill=SURFACE, outline='#323354', width=2)
        d.rounded_rectangle((61, y + 18, 302, y + 90), radius=11,
                            fill='#172642', outline=color, width=2)
        lf = font(24, True)
        d.text((81, y + 35), label, font=lf, fill=color)
        body_font, lines = fit_lines(d, beat[field], 1505, 2, 31, 25)
        height = len(lines) * 38
        text_lines(d, (330, y + (108 - height) // 2 - 3), lines, body_font, INK, 38)
    d.rounded_rectangle((45, 747, 1875, 832), radius=18,
                        fill='#25200e', outline=GOLD, width=3)
    d.text((68, 772), 'KEY', font=font(24, True), fill=GOLD)
    key_font, key_lines = fit_lines(d, beat['key'], 1655, 2, 27, 22, True)
    text_lines(d, (153, 765 if len(key_lines) == 2 else 770), key_lines, key_font, '#fff0bf', 32)
    src = f'SOURCE: {section["source"]}   •   Illustrations are hypothetical'
    sf, sl = fit_lines(d, src, 1830, 1, 19, 15)
    text_lines(d, (49, 845), sl, sf, MUTED, 24)
    # Dark subtitle band matches the screenshot; libass renders speech later.
    d.rounded_rectangle((45, 882, 1875, 1056), radius=20,
                        fill='#030712', outline='#2d3956', width=2)
    d.text((66, 892), 'ENGLISH SUBTITLES  /  TRANSLATION • AUTOMATICALLY ALIGNED • NOT HUMAN-VERIFIED',
           font=font(18, True), fill='#7a8da8')
    progress = ((chapter_num - 1) * 2 + beat_num) / (total_chapters * 2)
    d.rounded_rectangle((47, 1064, 1873, 1074), radius=5, fill='#1b2940')
    d.rounded_rectangle((47, 1064, 47 + int(1826 * progress), 1074), radius=5, fill=TEAL)
    im.save(dest, optimize=True)


def audio_pcm(ff: str, path: Path) -> bytes:
    # Fixed-format PCM makes chapter lengths sample-accurate and avoids MP3
    # encoder-delay accumulation when chapters are joined.
    proc = subprocess.run([ff, '-v', 'error', '-i', str(path), '-f', 's16le',
                           '-acodec', 'pcm_s16le', '-ac', '1', '-ar', '24000', 'pipe:1'],
                          capture_output=True, check=True)
    if not proc.stdout:
        raise RuntimeError(f'No audio decoded from {path}')
    return proc.stdout


def stamp(seconds: float, sep: str = '.') -> str:
    ms = max(0, round(seconds * 1000))
    hours, ms = divmod(ms, 3_600_000)
    mins, ms = divmod(ms, 60_000)
    secs, ms = divmod(ms, 1000)
    return f'{hours:02d}:{mins:02d}:{secs:02d}{sep}{ms:03d}'


def ass_stamp(seconds: float) -> str:
    cs = max(0, round(seconds * 100))
    h, cs = divmod(cs, 360_000)
    m, cs = divmod(cs, 6_000)
    s, cs = divmod(cs, 100)
    return f'{h}:{m:02d}:{s:02d}.{cs:02d}'


def load_alignment() -> dict:
    if not ALIGNMENT.is_file():
        raise SystemExit(f'Missing audio alignment: {ALIGNMENT}')
    return json.loads(ALIGNMENT.read_text(encoding='utf-8'))


def build_timeline(data: dict, durations: list[float], alignment: dict):
    """Use recorded, audio-aligned cues; reject stale text, audio or timing data."""
    sections = data['sections']
    aligned = alignment.get('sections', [])
    if len(sections) != len(durations) or len(sections) != len(aligned):
        raise ValueError('Alignment, audio durations and chapter counts differ')
    timeline, captions = [], []
    elapsed = 0.0
    for si, (section, duration, entry) in enumerate(zip(sections, durations, aligned), 1):
        source = section_tts_text(section)
        script_hash = hashlib.sha256(source.encode('utf-8')).hexdigest()
        audio_hash = hashlib.sha256((HERE / 'audio' / section['audio']).read_bytes()).hexdigest()
        if entry.get('audio') != section['audio'] or entry.get('audio_sha256') != audio_hash:
            raise ValueError(f'Section {si}: audio changed since caption alignment')
        if entry.get('script_sha256') != script_hash:
            raise ValueError(f'Section {si}: narration text changed since caption alignment')
        if abs(entry.get('duration', -1) - duration) > 0.05:
            raise ValueError(f'Section {si}: decoded duration changed since caption alignment')
        split = entry.get('beat_boundary', -1)
        if not 0 < split < duration:
            raise ValueError(f'Section {si}: invalid beat boundary')
        cues = entry.get('cues', [])
        if not cues or ' '.join(c.get('text', '') for c in cues) != source:
            raise ValueError(f'Section {si}: caption text does not match the saved speech input')
        prev_end, prev_beat, seen_beats = 0.0, 1, set()
        for cue in cues:
            start, end, beat = cue['start'], cue['end'], cue['beat']
            if not (beat in (1, 2) and beat >= prev_beat and 0 <= start < end <= duration + 0.001
                    and start + 0.001 >= prev_end):
                raise ValueError(f'Section {si}: invalid or overlapping caption cue: {cue}')
            if (beat == 1 and end > split + 0.001) or (beat == 2 and start < split - 0.001):
                raise ValueError(f'Section {si}: caption crosses its slide boundary: {cue}')
            captions.append((elapsed + start, elapsed + end, cue['text']))
            prev_end, prev_beat = end, beat
            seen_beats.add(beat)
        if seen_beats != {1, 2}:
            raise ValueError(f'Section {si}: both slides must have captions')
        timeline.append((si, 1, elapsed, elapsed + split))
        timeline.append((si, 2, elapsed + split, elapsed + duration))
        elapsed += duration
    return timeline, captions, elapsed


def romanize_hinglish(text: str, dictionary: dict[str, str]) -> str:
    """Transliterate the exact synthesis input, retaining English words and punctuation."""
    def convert(match):
        word = match.group(0)
        if word not in dictionary:
            raise ValueError(f'No Roman transliteration recorded for {word!r}')
        return dictionary[word]

    text = re.sub(r'[\u0900-\u0963\u0965-\u097f]+', convert, text).replace('।', '.')
    if re.search(r'[\u0900-\u097f]', text):
        raise ValueError('Unexpected Devanagari in Roman subtitles')
    return text


def translated_captions(data: dict, alignment: dict) -> list[str]:
    """Pair each English translation with the audio-aligned cue that it translates."""
    translations = json.loads((HERE / 'notes' / 'english-subtitles.json').read_text(encoding='utf-8'))
    sources = json.loads((HERE / 'notes' / 'english-translation-source-sha256.json').read_text(encoding='utf-8'))
    if set(translations) != {s['audio'] for s in data['sections']} or set(sources) != set(translations):
        raise ValueError('English subtitle sections differ from the narration')
    result = []
    for section, aligned in zip(data['sections'], alignment['sections']):
        audio = section['audio']
        cue_hash = hashlib.sha256('\n'.join(cue['text'] for cue in aligned['cues']).encode('utf-8')).hexdigest()
        if sources[audio] != cue_hash:
            raise ValueError(f'{audio}: English translation was made for different source cues')
        lines = translations[audio]
        if len(lines) != len(aligned['cues']) or any(not line.strip() for line in lines):
            raise ValueError(f'{audio}: English translation cue count differs from alignment')
        if any(re.search(r'[\u0900-\u097f]', line) for line in lines):
            raise ValueError(f'{audio}: English subtitles must use Roman script')
        result.extend(lines)
    return result


def make_subtitles(captions, english: list[str], temp: Path, publish: bool = True) -> None:
    if len(captions) != len(english):
        raise ValueError('English subtitle count does not match aligned speech cues')
    dictionary = json.loads((HERE / 'notes' / 'roman-hindi.json').read_text(encoding='utf-8'))
    en_vtt = ['WEBVTT', '', 'NOTE English translation of the spoken Hinglish, not a verbatim transcript. Cue timing is automatically aligned and is not human-verified; it can still be wrong.', '']
    roman_vtt = ['WEBVTT', '', 'NOTE Roman-script Hinglish transliteration of the synthesis input, automatically audio-aligned and not human-verified as verbatim. It may differ from what the voice actually says.', '']
    ass = [
        '[Script Info]', 'ScriptType: v4.00+', 'PlayResX: 1920', 'PlayResY: 1080',
        'WrapStyle: 0', 'ScaledBorderAndShadow: yes', '', '[V4+ Styles]',
        'Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,Strikeout,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding',
        'Style: Default,Noto Sans,52,&H00FFFFFF,&H00FFFFFF,&H00100C05,&H9A000000,0,0,0,0,100,100,0,0,1,3,1,2,105,105,44,1',
        '', '[Events]', 'Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text'
    ]
    for i, ((start, end, source), translated) in enumerate(zip(captions, english), 1):
        roman = romanize_hinglish(source, dictionary)
        for dest, text, setting in ((en_vtt, translated, ''),
                                    (roman_vtt, roman, ' line:5% position:50% align:center')):
            lines = textwrap.wrap(text, width=62, break_long_words=False, break_on_hyphens=False)
            dest += [str(i), f'{stamp(start)} --> {stamp(end)}{setting}', '\n'.join(lines), '']
        clean = translated.replace('\\', '').replace('{', '(').replace('}', ')')
        ass.append(f'Dialogue: 0,{ass_stamp(start)},{ass_stamp(end)},Default,,0,0,0,,{clean}')
    for name, lines in (('Captions-en.vtt', en_vtt), ('Captions-roman.vtt', roman_vtt)):
        path = temp / name
        path.write_text('\n'.join(lines), encoding='utf-8')
        if publish:
            os.replace(path, HERE / name)
    (temp / 'captions.ass').write_text('\n'.join(ass) + '\n', encoding='utf-8')


def section_tts_text(section: dict) -> str:
    """Return the exact input used to synthesize this section's voice clip."""
    return ' '.join(line for beat in section['beats'] for line in beat['lines'])


def make_narration_script(data: dict) -> None:
    out = ['BATCH 01 — CITY HINGLISH NARRATION SCRIPT',
           'The text below is the input sent to the selected text-to-speech voice for each chapter.',
           'The audio was checked with automatic speech recognition, not human-reviewed for verbatim accuracy.',
           'Caption timing was aligned to the audio automatically and may still be slightly off.',
           'All examples are hypothetical. Consult Batch-01-Guide.md and cited orders for details.', '']
    for idx, section in enumerate(data['sections'], 1):
        out += [f'{idx:02d}. {section["title"]}', f'Sources: {section["source"]}',
                'TTS INPUT:', section_tts_text(section), '']
    (HERE / 'Narration-hi.txt').write_text('\n'.join(out), encoding='utf-8')


def ff_filter_path(path: Path) -> str:
    # Escape ffmpeg filter-special characters. Paths in the delivered project
    # do not contain colons or quotes, but the escaping also supports them.
    return str(path).replace('\\', '\\\\').replace(':', '\\:').replace("'", "\\'").replace(',', '\\,')


def make_build(data: dict, ff: str, preview_only=False):
    from PIL import Image  # dependency check with a clear install message
    del Image
    make_narration_script(data)
    with tempfile.TemporaryDirectory(prefix='ccs-ta-batch01-') as tmp:
        temp = Path(tmp)
        if preview_only:
            image = temp / 'preview.png'
            slide(data['sections'][3], data['sections'][3]['beats'][1], 4, 2, image, len(data['sections']))
            # A synthetic English caption checks subtitle placement in the preview.
            sample = 'Example: Level Seven can check economy entitlement on an official tour.'
            make_subtitles([(0, 5, sample)], [sample], temp, publish=False)
            dest = Path('/tmp/ccs-ta-batch01-preview.png')
            filt = f"ass=filename='{ff_filter_path(temp / 'captions.ass')}':fontsdir='{ff_filter_path(ASSETS)}'"
            subprocess.run([ff, '-hide_banner', '-loglevel', 'warning', '-y', '-i', str(image),
                            '-vf', filt, '-frames:v', '1', '-update', '1', str(dest)], check=True)
            print(f'Preview: {dest}')
            return
        durations: list[float] = []
        pcm_path = temp / 'narration.pcm'
        with pcm_path.open('wb') as all_audio:
            for idx, section in enumerate(data['sections'], 1):
                pcm = audio_pcm(ff, HERE / 'audio' / section['audio'])
                all_audio.write(pcm)
                durations.append(len(pcm) / (24000 * 2))
                print(f'Audio {idx:02d}: {durations[-1]:.2f}s', flush=True)
        alignment = load_alignment()
        timeline, captions, total = build_timeline(data, durations, alignment)
        english = translated_captions(data, alignment)
        # Stage sidecars until the new MP4 has finished encoding successfully.
        make_subtitles(captions, english, temp, publish=False)
        concat = temp / 'slides.txt'
        with concat.open('w', encoding='utf-8') as listing:
            for si, bi, start, end in timeline:
                frame = temp / f'slide-{si:02d}-{bi}.png'
                slide(data['sections'][si - 1], data['sections'][si - 1]['beats'][bi - 1],
                      si, bi, frame, len(data['sections']))
                listing.write(f"file '{frame.as_posix()}'\n")
                listing.write(f'duration {end - start:.6f}\n')
            # The concat demuxer needs the last frame repeated to honour its duration.
            listing.write(f"file '{frame.as_posix()}'\n")
        filt = f"fps=12,ass=filename='{ff_filter_path(temp / 'captions.ass')}':fontsdir='{ff_filter_path(ASSETS)}'"
        output = HERE / 'Batch-01-Lecture.mp4'
        # Keep a previously completed lecture playable until the new one is ready.
        rendering = HERE / '.Batch-01-Lecture-rendering.mp4'
        cmd = [ff, '-hide_banner', '-y', '-loglevel', 'warning',
               '-f', 'concat', '-safe', '0', '-i', str(concat),
               '-f', 's16le', '-ar', '24000', '-ac', '1', '-i', str(pcm_path),
               '-vf', filt, '-map', '0:v:0', '-map', '1:a:0', '-t', f'{total:.6f}',
               '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '23', '-pix_fmt', 'yuv420p',
               '-c:a', 'aac', '-b:a', '80k', '-movflags', '+faststart', str(rendering)]
        print(f'Rendering {total:.1f}s to {output.name} (12 fps, 1920x1080) ...', flush=True)
        try:
            subprocess.run(cmd, check=True)
            for name in ('Captions-en.vtt', 'Captions-roman.vtt'):
                os.replace(temp / name, HERE / name)
            os.replace(rendering, output)
        finally:
            rendering.unlink(missing_ok=True)
        print(f'Video ready: {output} ({output.stat().st_size / 1024 / 1024:.1f} MiB)', flush=True)
        audio_output = HERE / 'Batch-01-Audio.mp3'
        audio_rendering = HERE / '.Batch-01-Audio-rendering.mp3'
        audio_cmd = [ff, '-hide_banner', '-y', '-loglevel', 'warning',
                     '-f', 's16le', '-ar', '24000', '-ac', '1', '-i', str(pcm_path),
                     '-c:a', 'libmp3lame', '-b:a', '96k', str(audio_rendering)]
        try:
            subprocess.run(audio_cmd, check=True)
            os.replace(audio_rendering, audio_output)
        finally:
            audio_rendering.unlink(missing_ok=True)
        print(f'Audio ready: {audio_output} ({audio_output.stat().st_size / 1024 / 1024:.1f} MiB)', flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--audit', action='store_true')
    group.add_argument('--preview', action='store_true')
    group.add_argument('--build', action='store_true')
    args = parser.parse_args()
    data = load_data()
    audit(data)
    if args.preview or args.build:
        try:
            import PIL  # noqa: F401
        except ImportError:
            raise SystemExit('Install Pillow: python3 -m pip install Pillow imageio-ffmpeg')
        make_build(data, ffmpeg_path(), preview_only=args.preview)


if __name__ == '__main__':
    main()
