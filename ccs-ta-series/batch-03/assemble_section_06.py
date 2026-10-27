#!/usr/bin/env python3
"""Rebuild an edit of section 06 from its preserved original voice clip.

ASR detected a possible erroneous first percentage in the local-journey list.
Rather than assert uncertain numbers in speech, the edit removes the whole
spoken percentage-list sentence. The slide and guide show the complete 15/35/50% list, explicitly marked
provisional. The audio edit and remaining captions still require human review.
Re-run alignment, render and review after changing the audio.
"""
from pathlib import Path
import os,subprocess,tempfile
from build_batch_03 import HERE,ffmpeg_path

original=HERE/'audio'/'source-06-original.mp3'
out=HERE/'audio'/'06-local-journeys.mp3'
ff=ffmpeg_path()
with tempfile.TemporaryDirectory(prefix='batch03-edit-') as temp:
 target=Path(temp)/'out.mp3'
 filt=("[0:a]atrim=start=0:end=15.55,asetpts=PTS-STARTPTS[a];"
       "[0:a]atrim=start=20.22,asetpts=PTS-STARTPTS[b];"
       "[a][b]concat=n=2:v=0:a=1[out]")
 subprocess.run([ff,'-v','error','-i',str(original),'-filter_complex',filt,
                 '-map','[out]','-ar','24000','-ac','1','-codec:a','libmp3lame',
                 '-b:a','96k','-y',str(target)],check=True)
 os.replace(target,out)
 print('Rebuilt',out)
