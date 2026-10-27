#!/usr/bin/env python3
"""Batch 3: normalize actual selected-voice audio, acoustic captions, card-timed 1080p.

Run after build_batch3.py and generating its nine speech clips. No network calls.
Only Batch 3 output paths are used. Scratch audio/video/images are git-ignored.
Caption timing is MFCC/DTW alignment, NOT proportional text-duration estimation.
A 144px caption band is reserved at authoring time: no legal text is obscured.
The final MP4 replaces a previous Batch 3 MP4 only after a successful full decode.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
import wave

import imageio_ffmpeg
from mutagen.mp3 import MP3
from PIL import Image, ImageDraw

import build_subtitles as acoustic
from build_video import block, font, metadata_escape, run
from batch3_roman import romanize
from build_batch3 import dump, register

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'video-work/batch3'
SCRIPT = ROOT / 'batch-03-narration.json'
VIDEO = ROOT / 'batch-03-video.mp4'
FPS = 10
BG, PANEL, WHITE, MUTED, GOLD, BLUE, GREEN = '#090e1e', '#142139', '#eff3fd', '#b8c6de', '#ffda70', '#57d1ff', '#57e1ba'


def prepare_audio(ffmpeg, scripts):
    cursor, chapters, waves = 0.0, [], []
    for i, s in enumerate(scripts, 1):
        source, target = WORK / 'audio' / s['file'], WORK / f'audio-{i:02}.wav'
        if not source.is_file():
            raise FileNotFoundError('Generate selected voice clip first: ' + str(source))
        duration = math.ceil(MP3(source).info.length * FPS) / FPS
        run([ffmpeg, '-v', 'error', '-y', '-i', str(source), '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11,apad',
             '-t', f'{duration:.3f}', '-ar', '48000', '-ac', '2', '-c:a', 'pcm_s16le', str(target)])
        with wave.open(str(target), 'rb') as w:
            duration = w.getnframes() / w.getframerate()
        chapters.append(dict(number=i, title=s['title'], start_seconds=round(cursor, 3), end_seconds=round(cursor + duration, 3),
                             card_ids=[u['card_id'] for u in s['units']], voice_id=s['voice'], source_clip_file=s['file'],
                             source_text_sha256=hashlib.sha256(s['text'].encode()).hexdigest(),
                             source_clip_sha256=hashlib.sha256(source.read_bytes()).hexdigest()))
        waves.append(target)
        cursor += duration
    with wave.open(str(WORK / 'master.wav'), 'wb') as output:
        output.setparams((2, 2, 48000, 0, 'NONE', 'not compressed'))
        for path in waves:
            with wave.open(str(path), 'rb') as w:
                output.writeframes(w.readframes(w.getnframes()))
    run([ffmpeg, '-v', 'error', '-y', '-i', str(WORK / 'master.wav'), '-c:a', 'libmp3lame', '-b:a', '96k',
         '-metadata', 'title=CCS LTC Batch 3 - Hometown and destination - City Hinglish', str(ROOT / 'batch-03-hinglish.mp3')])
    return chapters


def parts(segment):
    if segment['units']:
        return [(u['card_id'], ' '.join((u['spoken_ref'], u['explanation'], 'Example, ' + u['example']))) for u in segment['units']]
    legal, practical = segment['text'].split('Aaj ', 1)
    return [('OPEN-LEGAL', legal.strip()), ('OPEN-PRACTICAL', 'Aaj ' + practical)]


def merge_readable(cues):
    """Merge flashing cues without moving any acoustic boundary or dropping words."""
    merged = []
    for cue in cues:
        if merged and (cue['end'] - cue['start'] < .55 or merged[-1]['end'] - merged[-1]['start'] < .55):
            previous = merged.pop()
            merged.append({**previous, 'end': cue['end'], 'text': previous['text'] + ' ' + cue['text']})
        else:
            merged.append(cue)
    # A bad acoustic fit must not be hidden by manufacturing ratio-based times.
    # Neighbour merges retain the actual DTW edges and are audited in the report.
    index = 0
    while index < len(merged):
        cue = merged[index]
        duration = cue['end'] - cue['start']
        if duration > 0 and len(romanize(cue['text'])) / duration <= 35:
            index += 1
            continue
        if len(merged) == 1:
            raise ValueError('Chapter alignment is too fast to read; inspect audio/timing')
        neighbour = index + 1 if index + 1 < len(merged) else index - 1
        a, b = sorted((index, neighbour))
        left, right = merged[a], merged[b]
        combined = {**left, 'end': right['end'], 'text': left['text'] + ' ' + right['text']}
        if len(romanize(combined['text'])) > 174:
            raise ValueError('Alignment requires an unreadably long cue; review rather than silently approximate')
        merged[a:b + 1] = [combined]
        index = a
    return merged


def align(ffmpeg, reference, segment, chapter):
    import numpy as np
    from scipy.spatial.distance import cdist
    from dtw import dtw
    phrases, markers = [], []
    for ident, text in parts(segment):
        markers.append((ident, len(phrases)))
        phrases.extend(acoustic.split_phrases(text, limit=76))
    if ' '.join(phrases).split() != segment['text'].split():
        raise ValueError('Phrase segmentation changed the transcript')
    pieces = [reference.synthesize(phrase) for phrase in phrases]
    boundaries = np.cumsum([0] + [len(piece) for piece in pieces]) / acoustic.SAMPLE_RATE
    ref_features = acoustic.features(np.concatenate(pieces))
    start, end = chapter['start_seconds'], chapter['end_seconds']
    raw = subprocess.check_output([ffmpeg, '-v', 'error', '-ss', str(start), '-i', str(WORK / 'master.wav'), '-t', str(end - start),
                                   '-vn', '-ac', '1', '-ar', str(acoustic.SAMPLE_RATE), '-f', 's16le', '-'])
    real_features = acoustic.features(np.frombuffer(raw, dtype='<i2').astype('float64'))
    distances = cdist(ref_features, real_features, metric='cosine')
    path = dtw(distances, step_pattern='symmetric2', keep_internals=False)
    ref_frames, real_frames = np.asarray(path.index1), np.asarray(path.index2)
    mapped = []
    for boundary in boundaries:
        frame = min(round(boundary / acoustic.FRAME_STEP), len(ref_features) - 1)
        selected = real_frames[ref_frames == frame]
        mapped.append(float(np.median(selected)) * acoustic.FRAME_STEP)
    mapped[0], mapped[-1] = 0.0, end - start
    if any(b < a for a, b in zip(mapped, mapped[1:])):
        raise ValueError('Non-monotonic acoustic alignment')
    raw_cues = [dict(chapter=chapter['number'], start=round(start + a, 3), end=round(start + b, 3), text=phrase)
                for a, b, phrase in zip(mapped, mapped[1:], phrases)]
    cues = [{**c, 'spoken_text': c['text'], 'text': romanize(c['text'])} for c in merge_readable(raw_cues)]
    pages = [dict(id=ident, start_seconds=round(start + mapped[index], 3), chapter=chapter['number']) for ident, index in markers]
    metrics = dict(chapter=chapter['number'], dtw_normalized_distance=float(path.normalizedDistance),
                   reference_seconds=round(float(boundaries[-1]), 3), raw_cue_count=len(raw_cues), cue_count=len(cues))
    return cues, pages, metrics


def captions(cues):
    ass = ['[Script Info]', 'ScriptType: v4.00+', 'PlayResX: 1920', 'PlayResY: 1080', 'WrapStyle: 2',
           'ScaledBorderAndShadow: yes', '', '[V4+ Styles]',
           'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
           'Style: Default,Atkinson Hyperlegible,40,&H00FFFFFF,&H00FFFFFF,&H00111B26,&H00111B26,0,0,0,0,100,100,0,0,1,1,0,2,110,110,20,1',
           '', '[Events]', 'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text']
    srt, vtt = [], ['WEBVTT\n']
    for i, cue in enumerate(cues, 1):
        text = acoustic.wrap_caption(cue['text'])
        if any(ch in text for ch in '{}\\'):
            raise ValueError('Unexpected ASS control character')
        if any(font(40).getlength(line) > 1700 for line in text.splitlines()):
            raise ValueError('Caption exceeds the safe width')
        srt.append(f'{i}\n{acoustic.timestamp(cue["start"])} --> {acoustic.timestamp(cue["end"])}\n{text}\n')
        vtt.append(f'{i}\n{acoustic.timestamp(cue["start"], True)} --> {acoustic.timestamp(cue["end"], True)}\n{text}\n')
        ass.append(f'Dialogue: 0,{acoustic.ass_timestamp(cue["start"])},{acoustic.ass_timestamp(cue["end"])},Default,,0,0,0,,' + text.replace('\n', r'\N'))
    for ext, lines in (('srt', srt), ('vtt', vtt), ('ass', ass)):
        (ROOT / f'batch-03-video.{ext}').write_text('\n'.join(lines).rstrip() + '\n')


def base(draw, ident, title):
    draw.rectangle((0, 0, 1920, 8), fill=BLUE)
    draw.text((64, 30), 'CCS / LTC STUDIO', font=font(29, True), fill=WHITE)
    draw.text((1120, 35), 'BATCH 03  |  HOMETOWN & DESTINATION', font=font(25), fill=MUTED)
    draw.line((64, 84, 1856, 84), fill='#344363', width=2)
    draw.text((64, 106), ident + '  |  REFERENCE > EXPLANATION > EXAMPLE', font=font(24, True), fill=BLUE)
    block(draw, title, (64, 146), 1792, 110, start=50, minimum=42, bold=True)
    draw.rectangle((0, 936, 1920, 1080), fill='#111b26')
    draw.line((64, 936, 1856, 936), fill='#344363', width=2)
    draw.text((64, 910), 'Educational examples | Exact sources & fuller restatements: batch-03.pdf | Reviewed 27 Oct 2026', font=font(21), fill=MUTED)


def slide(card, destination):
    image = Image.new('RGB', (1920, 1080), BG)
    draw = ImageDraw.Draw(image)
    base(draw, card['id'], card['title'])
    refsize = block(draw, card['ref'], (64, 260), 1792, 84, GOLD, start=30, minimum=26, bold=True)
    sizes = [refsize]
    for x, width, label, color, key in ((64, 870, 'SIMPLE CITY HINGLISH', BLUE, 'explanation_roman'),
                                       (962, 894, 'IMMEDIATE EXAMPLE / HYPOTHETICAL', GREEN, 'example_roman')):
        draw.rounded_rectangle((x, 360, x + width, 752), 18, fill=PANEL, outline=color, width=2)
        draw.text((x + 26, 382), label, font=font(24, True), fill=color)
        sizes.append(block(draw, card[key], (x + 26, 435), width - 52, 293, start=39, minimum=34))
    draw.rounded_rectangle((64, 774, 1856, 894), 12, fill='#282414', outline=GOLD)
    sizes.append(block(draw, 'WATCH OUT: ' + card['trap'], (86, 792), 1748, 90, GOLD, start=30, minimum=27))
    image.save(destination)
    return {'body_font_sizes': sizes, 'caption_band_height': 144}


def opening(kind, destination):
    image = Image.new('RGB', (1920, 1080), BG)
    draw = ImageDraw.Draw(image)
    base(draw, 'DATES FIRST', 'Key legal dates' if kind == 'OPEN-LEGAL' else 'Practical blocks and deadlines')
    if kind == 'OPEN-LEGAL':
        rows = [('11.02.1958', 'Own-Controlling-Officer declaration route; issue date, not a new benefit'),
                ('24.06.1958', 'Normal-residence test; visits > property > relations > pre-service residence'),
                ('18.05.2015', 'HQ = hometown / other-state NCR clarification, cited in official FAQ'),
                ('01.07 / 03.09.2025', 'FAQ / consolidation; full Rule 6 versus compressed summary disclosed'),
                ('31.10.1958', 'EXPIRED redeclaration window; historical 1958-59 block, NOT current')]
    else:
        rows = [('2026-2029', 'Current REGULAR block; sub-blocks 2026-27 and 2028-29'),
                ('31.12.2026', 'CONDITIONAL unused previous-block carryover; Rule 10 conditions apply'),
                ('BEFORE start', 'Declare All-India place in advance; CO approval for pre-start change'),
                ('AFTER start', 'Normally no change; beyond-control inability to request earlier + relaxation'),
                ('No fixed day count', 'Rule 6 has no universal 21/30-day deadline; other instructions still apply')]

    for index, (date, text) in enumerate(rows):
        y = 285 + index * 111
        draw.rounded_rectangle((64, y, 1856, y + 99), 12, fill=PANEL, outline='#344363')
        block(draw, date, (88, y + 20), 432, 68, GOLD, start=36, minimum=30, bold=True)
        block(draw, text, (548, y + 16), 1280, 74, start=32, minimum=28)
    block(draw, 'Issue dates are not blanket new effective dates. Check the written companion for the historical crosswalk and conditions.',
          (70, 853), 1780, 52, MUTED, start=24, minimum=22)
    image.save(destination)
    return {'caption_band_height': 144}


def render_raw(ffmpeg, pages, chapters, cards):
    by_id = {c['id']: c for c in cards}
    total = chapters[-1]['end_seconds']
    rendered_pages = []
    for index, original in enumerate(pages):
        page = {**original, 'end_seconds': pages[index + 1]['start_seconds'] if index + 1 < len(pages) else total}
        if page['end_seconds'] <= page['start_seconds']:
            raise ValueError('Card has no positive display time')
        path = WORK / (page['id'] + '.png')
        layout = opening(page['id'], path) if page['id'].startswith('OPEN-') else slide(by_id[page['id']], path)
        rendered_pages.append({**page, 'layout': layout})
        if page['id'] == 'B3-22':
            Image.open(path).save(ROOT / 'batch-03-video-poster.jpg', quality=90)
    lines = ['ffconcat version 1.0']
    for page in rendered_pages:
        lines += ["file '" + page['id'] + ".png'", f'duration {page["end_seconds"] - page["start_seconds"]:.3f}']
    lines.append("file '" + pages[-1]['id'] + ".png'")
    listing = WORK / 'slides.ffconcat'
    listing.write_text('\n'.join(lines) + '\n')
    metadata = WORK / 'chapters.ffmeta'
    lines = [';FFMETADATA1', 'title=CCS LTC Batch 3 - Hometown and destination - Roman Hinglish']
    for c in chapters:
        lines += ['[CHAPTER]', 'TIMEBASE=1/1000', f'START={round(c["start_seconds"] * 1000)}',
                  f'END={round(c["end_seconds"] * 1000)}', 'title=' + metadata_escape(c['title'])]
    metadata.write_text('\n'.join(lines) + '\n')
    raw = WORK / 'clean.mp4'
    run([ffmpeg, '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(listing), '-i', str(WORK / 'master.wav'),
         '-f', 'ffmetadata', '-i', str(metadata), '-map', '0:v:0', '-map', '1:a:0', '-map_metadata', '2', '-map_chapters', '2',
         '-vf', 'fps=10', '-t', str(total), '-c:v', 'libx264', '-threads', '2', '-preset', 'veryfast', '-tune', 'stillimage',
         '-crf', '23', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '96k', '-ar', '48000', '-ac', '2',
         '-movflags', '+faststart', str(raw)])
    return raw, rendered_pages


def final(ffmpeg, raw, chapters, pages, subtitle_report):
    target = WORK / 'captioned.mp4'
    before = acoustic.audio_digest(ffmpeg, raw)
    run([ffmpeg, '-v', 'error', '-y', '-i', str(raw), '-map', '0:v:0', '-map', '0:a:0', '-map_metadata', '0', '-map_chapters', '0',
         '-vf', 'ass=batch-03-video.ass:fontsdir=video-fonts', '-c:v', 'libx264', '-threads', '2', '-preset', 'veryfast',
         '-crf', '22', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart', str(target)])
    run([ffmpeg, '-v', 'error', '-xerror', '-i', str(target), '-map', '0:v:0', '-map', '0:a:0', '-f', 'null', '-'])
    if acoustic.audio_digest(ffmpeg, target) != before:
        raise ValueError('Caption render changed the AAC bitstream')
    reader = imageio_ffmpeg.read_frames(str(target))
    metadata = next(reader)
    reader.close()
    if metadata['size'] != (1920, 1080) or abs(metadata['duration'] - chapters[-1]['end_seconds']) > .2:
        raise ValueError('Unexpected final video metadata: ' + str(metadata))
    # Embedded chapters must also match the actual MP4, not just our own report.
    chapter_dump = subprocess.run([ffmpeg, '-hide_banner', '-i', str(target)], capture_output=True, text=True)
    for c in chapters:
        key = f'Chapter #0:{c["number"] - 1}: start {c["start_seconds"]:.6f}, end {c["end_seconds"]:.6f}'
        if key not in chapter_dump.stderr:
            raise ValueError('Embedded chapter differs: ' + key)
    subtitle_report = {**subtitle_report, 'full_decode_check': 'passed', 'audio_stream_unchanged': True,
                       'audio_sha256': before, 'burned_in': True, 'video_bytes': target.stat().st_size}
    target.replace(VIDEO)
    dump('batch-03-subtitle-report.json', subtitle_report)
    dump('batch-03-video-report.json', dict(file=VIDEO.name, bytes=VIDEO.stat().st_size, width=1920, height=1080,
         duration_seconds=metadata['duration'], fps=10, video_codec='h264', audio_codec='aac', full_decode_check='passed',
         embedded_chapter_check='passed', source_script_sha256=hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),
         chapters=chapters, pages=pages, subtitles=dict(burned_in=True, script='Roman Hinglish', srt='batch-03-video.srt',
         vtt='batch-03-video.vtt', caption_band_height=144),
         review_limit='Automatic acoustic phrase alignment and technical checks; not a certified word-level or full manual listening audit.'))
    register()
    print('BATCH 3 READY:', metadata['duration'], 'seconds;', len(pages), 'pages;', len(subtitle_report['cues']), 'Roman cues', flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--render-only', action='store_true', help='Reuse acoustic report/normalized master for a layout-only correction')
    args = parser.parse_args()
    WORK.mkdir(parents=True, exist_ok=True)
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    scripts = json.loads(SCRIPT.read_text())
    cards = json.loads((ROOT / 'batch-03.json').read_text())['cards']
    if not args.render_only:
        chapters = prepare_audio(ffmpeg, scripts)
        reference = acoustic.ReferenceSpeech()
        cues, pages, audits = [], [], []
        for s, c in zip(scripts, chapters, strict=True):
            chapter_cues, chapter_pages, metrics = align(ffmpeg, reference, s, c)
            cues.extend(chapter_cues)
            pages.extend(chapter_pages)
            audits.append(metrics)
            print('Aligned chapter', c['number'], '/', len(chapters), 'cues', len(chapter_cues), flush=True)
        report = dict(source_script_sha256=hashlib.sha256(SCRIPT.read_bytes()).hexdigest(), source_script_file=SCRIPT.name,
                      alignment='chapter-local MFCC / DTW against Hindi eSpeak NG reference speech', frame_step_seconds=.02,
                      timing_precision_note='20ms analysis grid is not a verified 20ms synchronization-accuracy guarantee. Automatic phrase alignment, not certified word-level timing.',
                      language='Roman-script city Hinglish; reviewed reversible transliteration, not translation',
                      chapters=audits, cues=cues, full_decode_check='not rendered')
        dump('batch-03-subtitle-report.json', report)
        (WORK / 'plan.json').write_text(json.dumps(dict(chapters=chapters, pages=pages), indent=2))
    else:
        plan = json.loads((WORK / 'plan.json').read_text())
        chapters, pages = plan['chapters'], plan['pages']
        report = json.loads((ROOT / 'batch-03-subtitle-report.json').read_text())
        if report['source_script_sha256'] != hashlib.sha256(SCRIPT.read_bytes()).hexdigest():
            raise ValueError('Script changed: fresh speech/alignment is required')
    captions(report['cues'])
    raw, rendered_pages = render_raw(ffmpeg, pages, chapters, cards)
    print('Clean slide video encoded; burning Roman captions', flush=True)
    final(ffmpeg, raw, chapters, rendered_pages, report)


if __name__ == '__main__':
    # Paths in the fixed ASS filter are relative to this directory, not caller cwd.
    import os
    os.chdir(ROOT)
    main()
