#!/usr/bin/env python3
"""Recreate chapter 04's edited narration from the two saved voice-00 clips.

The original chapter 04 opening contained a numerically written 2023, which
was recognized ambiguously as "2030s" in one ASR pass. The replacement opening
is the same speaker's spoken-out 2023 sentence from chapter 06. This edit is
not a human listening certification. Re-run caption alignment after rebuilding;
existing hashes deliberately reject changed audio. Requires imageio-ffmpeg or
FFMPEG_BIN. Inputs and the original are preserved in audio/.
"""
from pathlib import Path
import os
import subprocess
from build_batch_02 import ffmpeg_path

ROOT = Path(__file__).resolve().parent
original = ROOT / 'audio/source-04-original.mp3'
speaker = ROOT / 'audio/06-foreign-conveyance.mp3'
target = ROOT / 'audio/04-foreign-da-slabs.mp3'
temporary = ROOT / 'audio/.04-foreign-da-slabs-assembling.mp3'
command = [ffmpeg_path(), '-hide_banner', '-loglevel', 'error', '-y',
           '-i', str(speaker), '-i', str(original),
           '-filter_complex', '[0:a]atrim=start=23.70:end=27.70,asetpts=PTS-STARTPTS[a];'
                              '[1:a]atrim=start=5.45,asetpts=PTS-STARTPTS[b];'
                              '[a][b]concat=n=2:v=0:a=1[out]',
           '-map', '[out]', '-ar', '24000', '-ac', '1', '-codec:a', 'libmp3lame',
           '-b:a', '96k', str(temporary)]
try:
    subprocess.run(command, check=True)
    os.replace(temporary, target)
finally:
    temporary.unlink(missing_ok=True)
print('Chapter 04 assembled. Regenerate and review caption alignment before rendering.')
