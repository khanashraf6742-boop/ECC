#!/usr/bin/env python3
"""Prepend selected-voice dates/GID lessons to the clean original video.

The fixed Git source is the pre-caption edition, never a captioned-on-captioned
transcode. Six new MP3s are required in ignored video-work/audio/. No TTS fallback.
After this script run build_subtitles.py for Roman-Hinglish captions.
"""
import hashlib
import json
import math
from pathlib import Path
import subprocess

import imageio_ffmpeg
from mutagen.mp3 import MP3
from PIL import Image, ImageDraw

import build_video as base

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'video-work' / 'extension'
BASE_COMMIT = 'f7badf15704c978b447c1ae5708d13f9bea47313'


def git_source(relative):
    try:
        return subprocess.check_output(['git', 'show', f'{BASE_COMMIT}:docs/ccs-ltc/{relative}'], cwd=ROOT)
    except subprocess.CalledProcessError as error:
        raise RuntimeError(f'Clean original unavailable. Fetch it first: git fetch origin {BASE_COMMIT}') from error


def render_prefix(index, segment, path):
    image = Image.new('RGB', (base.W, base.H), base.BG)
    draw = ImageDraw.Draw(image)
    color = base.COLORS[index % 4]
    draw.rectangle((0, 0, base.W, 8), fill=color)
    draw.text((64, 30), 'CCS / LTC STUDIO', font=base.font(29, True), fill=base.WHITE)
    draw.text((1030, 35), 'DATES + GIDs   |   ROMAN HINGLISH', font=base.font(24), fill=base.MUTED)
    draw.line((64, 84, base.W - 64, 84), fill='#344363', width=2)
    draw.text((64, 112), f'OPENING {index + 1:02} / 06  |  REVIEW: 27 OCT 2026', font=base.font(23, True), fill=color)
    base.block(draw, segment['title'], (64, 155), base.W - 128, 66, start=44, minimum=36, bold=True)
    draw.text((64, 230), 'Exact reference first. Simple explanation next. Practical hypothetical immediately after.', font=base.font(26), fill=base.MUTED)
    units = segment['units']
    height = 194 if len(units) == 3 else 238
    sizes = []
    for row, unit in enumerate(units):
        y = 294 + row * (height + 12)
        shade = base.COLORS[row % 4]
        draw.rounded_rectangle((64, y, base.W - 64, y + height), 14, fill=base.PANEL, outline=shade, width=2)
        draw.text((90, y + 12), unit['card_id'], font=base.font(18, True), fill=shade)
        sizes.append(base.block(draw, unit['legal_ref'], (90, y + 43), 350, height - 52, shade, start=28))
        draw.line((470, y + 16, 470, y + height - 16), fill='#344363')
        draw.text((494, y + 12), 'DATE / SIMPLE POINT', font=base.font(18, True), fill=base.COLORS[0])
        sizes.append(base.block(draw, unit['point'], (494, y + 43), 600, height - 52, start=30))
        draw.line((1120, y + 16, 1120, y + height - 16), fill='#344363')
        draw.text((1144, y + 12), 'EXAMPLE / HYPOTHETICAL', font=base.font(18, True), fill=base.COLORS[2])
        sizes.append(base.block(draw, unit['visual_example'], (1144, y + 43), 686, height - 52, start=30))
    draw.rounded_rectangle((64, 940, base.W - 64, 1005), 12, fill='#282414', outline=base.GOLD, width=2)
    base.block(draw, segment['caution'], (86, 950), base.W - 172, 48, base.GOLD, start=27, minimum=26)
    draw.text((64, 1024), 'Sources: DATES-AND-GIDS.md | Full series coverage: gid-coverage-register.csv | Evidence holds retained', font=base.font(23), fill=base.MUTED)
    image.save(path)
    return {'canvas': [base.W, base.H], 'body_font_sizes': sizes}


def aac_bytes(ffmpeg, path):
    return subprocess.check_output([ffmpeg, '-v', 'error', '-i', str(path), '-map', '0:a:0',
                                    '-c:a', 'copy', '-f', 'adts', '-'])


def build():
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    WORK.mkdir(parents=True, exist_ok=True)
    source = WORK / 'original-clean.mp4'
    source.write_bytes(git_source('batch-01-video.mp4'))
    old_report = json.loads(git_source('video-build-report.json'))
    prefix = json.loads((ROOT / 'video-prefix.json').read_text())
    old_script = json.loads((ROOT / 'narration.json').read_text())
    script_path = ROOT / 'video-narration.json'
    script_path.write_text(json.dumps(prefix + old_script, ensure_ascii=False, indent=2) + '\n')
    chapters, clips, cursor = [], [], 0.0
    for index, segment in enumerate(prefix):
        audio = ROOT / 'video-work' / 'audio' / segment['file']
        if not audio.exists():
            raise FileNotFoundError(f'Selected-voice clip is required: {audio}')
        duration = math.ceil(MP3(audio).info.length * base.FPS) / base.FPS
        slide, clip = WORK / f'opening-{index + 1}.png', WORK / f'opening-{index + 1}.mp4'
        audit = render_prefix(index, segment, slide)
        base.encode(slide, audio, duration, clip, ffmpeg)
        chapters.append({'number': index + 1, 'title': segment['title'], 'start_seconds': round(cursor, 3),
                         'end_seconds': round(cursor + duration, 3), 'audio_duration': MP3(audio).info.length,
                         'card_ids': [u['card_id'] for u in segment['units']], 'layout': audit})
        clips.append(clip)
        cursor += duration
        print(f'New opening chapter {index + 1}/6: {duration:.1f}s', flush=True)
    prefix_duration = round(cursor, 3)
    for chapter in old_report['chapters']:
        chapters.append({**chapter, 'number': chapter['number'] + len(prefix),
                         'start_seconds': round(chapter['start_seconds'] + prefix_duration, 3),
                         'end_seconds': round(chapter['end_seconds'] + prefix_duration, 3)})
    clips.append(source)
    concat = WORK / 'concat.txt'
    concat.write_text('\n'.join(f"file '{p.name}'" for p in clips) + '\n')
    lines = [';FFMETADATA1', 'title=CCS LTC Batch 1 - Dates and GIDs - Roman Hinglish',
             'comment=Dates-first edition. Original ten core chapters retained; automatic phrase captions follow.']
    for chapter in chapters:
        lines += ['[CHAPTER]', 'TIMEBASE=1/1000', f'START={round(chapter["start_seconds"] * 1000)}',
                  f'END={round(chapter["end_seconds"] * 1000)}', f'title={base.metadata_escape(chapter["title"])}']
    metadata = WORK / 'chapters.ffmeta'
    metadata.write_text('\n'.join(lines) + '\n')
    target = WORK / 'extended-clean.mp4'
    base.run([ffmpeg, '-v', 'warning', '-y', '-f', 'concat', '-safe', '0', '-i', str(concat),
              '-f', 'ffmetadata', '-i', str(metadata), '-map', '0:v:0', '-map', '0:a:0',
              '-map_metadata', '1', '-map_chapters', '1', '-c', 'copy', '-movflags', '+faststart', str(target)])
    base.run([ffmpeg, '-v', 'error', '-xerror', '-i', str(target), '-f', 'null', '-'])
    if aac_bytes(ffmpeg, source) not in aac_bytes(ffmpeg, target):
        raise RuntimeError('The original AAC soundtrack must be retained as an unchanged packet sequence')
    video = ROOT / 'batch-01-video.mp4'
    target.replace(video)
    reader = imageio_ffmpeg.read_frames(str(video))
    info = next(reader)
    reader.close()
    report = {**old_report, 'bytes': video.stat().st_size, 'duration_seconds': info['duration'],
              'source_script_file': script_path.name, 'source_script_sha256': hashlib.sha256(script_path.read_bytes()).hexdigest(),
              'original_narration_sha256': hashlib.sha256((ROOT / 'narration.json').read_bytes()).hexdigest(),
              'original_video_commit': BASE_COMMIT, 'original_aac_sequence_retained': True,
              'opening_duration_seconds': prefix_duration, 'chapters': chapters, 'subtitles': {'burned_in': False},
              'note': 'Six dates/GID opening chapters plus the original ten core chapters. Caption pass is separate.',
              'full_decode_check': 'passed'}
    (ROOT / 'video-build-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(f'Clean dates-first video: {info["duration"]}s; original AAC sequence retained.', flush=True)


if __name__ == '__main__':
    build()
