#!/usr/bin/env python3
"""Build a 1080p chapter-timed video from the approved clause-reference script.

Install: python -m pip install -r docs/ccs-ltc/video-requirements.txt
Build:   python docs/ccs-ltc/build_video.py
Needs the ten selected-voice clips in video-work/audio/, named by narration.json.
Those clips are generated separately, not by this script. No TTS substitution.

Slides are chapter summaries, not word-synchronised captions. Encoding durations
come from the actual video narration clips, not estimates from text length.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess

from PIL import Image, ImageDraw, ImageFont
from mutagen.mp3 import MP3
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parent
W, H, FPS = 1920, 1080, 10
BG, PANEL, WHITE = '#090e1e', '#121e35', '#eff3fd'
MUTED, GOLD = '#b8c6de', '#ffda70'
COLORS = ('#57d1ff', '#ffda70', '#57e1ba', '#c8a9ff')
TITLES = (
    'Batch 1 | The clause-reference edition',
    'Scheme name, start date & the entry gate',
    'Who is included? Four legal categories',
    'Who is excluded? Clauses (a) to (c)',
    'Who is excluded? Clauses (d) to (g)',
    'Rule 2(1) | Service, certificate & hometown',
    'Four-year tenure, extension & continuity',
    'Re-employment conditions & Rule 3 scope',
    'Separate family travel & applicability notes',
    'Source hierarchy & the final checklist',
)
CAUTIONS = (
    'Every spoken reference is followed by an explanation and a hypothetical example.',
    'The exact 1988 Gazette publication day remains unverified. Dates shown are hypothetical.',
    'Inclusion alone is not final approval: exclusions and other LTC conditions still apply.',
    'One year of service does not override an express exclusion in Rule 1(4).',
    'Railway pass-surrender details remain pending. Check relevant later instructions.',
    'Rule 2(1) has unlettered conditions. These teaching labels do not invent clause letters.',
    'Duration and no-break continuity do not create a fresh occasion in an already-used block.',
    'Rule 3 has no numbered sub-rules. Full Rule 4(d) family detail belongs to the next batch.',
    'Guideline notes are not new Rule 1 clauses. The 1960-61 starting block is historical.',
    'Open checks: exact Gazette date, detailed Railway conditions and exhaustive later orders.',
)


def font(size, bold=False):
    name = 'AtkinsonHyperlegible-Bold.ttf' if bold else 'AtkinsonHyperlegible-Regular.ttf'
    return ImageFont.truetype(str(ROOT / 'video-fonts' / name), size)


def wrap(text, face, width):
    lines = []
    for paragraph in text.split('\n'):
        current = ''
        for word in paragraph.split():
            if face.getlength(word) > width:
                raise ValueError(f'Unbreakable word exceeds video layout: {word}')
            candidate = f'{current} {word}'.strip()
            if current and face.getlength(candidate) > width:
                lines.append(current)
                current = word
            else:
                current = candidate
        lines.append(current)
    return lines


def fit(text, width, height, start=30, minimum=26, bold=False):
    for size in range(start, minimum - 1, -1):
        face = font(size, bold)
        lines = wrap(text, face, width)
        line_height = math.ceil(size * 1.2)
        if len(lines) * line_height <= height:
            return face, lines, line_height, size
    raise ValueError(f'Video text would require a font smaller than {minimum}px: {text}')


def block(draw, text, xy, width, height, color=WHITE, start=30, minimum=26, bold=False):
    face, lines, line_height, size = fit(text, width, height, start, minimum, bold)
    for index, line in enumerate(lines):
        draw.text((xy[0], xy[1] + index * line_height), line, font=face, fill=color)
    return size


def reference_label(unit):
    ref = unit['legal_ref']
    if ref.startswith('2025 Guidelines:'):
        return ref.replace('2025 Guidelines:', 'DoPT Guidelines\n03.09.2025 |')
    if ref.startswith('Rule 3 +'):
        return 'Rule 3; Rules 9/11\nFAQ 6 (01.07.2025)'
    if ref.startswith('Batch 1'):
        return 'Teaching checklist\nNot a legal rule'
    return ref.replace(': ', '\n').replace(' + later instructions', '\n+ later instructions')


def intro(draw):
    draw.text((84, 300), 'REFERENCE  >  EXPLANATION  >  EXAMPLE', font=font(35, True), fill=COLORS[0])
    stats = [('Rules 1-3', 'Clearly bounded legal scope'),
             ('30 cards', 'Each mapped to a spoken anchor'),
             ('City Hinglish', 'Same selected teacher + questioner'),
             ('10 chapters', 'Visual summaries timed to audio')]
    for index, (title, subtitle) in enumerate(stats):
        x = 64 + index * 454
        draw.rounded_rectangle((x, 396, x + 430, 550), 16, fill=PANEL, outline=COLORS[index], width=2)
        block(draw, title, (x + 22, 417), 386, 50, COLORS[index], start=36, bold=True)
        block(draw, subtitle, (x + 22, 478), 386, 66, MUTED, start=26)
    draw.text((84, 610), 'How to follow the references', font=font(34, True), fill=WHITE)
    block(draw, 'Rule 1(3)(i) is spoken as: Rule one, sub rule three, clause Roman one.',
          (84, 668), 1730, 70, start=34)
    block(draw, 'Rule 1(4)(a) is spoken as: Rule one, sub rule four, clause A.',
          (84, 726), 1730, 70, start=34)
    block(draw, 'Rule 2(1) conditions have no separate letters. Supplementary notes are labelled separately.',
          (84, 806), 1730, 90, MUTED, start=30)


def render_slide(index, segment, summaries, path):
    image = Image.new('RGB', (W, H), BG)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, W, 8), fill=COLORS[index % 4])
    draw.text((64, 30), 'CCS / LTC STUDIO', font=font(29, True), fill=WHITE)
    draw.text((1120, 35), 'BATCH 01   |   CITY HINGLISH   |   1080p', font=font(24), fill=MUTED)
    draw.line((64, 84, W - 64, 84), fill='#344363', width=2)
    draw.text((64, 112), f'CHAPTER {index + 1:02} / 10  |  RULES 1-3 & ASSOCIATED NOTES', font=font(23, True), fill=COLORS[index % 4])
    block(draw, TITLES[index], (64, 155), W - 128, 66, start=48, minimum=38, bold=True)
    draw.text((64, 230), 'On-screen points are summaries. Listen for each clause reference before its explanation.', font=font(27), fill=MUTED)
    sizes = []
    units = segment['units']
    if not units:
        intro(draw)
    else:
        row_height = {2: 238, 3: 194, 4: 150}[len(units)]
        for row, unit in enumerate(units):
            y = 294 + row * (row_height + 12)
            color = COLORS[row % 4]
            draw.rounded_rectangle((64, y, W - 64, y + row_height), 14, fill=PANEL, outline=color, width=2)
            draw.rectangle((65, y + 14, 72, y + row_height - 14), fill=color)
            draw.text((90, y + 13), unit['card_id'], font=font(18, True), fill=color)
            sizes.append(block(draw, reference_label(unit), (90, y + 44), 355, row_height - 54, color, start=29, bold=True))
            draw.line((470, y + 16, 470, y + row_height - 16), fill='#344363')
            draw.text((494, y + 12), 'SIMPLE POINT', font=font(18, True), fill=COLORS[0])
            summary = summaries[unit['card_id']]
            sizes.append(block(draw, summary['point'], (494, y + 43), 600, row_height - 51, start=30))
            draw.line((1120, y + 16, 1120, y + row_height - 16), fill='#344363')
            draw.text((1144, y + 12), 'EXAMPLE / HYPOTHETICAL', font=font(18, True), fill=COLORS[2])
            sizes.append(block(draw, summary['example'], (1144, y + 43), 686, row_height - 51, start=30))
    draw.rounded_rectangle((64, 940, W - 64, 1005), 12, fill='#282414', outline=GOLD, width=2)
    block(draw, CAUTIONS[index], (86, 952), W - 172, 45, GOLD, start=28)
    draw.text((64, 1024), 'Sources & evidence limits: Batch 1 PDF / REVIEW-NOTES.md | Text review: 27 Oct 2026', font=font(23), fill=MUTED)
    for chapter in range(10):
        x = 64 + chapter * 180
        draw.rounded_rectangle((x, 1060, x + 166, 1066), 3, fill=COLORS[0] if chapter <= index else '#2b3653')
    image.save(path)
    return dict(canvas=[W, H], body_font_sizes=sizes)


def run(command):
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(f'Command failed: {command[0]}\n{result.stderr[-5000:]}')
    return result


def metadata_escape(value):
    return re.sub(r'([\\=;#])', r'\\\1', value).replace('\n', ' ')


def encode(slide, audio, duration, output, ffmpeg):
    run([ffmpeg, '-hide_banner', '-y', '-loop', '1', '-framerate', str(FPS), '-i', str(slide),
         '-i', str(audio), '-t', f'{duration:.3f}', '-map', '0:v:0', '-map', '1:a:0',
         '-c:v', 'libx264', '-threads', '2', '-preset', 'veryfast', '-tune', 'stillimage',
         '-crf', '24', '-pix_fmt', 'yuv420p', '-r', str(FPS),
         '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11,apad', '-c:a', 'aac', '-b:a', '96k',
         '-ar', '48000', '-ac', '2', '-movflags', '+faststart', str(output)])


def build(slides_only=False):
    work = ROOT / 'video-work'
    work.mkdir(exist_ok=True)
    segments = json.loads((ROOT / 'narration.json').read_text())
    summaries = {s['card_id']: s for s in json.loads((ROOT / 'video-summaries.json').read_text())}
    cards = json.loads((ROOT / 'batch-01.json').read_text())['cards']
    units = [u for s in segments for u in s['units']]
    if [u['card_id'] for u in units] != [c['id'] for c in cards]:
        raise ValueError('Video must preserve all 30 clause-reference cards, in order')
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    chapters, clips, cursor = [], [], 0.0
    for index, segment in enumerate(segments):
        slide = work / f'chapter-{index + 1:02}.png'
        audit = render_slide(index, segment, summaries, slide)
        if index == 2:
            with Image.open(slide) as image:
                image.save(ROOT / 'batch-01-video-poster.jpg', quality=90)
        if slides_only:
            print(f'Layout passed: chapter {index + 1:02}', flush=True)
            continue
        audio = work / 'audio' / segment['file']
        audio_duration = MP3(audio).info.length
        duration = math.ceil(audio_duration * FPS) / FPS
        clip = work / f'chapter-{index + 1:02}.mp4'
        encode(slide, audio, duration, clip, ffmpeg)
        chapters.append(dict(number=index + 1, title=TITLES[index], start_seconds=round(cursor, 3),
                             end_seconds=round(cursor + duration, 3), audio_duration=audio_duration,
                             card_ids=[u['card_id'] for u in segment['units']], layout=audit))
        cursor += duration
        clips.append(clip)
        print(f'Encoded chapter {index + 1:02}/10 | {duration:.1f}s | {clip.stat().st_size / 1048576:.1f} MiB', flush=True)
    if slides_only:
        return
    concat = work / 'concat.txt'
    concat.write_text('\n'.join(f"file '{p.name}'" for p in clips) + '\n')
    metadata = work / 'chapters.ffmeta'
    lines = [';FFMETADATA1', 'title=CCS LTC Batch 1 - Clause-reference edition',
             'comment=City Hinglish. Chapter summary slides, not word-synchronised captions.']
    for chapter in chapters:
        lines += ['[CHAPTER]', 'TIMEBASE=1/1000', f'START={round(chapter["start_seconds"] * 1000)}',
                  f'END={round(chapter["end_seconds"] * 1000)}', f'title={metadata_escape(chapter["title"])}']
    metadata.write_text('\n'.join(lines) + '\n')
    output = ROOT / 'batch-01-video.mp4'
    run([ffmpeg, '-hide_banner', '-y', '-f', 'concat', '-safe', '0', '-i', str(concat),
         '-f', 'ffmetadata', '-i', str(metadata), '-map', '0:v:0', '-map', '0:a:0',
         '-map_metadata', '1', '-map_chapters', '1', '-c', 'copy', '-movflags', '+faststart', str(output)])
    # Full decode check, not just file existence. Fail before publishing a broken MP4.
    run([ffmpeg, '-hide_banner', '-v', 'error', '-i', str(output), '-map', '0:v:0', '-map', '0:a:0', '-f', 'null', '-'])
    reader = imageio_ffmpeg.read_frames(str(output))
    info = next(reader)
    reader.close()
    if tuple(info['size']) != (W, H) or abs(info['duration'] - cursor) > 1:
        raise ValueError(f'Unexpected rendered video metadata: {info}')
    report = dict(file=output.name, bytes=output.stat().st_size, width=W, height=H, fps=FPS,
                  duration_seconds=info['duration'], video_codec='h264', audio_codec='aac',
                  source_script_sha256=hashlib.sha256((ROOT / 'narration.json').read_bytes()).hexdigest(),
                  note='New synthesis of the same approved script and selected voices. Existing standalone MP3 unchanged. Slides switch at actual audio-chapter boundaries, not individual word boundaries.',
                  full_decode_check='passed', chapters=chapters)
    (ROOT / 'video-build-report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(f'VIDEO READY: {output} | {info["duration"]:.2f}s | {output.stat().st_size / 1048576:.1f} MiB', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--slides-only', action='store_true')
    build(parser.parse_args().slides_only)
