#!/usr/bin/env python3
"""Build an offline, cue-by-cue human review page for the finished lecture.

The output embeds the current VTT and binds exported review records to SHA-256
hashes of the MP4 and caption file. It does not certify or alter any captions.
Run after rendering the lecture: python3 build_review.py
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TIME = re.compile(r'^(\d{2,}):(\d{2}):(\d{2})\.(\d{3})$')


def seconds(value: str) -> float:
    m = TIME.fullmatch(value)
    if not m or int(m[2]) > 59 or int(m[3]) > 59:
        raise ValueError(f'Invalid VTT time: {value}')
    h, minute, sec, ms = map(int, m.groups())
    return h * 3600 + minute * 60 + sec + ms / 1000


def parse_vtt(text: str) -> list[dict]:
    blocks = re.split(r'\n\s*\n', text.replace('\r\n', '\n').strip())
    if not blocks or not blocks[0].startswith('WEBVTT'):
        raise ValueError('Missing WEBVTT header')
    result = []
    previous_end = 0.0
    for block in blocks[1:]:
        lines = block.splitlines()
        if not lines or lines[0].startswith(('NOTE', 'STYLE', 'REGION')):
            continue
        timing = next((i for i, line in enumerate(lines) if '-->' in line), None)
        if timing is None:
            raise ValueError('Missing cue timestamp')
        start, end_with_settings = lines[timing].split('-->', 1)
        a, b = seconds(start.strip()), seconds(end_with_settings.strip().split()[0])
        content = ' '.join(line.strip() for line in lines[timing + 1:]).strip()
        if a < previous_end or b <= a or not content:
            raise ValueError('Empty, overlapping, or out-of-order VTT cue')
        result.append({'start': a, 'end': b, 'text': content})
        previous_end = b
    if not result:
        raise ValueError('No cues found')
    return result


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build() -> None:
    video = ROOT / 'Batch-03-Lecture.mp4'
    vtt = ROOT / 'Captions-roman.vtt'
    record = {
        'version': 1,
        'video': video.name,
        'video_sha256': digest(video),
        'caption_file': vtt.name,
        'caption_sha256': digest(vtt),
        'cues': parse_vtt(vtt.read_text(encoding='utf-8')),
    }
    data = json.dumps(record, ensure_ascii=True, separators=(',', ':')).replace('<', '\\u003c')
    page = TEMPLATE.replace('__REVIEW_DATA__', data)
    (ROOT / 'Caption-Review.html').write_text(page, encoding='utf-8')
    print(f"Created Caption-Review.html with {len(record['cues'])} cues")


TEMPLATE = r'''<!doctype html>
<html lang="en-IN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Batch 3 · Human caption review</title>
<style>
:root{color-scheme:dark;--bg:#091121;--panel:#122039;--ink:#f1f6ff;--sub:#c2d1e5;--accent:#4be0bf;--line:#324560;--warning:#ffdf84}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 system-ui,sans-serif}main{max-width:1200px;margin:auto;padding:1.2rem}a{color:#82dfff}h1{line-height:1.15;font-size:clamp(1.8rem,4vw,2.7rem);margin:.5rem 0}h2{margin:.6rem 0}p{max-width:80ch}.eyebrow{color:var(--accent);font-weight:700;letter-spacing:.08em;text-transform:uppercase;font-size:.82rem}.notice,.panel,.cue{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:1rem;margin:1rem 0}.notice{border-left:5px solid var(--warning)}.notice strong{color:var(--warning)}video{width:100%;max-height:55vh;background:#000}.toolbar,.row,.cue-controls{display:flex;flex-wrap:wrap;gap:.6rem;align-items:center}.toolbar{margin:.9rem 0}button,.file-label{cursor:pointer;border:1px solid #4a617d;border-radius:7px;padding:.55rem .8rem;background:#1b3450;color:white;font:inherit}button:hover,.file-label:hover{background:#285078}button:focus-visible,input:focus-visible,textarea:focus-visible,select:focus-visible{outline:3px solid var(--warning);outline-offset:2px}button.primary{background:#126f60;border-color:#3fd4b2}.file-label input{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}input,textarea,select{font:inherit;background:#091628;color:var(--ink);border:1px solid #60748d;border-radius:6px;padding:.45rem}input[type=number]{width:8rem}input[type=checkbox]{width:1.2em;height:1.2em;accent-color:var(--accent)}textarea{width:100%;min-height:3.3rem;resize:vertical}label{font-weight:600}.cue{scroll-margin-top:1rem}.cue h3{margin:0}.cue.original{color:var(--sub)}.original{color:var(--sub);font-size:.9rem;overflow-wrap:anywhere}.caption-label{display:block;margin:.6rem 0 .25rem}.review-check{display:flex;gap:.5rem;align-items:center}.status{color:var(--accent);font-weight:700}.muted{color:var(--sub);font-size:.9rem}.cue[data-reviewed=true]{border-color:#3c977f}progress{width:min(100%,360px);height:1rem}#message{min-height:1.5em;color:var(--warning)}@media(max-width:600px){main{padding:.75rem}input[type=number]{width:6.8rem}.toolbar>*{max-width:100%}}
</style></head><body><main>
<a href="Batch-03-Guide.html">← Back to the companion guide</a>
<p class="eyebrow">Batch 03 / cue-by-cue listening</p><h1>Human caption review</h1>
<div class="notice"><strong>Not yet human-verified.</strong> These cues are automatic transliterations of a best-effort alignment text, which differs from the original synthesis input in sections 04 and 06. A person must listen to every cue before calling the recording verbatim-verified. Check names, numbers, words and timing; forced alignment and speech recognition can be wrong. The English subtitles are a separate translation and are not being certified here.</div>
<section class="panel" aria-labelledby="player-title"><h2 id="player-title">1. Listen and compare</h2>
<p>Use headphones, play each segment and compare it with the Roman-Hinglish text. Correct the words and timestamps if needed, then tick that cue only after you have listened. The original subtitle is burned into the video and cannot change in this player.</p>
<video id="player" controls preload="metadata" src="Batch-03-Lecture.mp4" aria-label="Batch 3 lecture for caption review"></video>
<div class="toolbar"><label for="speed">Playback speed</label><select id="speed"><option value="0.75">0.75×</option><option value="1" selected>1×</option><option value="1.25">1.25×</option></select><button id="play-all" type="button">Play full lecture</button><button id="pause" type="button">Pause</button></div>
<p class="muted">Each cue's Play button starts slightly before its proposed start and pauses just after its proposed end. Times are seconds from the beginning of the video. Boundary playback is approximate.</p>
</section>
<section class="panel" aria-labelledby="review-title"><h2 id="review-title">2. Record the review</h2>
<p>Review status is stored in this browser when available. Export a backup before closing or switching devices. A tick is a reviewer's assertion, not automatic proof of accuracy.</p>
<label for="reviewer">Reviewer name or initials (optional)</label> <input id="reviewer" type="text" maxlength="120" autocomplete="name"><br>
<p><span id="count" class="status" aria-live="polite">0 reviewed</span><br><progress id="progress" value="0" max="1" aria-label="Cue review progress"></progress></p>
<div class="toolbar"><button class="primary" id="export" type="button">Export review JSON</button><button id="export-vtt" type="button">Export corrected Roman VTT</button><label class="file-label">Import review JSON<input id="import" type="file" accept="application/json,.json"></label><button id="reset" type="button">Reset local review</button></div>
<p class="muted">The JSON is tied to this video's and VTT's SHA-256 hashes. Send it back if you want approved corrections incorporated into a new video. Exported VTT is a draft until all cues are actually checked; it does not replace burned-in subtitles or automatically update the English translation.</p><p id="message" role="status"></p>
</section>
<section aria-labelledby="cues-title"><h2 id="cues-title">3. Review every cue</h2><div id="cues"></div></section>
</main><script>
'use strict';
const source=__REVIEW_DATA__;
const key='ccs-ta-review-v1-'+source.video_sha256+'-'+source.caption_sha256;
const video=document.querySelector('#player'),list=document.querySelector('#cues'),message=document.querySelector('#message');
const progress=document.querySelector('#progress'),count=document.querySelector('#count'),reviewer=document.querySelector('#reviewer');
let stopAt=null;
const initial=()=>({reviewer:'',cues:source.cues.map((c,i)=>({index:i+1,start:c.start,end:c.end,text:c.text,reviewed:false,notes:''}))});
let state=initial();
try { const saved=localStorage.getItem(key); if(saved) {const value=JSON.parse(saved); if(value.cues&&value.cues.length===source.cues.length) state=value;} }
catch(e){message.textContent='Browser storage is unavailable. Export your review before leaving this page.';}
function save(){try{localStorage.setItem(key,JSON.stringify(state));}catch(e){message.textContent='Browser storage is unavailable. Export your review before leaving this page.';} updateProgress();}
function updateProgress(){const done=state.cues.filter(c=>c.reviewed).length;progress.max=state.cues.length;progress.value=done;count.textContent=done+' / '+state.cues.length+' cues marked reviewed';}
function make(tag,attrs={},text=''){const el=document.createElement(tag);for(const [k,v] of Object.entries(attrs))el.setAttribute(k,v);el.textContent=text;return el;}
function render(){
  reviewer.value=state.reviewer||'';list.replaceChildren();
  source.cues.forEach((original,i)=>{
    const c=state.cues[i],card=make('article',{class:'cue','data-reviewed':String(!!c.reviewed)}),id='cue-'+(i+1);card.id=id;
    card.append(make('h3',{},'Cue '+(i+1)),make('p',{class:'original'},'Original '+original.start.toFixed(3)+'–'+original.end.toFixed(3)+' s: '+original.text));
    const controls=make('div',{class:'cue-controls'}),play=make('button',{type:'button'},'Play cue '+(i+1));
    const sl=make('label',{for:id+'-start'},'Start (s)'),start=make('input',{id:id+'-start',type:'number',min:'0',step:'0.001'});start.value=c.start;
    const el=make('label',{for:id+'-end'},'End (s)'),end=make('input',{id:id+'-end',type:'number',min:'0',step:'0.001'});end.value=c.end;
    controls.append(play,sl,start,el,end);card.append(controls);
    const textlabel=make('label',{class:'caption-label',for:id+'-text'},'Heard Roman-Hinglish wording'),text=make('textarea',{id:id+'-text',rows:'2'});text.value=c.text;card.append(textlabel,text);
    const noteslabel=make('label',{class:'caption-label',for:id+'-notes'},'Notes (optional)'),notes=make('input',{id:id+'-notes',type:'text',maxlength:'300'});notes.value=c.notes||'';card.append(noteslabel,notes);
    const checkLabel=make('label',{class:'review-check',for:id+'-reviewed'}),check=make('input',{id:id+'-reviewed',type:'checkbox'});check.checked=!!c.reviewed;checkLabel.append(check,document.createTextNode('I listened and checked this cue’s wording and timing.'));card.append(checkLabel);
    const edit=()=>{c.start=start.value===''?null:Number(start.value);c.end=end.value===''?null:Number(end.value);c.text=text.value;c.notes=notes.value;c.reviewed=false;check.checked=false;card.dataset.reviewed='false';save();};
    [start,end,text,notes].forEach(e=>e.addEventListener('input',edit));
    check.addEventListener('change',()=>{c.reviewed=check.checked;card.dataset.reviewed=String(c.reviewed);save();});
    play.addEventListener('click',()=>{if(!Number.isFinite(c.start)||!Number.isFinite(c.end)||c.start<0||c.end<=c.start){message.textContent='Correct this cue’s start and end before playback.';return;}message.textContent='';stopAt=c.end+.15;video.currentTime=Math.max(0,c.start-.15);video.play().catch(()=>{message.textContent='Press Play on the video to start playback.';});});
    list.append(card);
  });updateProgress();
}
function valid(){
 let prior=0;for(let i=0;i<state.cues.length;i++){const c=state.cues[i];if(!Number.isFinite(c.start)||!Number.isFinite(c.end)||c.start<prior||c.end<=c.start||(Number.isFinite(video.duration)&&c.end>video.duration+.05)||!c.text.trim()||/[\u0900-\u097f]/.test(c.text)||c.text.includes('-->')) return i+1;prior=c.end;}return 0;
}
function download(name,type,content){const blob=new Blob([content],{type}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
function stamp(t){let ms=Math.round(t*1000),h=Math.floor(ms/3600000);ms-=h*3600000;let m=Math.floor(ms/60000);ms-=m*60000;let s=Math.floor(ms/1000);ms-=s*1000;return String(h).padStart(2,'0')+':'+String(m).padStart(2,'0')+':'+String(s).padStart(2,'0')+'.'+String(ms).padStart(3,'0');}
reviewer.addEventListener('input',()=>{state.reviewer=reviewer.value;save();});
document.querySelector('#speed').addEventListener('change',e=>video.playbackRate=Number(e.target.value));
document.querySelector('#play-all').addEventListener('click',()=>{stopAt=null;video.play().catch(()=>{message.textContent='Press Play on the video to start playback.';});});
document.querySelector('#pause').addEventListener('click',()=>{stopAt=null;video.pause();});
video.addEventListener('timeupdate',()=>{if(stopAt!==null&&video.currentTime>=stopAt){video.pause();stopAt=null;}});
document.querySelector('#export').addEventListener('click',()=>{const bad=valid();if(bad){message.textContent='Check time, ordering and Roman text in cue '+bad+' before export.';return;}const payload={format:'ccs-ta-caption-review-v1',video:source.video,video_sha256:source.video_sha256,caption_file:source.caption_file,caption_sha256:source.caption_sha256,exported_at:new Date().toISOString(),reviewer:state.reviewer||'',reviewed_count:state.cues.filter(c=>c.reviewed).length,total:state.cues.length,cues:state.cues};download('Batch-03-Caption-Review.json','application/json',JSON.stringify(payload,null,2)+'\n');message.textContent='Review exported. A tick reflects the reviewer’s own check.';});
document.querySelector('#export-vtt').addEventListener('click',()=>{const bad=valid();if(bad){message.textContent='Check time, ordering and Roman text in cue '+bad+' before export.';return;}let out='WEBVTT\n\nNOTE Reviewer-edited draft. Review status is recorded separately in the exported JSON.\n\n';state.cues.forEach((c,i)=>{out+=(i+1)+'\n'+stamp(c.start)+' --> '+stamp(c.end)+'\n'+c.text.replace(/\r?\n/g,' ')+'\n\n';});download('Batch-03-Captions-Reviewed-Draft.vtt','text/vtt',out);message.textContent='Draft VTT exported; the video has not been changed.';});
document.querySelector('#import').addEventListener('change',async e=>{try{const file=e.target.files[0];if(!file)return;const p=JSON.parse(await file.text());if(p.format!=='ccs-ta-caption-review-v1'||p.video_sha256!==source.video_sha256||p.caption_sha256!==source.caption_sha256||!Array.isArray(p.cues)||p.cues.length!==source.cues.length)throw Error('This review belongs to different source files.');for(let i=0;i<p.cues.length;i++){const c=p.cues[i];if(c.index!==i+1||!Number.isFinite(c.start)||!Number.isFinite(c.end)||typeof c.text!=='string'||typeof c.reviewed!=='boolean'||typeof(c.notes||'')!=='string')throw Error('Invalid cue in review file.');}const old=state;state={reviewer:typeof p.reviewer==='string'?p.reviewer:'',cues:p.cues.map(c=>({index:c.index,start:c.start,end:c.end,text:c.text,reviewed:c.reviewed,notes:c.notes||''}))};const bad=valid();if(bad){state=old;throw Error('Invalid time or text in cue '+bad+'.');}save();render();message.textContent='Matching review imported.';}catch(err){message.textContent='Import failed: '+err.message;}finally{e.target.value='';}});
document.querySelector('#reset').addEventListener('click',()=>{if(!confirm('Delete this browser’s local review? Export a backup first.'))return;state=initial();save();render();message.textContent='Local review reset.';});
render();
</script></body></html>'''

if __name__ == '__main__':
    build()
