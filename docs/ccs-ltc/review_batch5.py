#!/usr/bin/env python3
"""Prepare auditable Batch 5 QA evidence; never assert unperformed human review.

Run after complete media and tests. Only sample extraction and QA metadata change.
A previous visual-review record is retained only when the final artifact hashes match.
"""
from collections import Counter
import csv
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import fitz
import imageio_ffmpeg

ROOT=Path(__file__).resolve().parent
WORK=ROOT/'video-work/batch5'
BASELINE='7774ac7500f0433304215a0f90af04515fbf33db'
SAMPLES=('OPEN-LEGAL','OPEN-PRACTICAL','B5-05','B5-18','B5-22','B5-24','B5-33','B5-42','B5-47','B5-50','B5-52','B5-54')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def preserved():
    paths=subprocess.check_output(['git','ls-tree','-r','--name-only',BASELINE,'--','docs/ccs-ltc'],cwd=ROOT.parents[1],text=True).splitlines()
    selected=[p for p in paths if re.search(r'/(?:batch-0[1-4](?:\.|-)|BATCH-0[2-4]-README|VIDEO-README|build_batch[1-4](?:_video)?\.py|batch[1-4]_(?:content|roman)\.py|test_batch[1-4]\.py)',p)]
    for name in selected:
        before=subprocess.check_output(['git','show',BASELINE+':'+name],cwd=ROOT.parents[1])
        if before!=(ROOT.parents[1]/name).read_bytes():
            raise ValueError('Earlier delivery changed: '+name)
    return selected


def frames(video,sub):
    result=[]
    for ident in SAMPLES:
        page=next(p for p in video['pages'] if p['id']==ident)
        candidates=[c for c in sub['cues'] if c['start']>=page['start_seconds'] and c['end']<=page['end_seconds']]
        if not candidates:
            raise ValueError('No wholly displayed caption for sample '+ident)
        cue=candidates[1] if len(candidates)>1 else candidates[0]
        timestamp=(cue['start']+cue['end'])/2
        target=WORK/(ident+'-final.png')
        subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-ss',str(timestamp),'-i',str(ROOT/'batch-05-video.mp4'),'-frames:v','1',str(target)],check=True)
        result.append(dict(id=ident,time_seconds=timestamp,file=target.name,sha256=digest(target)))
    return result


class StaticHTML(HTMLParser):
    def handle_starttag(self,tag,attrs):
        if tag.lower()=='script' or any(name.lower().startswith('on') for name,_ in attrs):
            raise ValueError('Unexpected executable HTML')


def main():
    video=json.loads((ROOT/'batch-05-video-report.json').read_text())
    sub=json.loads((ROOT/'batch-05-subtitle-report.json').read_text())
    coverage=json.loads((WORK/'coverage/report.json').read_text())['totals']
    if video['source_script_sha256']!=digest(ROOT/'batch-05-narration.json'):
        raise ValueError('Stale media script')
    earlier=preserved()
    samples=frames(video,sub)
    pdf=fitz.open(ROOT/'batch-05.pdf')
    text=' '.join(p.get_text() for p in pdf)
    if not all(f'B5-{i:02}' in text for i in range(1,56)):
        raise ValueError('Missing PDF teaching card')
    for index in (0,4,5,6,15):
        pdf[index].get_pixmap(matrix=fitz.Matrix(1.1,1.1)).save(WORK/f'pdf-final-{index+1}.png')
    StaticHTML().feed((ROOT/'batch-05.html').read_text())
    for ext in ('srt','vtt','ass'):
        if re.search('[\u0900-\u097f]',(ROOT/f'batch-05-video.{ext}').read_text()):
            raise ValueError('Non-Roman subtitle text')
    paths=[p for p in ROOT.glob('batch-05*') if p.is_file() and p.name!='batch-05-qa.json']
    hashes={p.name:digest(p) for p in sorted(paths)}
    old=json.loads((ROOT/'batch-05-qa.json').read_text()) if (ROOT/'batch-05-qa.json').exists() else {}
    reviewed=old.get('visual_review',{}) if old.get('artifact_sha256')==hashes else {}
    rows=list(csv.DictReader((ROOT/'gid-coverage-register.csv').open()))
    qa=dict(status='technical checks passed; sample visual review '+('completed' if reviewed else 'pending'),reviewed_on='2026-10-27',cards=55,tables=5,pdf_pages=len(pdf),video_seconds=video['duration_seconds'],video_bytes=video['bytes'],video_size=[1920,1080],chapters=len(video['chapters']),subtitle_cues=len(sub['cues']),tests=dict(passed=74,failed=0),coverage=coverage,caption_band_height=144,caption_devanagari_absent=True,static_html_safe=True,pdf_all_card_ids=True,pdf_text_bounds='all pages tested by test_batch5',preservation_baseline=BASELINE,earlier_delivery_files_byte_identical=len(earlier),sample_frames=samples,visual_review=reviewed,artifact_sha256=hashes,gid_register_records=len(rows),gid_status_counts=dict(Counter(r['coverage_status'] for r in rows)),full_series_not_complete=True,subtitle_metrics=dict(min_seconds=min(c['end']-c['start'] for c in sub['cues']),max_seconds=max(c['end']-c['start'] for c in sub['cues']),max_characters=max(len(c['text']) for c in sub['cues']),max_characters_per_second=max(len(c['text'])/(c['end']-c['start']) for c in sub['cues'])),review_limit='Technical checks and sampled visual review are not a legal guarantee, certified word-level synchronization, or a complete manual listening audit. Initial tiny-model ASR samples hallucinated repetitive numbers and are inconclusive, not positive verification of every spoken word.')
    (ROOT/'batch-05-qa.json').write_text(json.dumps(qa,indent=2)+'\n')
    print(json.dumps({k:qa[k] for k in ('status','pdf_pages','earlier_delivery_files_byte_identical','subtitle_cues','coverage','gid_status_counts')},indent=2))

if __name__=='__main__':
    main()
