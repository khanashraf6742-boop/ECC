// Phase 2/3 builder (CommonJS). Verbatim extraction + study aids → work/ch-*.html fragments → TA_Rules_Study_Guide.html
const fs=require('fs'),path=require('path');
const {build,strip}=require('./classify');
const TABLES=require('./tables'),SVGS=require('./svgs');
const OFF=require('./official'),OFF2=require('./official2'),EXTRA=require('./extra'),META=require('./meta'),LTC=require('./ltc'),FRSR=require('./frsr');
const OUT=path.join(__dirname,'..','TA_Rules_Study_Guide.html');
const esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
const data=build();
const FRAG={front:'ch-00-front',p2:'ch-part-ii',pack:'ao-pack',tk:'addendum',apA:'ap-a',apB:'ap-b',apC:'ap-c',apD:'ap-d'};
const fragName=k=>FRAG[k]||k.replace(/^ch(\d+)$/,'ch-$1');
const aidOf=k=>{try{return require('./aids/'+k)}catch(e){return {quick:{},hooks:{},mcqs:[],cards:[]}}};
const SECID=k=>'sec-'+k;
// ---------- cleaning ----------
function clean(h,type){
  h=h.replace(/\sstyle="[^"]*"/g,'').replace(/\sstyle='[^']*'/g,'');
  if(type==='cover'||type==='part-ii-update')h=h.replace(/<h2\b/g,'<h3').replace(/<\/h2>/g,'</h3>');
  h=h.replace(/<h1\b/g,'<h2').replace(/<\/h1>/g,'</h2>');
  h=h.replace(/<a class="back-top"[^>]*>[^<]*<\/a>/g,'');
  h=h.replace(/<div class="simple"><span class="lbl">/g,'<div class="simple"><span class="lbl" role="button" tabindex="0" aria-expanded="false">');
  h=h.replace(/target="_blank"/g,'target="_blank" rel="noopener noreferrer"');
  h=h.replace(/<table\b/g,'<div class="tablewrap" tabindex="0" role="region" aria-label="Table (scrollable)"><table').replace(/<\/table>/g,'</table></div>');
  return h;
}
// ---------- cross references ----------
const DATEMAP={'13.07.2017':'ch01-004','04.09.2017':'ch07-006','14.09.2017':'ch07-007','01.02.2018':'ch07-008','13.03.2018':'ch07-009','15.06.2021':'ch07-009','29.06.2018':'ch07-010','23.06.2020':'ch07-011','22.12.2020':'ch07-012','06.01.2022':'ch07-013','24.01.2022':'ch07-014','16.06.2022':'ch07-015','12.09.2022':'ch07-016','31.12.2021':'ch07-017','16.02.2022':'ch07-017','19.09.2017':'ch07-018','31.07.2018':'ch07-018'};
const APP={A:'flash',B:'drill',C:'index',D:'appendix-d'};
const XR={}; // sr key -> {label, cites:[{id,head}]}
function autolink(html,p,collect){
  const seen=new Set();let inA=0,inH=0;
  return html.split(/(<[^>]+>)/).map(t=>{
    if(t[0]==='<'){if(/^<a\b/i.test(t))inA++;else if(/^<\/a>/i.test(t))inA--;if(/^<(h[1-6]|summary)\b/i.test(t))inH++;else if(/^<\/(h[1-6]|summary)>/i.test(t))inH--;return t;}
    if(inA>0||inH>0||!t.trim())return t;
    t=t.replace(/\b(Chapters?)((?:\s|&nbsp;)+)(\d{1,2})(?!\d)/g,(m,a,b,n)=>{n=+n;if(n<1||n>17||seen.has('c'+n+p.id))return m;seen.add('c'+n+p.id);return `<a class="xref" href="#ch${n}">${m}</a>`;});
    t=t.replace(/\bCh\.?((?:\s|&nbsp;)+)(\d{1,2})\b/g,(m,b,n)=>{n=+n;if(n<1||n>17||seen.has('c'+n+p.id))return m;seen.add('c'+n+p.id);return `<a class="xref" href="#ch${n}">${m}</a>`;});
    t=t.replace(/\bAppendix((?:\s|&nbsp;)+)([A-D])\b(?!\s*[–-]\s*D)/g,(m,b,l)=>{const k='a'+l+p.id;if(seen.has(k))return m;seen.add(k);return `<a class="xref" href="#${APP[l]}">${m}</a>`;});
    t=t.replace(/\bSR((?:\s|&nbsp;)+)(\d{1,3})(?:-([A-Z]))?\b(?![–\-]\d)/g,(m,s,n,l)=>{const key='sr-'+n+(l?'-'+l.toLowerCase():'');
      if(collect){const e=XR[key]||(XR[key]={label:'SR '+n+(l?'-'+l:''),cites:[],n:+n});if(!e.cites.some(c=>c.id===p.id))e.cites.push({id:p.id,head:p.head||p.type,seg:p.seg});return m;}
      if(!XR[key]||seen.has(key))return m;seen.add(key);return `<a class="xref" href="#xref-${key}">${m}</a>`;});
    t=t.replace(/\b(\d{2}\.\d{2}\.\d{4})\b/g,(m,d)=>{const tgt=DATEMAP[d];if(!tgt||tgt===p.id||collect||seen.has('d'+d))return m;seen.add('d'+d);return `<a class="xref" href="#${tgt}" title="Jump to the card for the O.M. dated ${d}">${m}</a>`;});
    return t;
  }).join('');
}
// ---------- element-type tagging (keyword heuristic; shown as auto-tags) ----------
const RX={proviso:/\bprovided\b|\bproviso\b|\bsubject to\b|\bonly if\b|\bonly when\b|\bonly where\b|\bunless\b|\bon condition\b|\bconditional(ly)?\b/i,
 exception:/\bexception(s)?\b|\bexcept\b|\bexclusion(s)?\b|\bexcluded\b|\bdoes not apply\b|\bnot applicable\b|\bnot admissible\b|\bnot payable\b|\bnot entitled\b|\bineligible\b|\bforfeit/i};
function tagInner(html){
  const tag=(re,open)=>html=html.replace(re,(m,attrs,body)=>{const s=strip(body);const t=[];if(RX.proviso.test(s))t.push('proviso');if(RX.exception.test(s))t.push('exception');if(!t.length)return m;return `<${open}${attrs} data-t="${t.join(' ')}" data-tl="${t.join(' + ')}">${body}`;});
  html=html.replace(/<li\b([^>]*)>([\s\S]*?)(?=<\/li>|<li\b|<\/ul>)/g,(m,a,b)=>{const s=strip(b);const t=[];if(RX.proviso.test(s))t.push('proviso');if(RX.exception.test(s))t.push('exception');return t.length?`<li${a} data-t="${t.join(' ')}" data-tl="${t.join(' + ')}">${b}`:m;});
  html=html.replace(/<tr\b([^>]*)>([\s\S]*?)<\/tr>/g,(m,a,b)=>{const s=strip(b);const t=[];if(RX.proviso.test(s))t.push('proviso');if(RX.exception.test(s))t.push('exception');return t.length?`<tr${a} data-t="${t.join(' ')}" data-tl="${t.join(' + ')}">${b}</tr>`:m;});
  html=html.replace(/<p\b([^>]*)>([\s\S]*?)(?=<\/p>)/g,(m,a,b)=>{if(/data-t=/.test(a))return m;const s=strip(b);const t=[];if(RX.proviso.test(s))t.push('proviso');if(RX.exception.test(s))t.push('exception');return t.length?`<p${a} data-t="${t.join(' ')}" data-tl="${t.join(' + ')}">${b}`:m;});
  return html;
}
function typesOf(p,src){
  const s=strip(src),T=new Set();const h=p.head+' '+(/<span class="lbl">([\s\S]*?)<\/span>/.exec(src)||['',''])[1];
  if(/\bO\.M\.|\bOM\b|Office Memorandum/.test(h)||(s.match(/O\.M\./g)||[]).length>=4)T.add('om');
  if(/\b(order|orders)\b(?!\s+to)|G\.S\.R\.|Gazette|Circular/i.test(h)||(s.match(/\b(order|orders)\b(?!\s+to)/gi)||[]).length>=4||/G\.S\.R\./.test(s))T.add('order');
  if(p.type==='faq'||p.seg==='ch17'||/\bFAQ/.test(h))T.add('faq');
  if(RX.proviso.test(s)&&/data-t="[^"]*proviso/.test(tagInner(src)))T.add('proviso');
  if(/data-t="[^"]*exception/.test(tagInner(src))||/class="trapx"/.test(src))T.add('exception');
  if(/class="(simple|analogy|comparison-note)"/.test(src))T.add('explanation');
  return [...T];
}
const TL={proviso:'Proviso',exception:'Exception',om:'O.M.',order:'Order',faq:'FAQ',explanation:'Explanation'};
// ---------- SVG ----------
function wrap(t,n){const w=t.split(/\s+/);const L=[];let c='';w.forEach(x=>{if((c+' '+x).trim().length>n){L.push(c);c=x}else c=(c+' '+x).trim()});if(c)L.push(c);return L}
function svg(s){const W=360,pad=10,LH=17,boxes=[];let y=8;
  s.steps.forEach(st=>{const tl=wrap(st[0],44),bl=wrap(st[1],50);const h=pad*2+(tl.length+bl.length)*LH;boxes.push({y,h,tl,bl});y+=h+26});
  const H=y-18;let o=`<svg class="flow" viewBox="0 0 ${W} ${H}" role="img" aria-labelledby="${s.id}-t ${s.id}-d"><title id="${s.id}-t">${esc(s.title)}</title><desc id="${s.id}-d">${esc(s.steps.map(x=>x[0]+': '+x[1]).join(' → '))}</desc>`;
  boxes.forEach((b,i)=>{o+=`<rect x="4" y="${b.y}" width="${W-8}" height="${b.h}" rx="9"/>`;let ty=b.y+pad+12;b.tl.forEach(l=>{o+=`<text class="t" x="14" y="${ty}">${esc(l)}</text>`;ty+=LH});b.bl.forEach(l=>{o+=`<text x="14" y="${ty}">${esc(l)}</text>`;ty+=LH});
    if(i<boxes.length-1){const ay=b.y+b.h;o+=`<path d="M${W/2} ${ay} V${ay+18}"/><polygon points="${W/2-5},${ay+16} ${W/2+5},${ay+16} ${W/2},${ay+24}"/>`}});
  return o+'</svg>';}
function svgBlock(s){return `<figure class="study-aid" id="${s.id}" data-chrome="1"><span class="aid-label">Study aid · Flowchart derived from the source text (not source text itself)</span><figcaption><b>${esc(s.title)}</b> — source: ${esc(s.cite)}</figcaption>${svg(s)}<details><summary>Text alternative</summary><ol>${s.steps.map(x=>`<li><b>${esc(x[0])}.</b> ${esc(x[1])}</li>`).join('')}</ol></details></figure>`}
// ---------- superseded passages (collapsed, never deleted) ----------
const SUPERSEDED=[
 ['Under the base O.M. dated 13.07.2017, retired employees settling','Superseded by DoE O.M. 06.01.2022 (retirement CTG: 20-km condition removed)'],
 ['The 25% Flat DA Abolition: Under 5th','Superseded by DoE O.M. 01.02.2018 (flat 25% DA discontinued)'],
 ['Purana rule (6th CPC): Pehle agar stay aur food dono free','Superseded by DoE O.M. 01.02.2018 (flat 25% DA discontinued)'],
 ['16.02.2022No. 19024/03/2021-E.IVEarlier best-available-fare','Superseded by DoE O.M. 16.06.2022 para 16 (supersedes all earlier air instructions); content also mis-described — see E6'],
 ['2. DoE O.M. of even number dated 16.02.2022 (Guidelines on Best Available Fare)','Superseded by DoE O.M. 16.06.2022 para 16; the 16.02.2022 O.M. itself only allowed private airlines — see E6']];
const supStats=[];
function markSup(html){
  const one=(m,open,a,b)=>{const t=strip(b).replace(/\s+/g,'');const e=SUPERSEDED.find(x=>t.startsWith(x[0].replace(/\s+/g,'')));if(!e)return null;supStats.push(e[1]);const cls=/class="/.test(a)?a.replace(/class="/,'class="sup '):a+' class="sup"';return `<${open}${cls} data-sup="${esc(e[1])}">`;};
  html=html.replace(/<li\b([^>]*)>([\s\S]*?)(?=<\/li>|<li\b|<\/ul>)/g,(m,a,b)=>{const r=one(m,'li',a,b);return r?r+b:m});
  html=html.replace(/<tr\b([^>]*)>([\s\S]*?)<\/tr>/g,(m,a,b)=>{const r=one(m,'tr',a,b);return r?r+b+'</tr>':m});
  html=html.replace(/<p\b([^>]*)>([\s\S]*?)(?=<\/p>)/g,(m,a,b)=>{const r=one(m,'p',a,b);return r?r+b:m});
  return html;
}
// ---------- render ----------
const LABEL={micronote:'Micro-note',verdict:'Source verdict / note',worked:'Worked example',flag:'Flag',faq:'FAQ','case-box':'Case',text:'Note',aside:'Provenance note',title:'Module title',other:'Block',cover:'Cover',mfs:'Fact-sheet',review:'Review','study-hub':'Study hub','part-ii-update':'Targeted update',recap:'Recap',card:'Card',section:'Section','section-el':'Section',flag2:'Flag'};
const STRUCT=new Set(['anchor','chapter-banner','study-map','comment']);
const allIdx=[],deck={cards:[],mcqs:[]};
function renderPiece(seg,p,aid,collect){
  p.seg=seg.key;
  if(p.type==='comment')return '';
  let html=clean(p.html,p.type);
  if(STRUCT.has(p.type))return html;
  // heading → summary
  let hd='',body=html;const hm=/^\s*(?:<[^>]+>\s*){0,2}?(<(h[1-4])\b[^>]*>[\s\S]*?<\/\2>)/.exec(html);
  if(hm&&html.indexOf(hm[1])<260){hd=hm[1].replace(/^<h[1-4]/,'<h3').replace(/<\/h[1-4]>$/,'</h3>');body=html.replace(hm[1],'');}
  const types=typesOf(p,html);
  const sl=`L${p.l1}–${p.l2}`;
  const label=hd?'':`<span class="chrome" data-chrome="1"><b>${esc(LABEL[p.type]||'Block')}</b> <span class="secmeta">— ${esc(strip(html).slice(0,80))}…</span></span>`;
  if(!collect)allIdx.push({seg:seg.key,id:p.id,head:p.head,type:p.type,sl});
  let inner=autolink(markSup(tagInner(body)),p,collect);
  const nSup=(inner.match(/class="sup\b|class="sup /g)||[]).length;
  const badges=types.map(t=>`<span class="tb tb-${t}" data-chrome="1" title="Automatic keyword tag">${TL[t]}</span>`).join('');
  const q=aid.quick[p.id],hk=aid.hooks[p.id];
  let aids='';
  if(q)aids+=`<div class="study-aid quick${/\[uncertain/.test(q)?' unc':''}" data-chrome="1"><span class="aid-label">Study aid · Quick revision (not source text)</span><p>${esc(q)}</p></div>`;
  if(hk)aids+=`<div class="study-aid aidhook" data-chrome="1"><span class="aid-label">Study aid · Memory hook</span><p>${esc(hk)}</p></div>`;
  if(OFF2.checks[p.id])aids+=`<div class="study-aid offcheck" data-chrome="1"><span class="aid-label">Official-text check · read from the official PDF on 26.11.2026</span><p>${esc(OFF2.checks[p.id])}</p></div>`;
  SVGS.filter(s=>s.after===p.id).forEach(s=>aids+=svgBlock(s));
  return `<details class="rule" id="${p.id}" data-types="${types.join(' ')}" data-sl="${sl}" open><summary><span class="rno" data-chrome="1">${p.id}</span>${hd||label}${badges}</summary><div class="rbody"><div class="rtools" data-chrome="1"><span>Source ${sl}</span>${nSup?`<span class="tb tb-exception">${nSup} superseded line${nSup>1?'s':''} hidden — use “Show superseded”</span>`:''}<label><input type="checkbox" class="rv" aria-label="Mark ${p.id} as reviewed"> Reviewed</label></div><div class="verbatim" data-src="${sl}">${inner}</div>${aids}</div></details>`;
}
function aidsSection(seg,aid){
  const tabs=TABLES.filter(t=>t.seg===seg.key);if(!tabs.length&&!aid.mcqs.length&&!aid.cards.length)return '';
  let h=`<div class="aidsec noprint-no" id="aids-${seg.key}"><h3>Study aids — ${esc(seg.title)}</h3><p class="secmeta">Everything in this box is the study guide’s own layer: it is derived from the verbatim text above and is not source text.</p>`;
  tabs.forEach(t=>{h+=`<div class="study-aid" data-chrome="1"><span class="aid-label">Study aid · Comparison table</span><div class="tablewrap" tabindex="0" role="region" aria-label="${esc(t.title)}"><table><caption>${esc(t.title)} <small>— source: ${esc(t.cite)}</small></caption><thead><tr>${t.head.map(c=>`<th scope="col">${esc(c)}</th>`).join('')}</tr></thead><tbody>${t.rows.map(r=>`<tr>${r.map((c,i)=>i?`<td>${esc(c)}</td>`:`<th scope="row">${esc(c)}</th>`).join('')}</tr>`).join('')}</tbody></table></div></div>`});
  if(aid.mcqs.length){h+=`<div class="study-aid" data-chrome="1"><span class="aid-label">Study aid · Practice MCQs (written for this guide; answers cite the source card)</span>`;
    aid.mcqs.forEach((m,i)=>{h+=`<details class="mcq"><summary>Q${i+1}. ${esc(m.q)}</summary><ol type="a">${m.o.map(o=>`<li>${esc(o)}</li>`).join('')}</ol><p><b>Answer: (${String.fromCharCode(97+m.a)})</b> ${esc(m.o[m.a])} — ${esc(m.why)} <small>Rule citation: ${esc(m.c)}</small></p></details>`;deck.mcqs.push({seg:seg.key,segt:seg.title,q:m.q,o:m.o,a:m.a,w:m.why,c:m.c})});h+='</div>'}
  if(aid.cards.length){h+=`<div class="study-aid" data-chrome="1"><span class="aid-label">Study aid · Flashcards (click the front to reveal the back)</span>`;
    aid.cards.forEach(c=>{h+=`<div class="fc"><button class="fcflip btn" aria-expanded="false">${esc(c.f)}</button><div class="fcback" hidden>${esc(c.b)} <small>Source: ${esc(c.c)}</small></div></div>`;deck.cards.push({seg:seg.key,segt:seg.title,f:c.f,b:c.b,c:c.c})});h+='</div>'}
  return h+'</div>';
}
// pass 1: collect SR xrefs
data.forEach(seg=>{const aid=aidOf(seg.key);seg.pieces.forEach(p=>renderPiece(seg,p,aid,true))});
allIdx.length=0;
// pass 2
const frags={};
data.forEach(seg=>{const aid=aidOf(seg.key);let h=`<section class="chapter" id="${SECID(seg.key)}" aria-labelledby="${SECID(seg.key)}-h"><h2 id="${SECID(seg.key)}-h" class="secmeta" style="margin:0">${esc(seg.title)} <small>· source lines ${seg.l1}–${seg.l2}</small></h2>`;
  seg.pieces.forEach(p=>{h+=renderPiece(seg,p,aid,false)+'\n'});h+=aidsSection(seg,aid)+'</section>';
  h=h.replace(/<h2 id="[^"]*-h" class="secmeta" style="margin:0">/,m=>m.replace(' style="margin:0"',''));
  fs.writeFileSync(path.join(__dirname,fragName(seg.key)+'.html'),h);frags[seg.key]=h});
// ---------- official verification chapter ----------
const offIdx=[];
function offRule(id,title,types,cite,body){offIdx.push({seg:'off',id,head:title,type:'card',sl:cite});return `<details class="rule" id="${id}" data-types="${types.join(' ')}" data-sl="official" open><summary><span class="rno" data-chrome="1">${id}</span><h3>${esc(title)}</h3>${types.map(t=>`<span class="tb tb-${t}" data-chrome="1">${TL[t]}</span>`).join('')}</summary><div class="rbody"><div class="rtools" data-chrome="1"><span>Source: ${esc(cite)}</span><label><input type="checkbox" class="rv" aria-label="Mark ${id} as reviewed"> Reviewed</label></div><div class="study-aid offcheck" data-chrome="1"><span class="aid-label">Official-text layer — not part of the original study guide</span>${body}</div></div></details>`}
function tblHtml(t){return `<div class="tablewrap" tabindex="0" role="region" aria-label="${esc(t.title)}"><table><caption>${esc(t.title)} <small>— source: ${esc(t.cite)}</small></caption><thead><tr>${t.head.map(c=>`<th scope="col">${esc(c)}</th>`).join('')}</tr></thead><tbody>${t.rows.map(r=>`<tr>${r.map((c,i)=>i?`<td>${esc(c)}</td>`:`<th scope="row">${esc(c)}</th>`).join('')}</tr>`).join('')}</tbody></table></div>`}
let offHtml=`<section class="chapter" id="sec-official" aria-labelledby="off-h"><h2 id="off-h">Official verification — read first (checked 26 November 2026)</h2>
<p>This chapter was added after the guide’s source text was converted. I downloaded the official orders from the Government hosts the source cites, read them (text layer or page images) and compared them with the guide. <b>The original source text elsewhere in this file is unchanged.</b> Where an official text differs from it, the affected card carries an amber <i>Official-text check</i> box that points to the errata below.</p>
<details class="rule" id="off-reg" data-types="om order" data-sl="official" open><summary><span class="rno" data-chrome="1">off-reg</span><h3>Evidence register — what was read</h3><span class="tb tb-om" data-chrome="1">O.M.s</span></summary><div class="rbody"><div class="rtools" data-chrome="1"><span>Official verification</span><label><input type="checkbox" class="rv" aria-label="Mark off-reg as reviewed"> Reviewed</label></div><div class="tablewrap" tabindex="0" role="region" aria-label="Evidence register"><table><thead><tr><th scope="col">Instrument</th><th scope="col">Official file</th><th scope="col">How read</th><th scope="col">Result</th></tr></thead><tbody>${OFF.REG.map(r=>`<tr><td>${esc(r[0])}</td><td><a href="${esc(r[1])}" target="_blank" rel="noopener noreferrer">${esc(r[1].replace(/^https:\/\//,'').slice(0,70))}</a></td><td>${esc(r[2])}</td><td>${esc(r[3])}</td></tr>`).join('')}</tbody></table></div><div class="study-aid unc" data-chrome="1"><span class="aid-label">Not retrieved — stays [uncertain]</span><ul>${OFF.NOT.map(n=>`<li>${esc(n)}</li>`).join('')}</ul></div></div></details>`;
offIdx.push({seg:'off',id:'off-reg',head:'Evidence register — what was read',type:'card',sl:'official'});
offHtml+=`<details class="rule" id="off-err" data-types="exception proviso om" data-sl="official" open><summary><span class="rno" data-chrome="1">off-err</span><h3>Errata — where the guide and the official text differ</h3><span class="tb tb-exception" data-chrome="1">Exception</span></summary><div class="rbody"><div class="rtools" data-chrome="1"><span>Official verification</span><label><input type="checkbox" class="rv" aria-label="Mark off-err as reviewed"> Reviewed</label></div><div class="tablewrap" tabindex="0" role="region" aria-label="Errata"><table><thead><tr><th scope="col">#</th><th scope="col">The guide says (location)</th><th scope="col">The official text says</th><th scope="col">Use this</th></tr></thead><tbody>${OFF.ERR.map(e=>`<tr id="${e[0]}"><th scope="row">${e[0]}</th><td>${esc(e[1])}</td><td>${esc(e[2])}</td><td>${esc(e[3])}</td></tr>`).join('')}</tbody></table></div></div></details>`;
offIdx.push({seg:'off',id:'off-err',head:'Errata — guide vs official text',type:'card',sl:'official'});
OFF2.SUP.slice().sort((a,b)=>parseInt(a.id.slice(5))-parseInt(b.id.slice(5))).forEach(b=>{offHtml+=offRule(b.id,b.title,b.types,b.cite,b.body)});
offHtml+=`<h3>Official-text tables</h3>`+OFF2.TABLES.map(t=>`<div class="study-aid" data-chrome="1"><span class="aid-label">Study aid · Table from official text</span>${tblHtml(t)}</div>`).join('');
offHtml+=`<h3>Official-text flowcharts</h3>`+OFF2.SVG.map(svgBlock).join('');
offHtml+=`<div class="aidsec" id="aids-off"><h3>Study aids — official orders</h3><div class="study-aid" data-chrome="1"><span class="aid-label">Study aid · Practice MCQs (answers cite the official paragraph)</span>`;
OFF2.MCQ.forEach((m,i)=>{offHtml+=`<details class="mcq"><summary>Q${i+1}. ${esc(m.q)}</summary><ol type="a">${m.o.map(o=>`<li>${esc(o)}</li>`).join('')}</ol><p><b>Answer: (${String.fromCharCode(97+m.a)})</b> ${esc(m.o[m.a])} — ${esc(m.why)} <small>Citation: ${esc(m.c)}</small></p></details>`;deck.mcqs.push({seg:'off',segt:'Official verification chapter',q:m.q,o:m.o,a:m.a,w:m.why,c:m.c})});
offHtml+=`</div><div class="study-aid" data-chrome="1"><span class="aid-label">Study aid · Flashcards</span>`;
OFF2.CARDS.forEach(c=>{offHtml+=`<div class="fc"><button class="fcflip btn" aria-expanded="false">${esc(c[0])}</button><div class="fcback" hidden>${esc(c[1])} <small>Source: ${esc(c[2])}</small></div></div>`;deck.cards.push({seg:'off',segt:'Official verification chapter',f:c[0],b:c[1],c:c[2]})});
offHtml+='</div></div></section>';
fs.writeFileSync(path.join(__dirname,'ch-official.html'),offHtml);
// ---------- traps + calculators ----------
EXTRA.MCQ.forEach(m=>deck.mcqs.push({seg:'extra',segt:'Extra practice (numerical, assertion–reason, official orders)',q:m.q,o:m.o,a:m.a,w:m.w,c:m.c}));
const trapsHtml=`<section class="chapter" id="sec-traps" aria-labelledby="traps-h"><h2 id="traps-h">Exam traps — commonly confused pairs</h2><details class="rule" id="off-trap" data-types="exception proviso" data-sl="official" open><summary><span class="rno" data-chrome="1">off-trap</span><h3>${EXTRA.TRAPS.length} trap pairs with the correct answer and where to check it</h3><span class="tb tb-exception" data-chrome="1">Exception</span></summary><div class="rbody"><div class="rtools" data-chrome="1"><span>Study aid</span><label><input type="checkbox" class="rv" aria-label="Mark off-trap as reviewed"> Reviewed</label></div><div class="study-aid" data-chrome="1"><span class="aid-label">Study aid · built from the guide’s source cards and the official orders</span><div class="tablewrap" tabindex="0" role="region" aria-label="Exam traps"><table><thead><tr><th scope="col">Topic</th><th scope="col">Common wrong answer</th><th scope="col">Correct (as per the cited text)</th><th scope="col">Check</th></tr></thead><tbody>${EXTRA.TRAPS.map(t=>`<tr><th scope="row">${esc(t[0])}</th><td>${esc(t[1])}</td><td>${esc(t[2])}</td><td>${esc(t[3])}</td></tr>`).join('')}</tbody></table></div></div></div></details></section>`;
offIdx.push({seg:'off',id:'off-trap',head:'Exam traps — commonly confused pairs',type:'card',sl:'study aid'});
const sel=(id,label,opts)=>`<p><label for="${id}">${label}</label> <select id="${id}">${opts.map(o=>`<option value="${o[0]}">${esc(o[1])}</option>`).join('')}</select></p>`;
const num=(id,label,v,extra='')=>`<p><label for="${id}">${label}</label> <input id="${id}" type="${extra==='text'?'text':'number'}" value="${v}" ${extra==='text'?'':'min="0" step="any"'} style="width:9em"></p>`;
const LV=[['L14','Level 14 and above'],['L12','Level 12 & 13'],['L9','Level 9 to 11'],['L6','Level 6 to 8'],['L5','Level 5 and below']];
const calcHtml=`<section class="chapter" id="sec-calc" aria-labelledby="calc-h"><h2 id="calc-h">Calculators (offline learning aids)</h2><p class="secmeta">Use these to practise the arithmetic. They apply the official 2017 base figures (DoE O.M. 13.07.2017) and, if you choose, the guide’s “current” figures (base × 1.25). They are <b>not</b> an entitlement decision; the conditions in the cards still apply.</p>
<div class="study-aid" data-chrome="1"><span class="aid-label">Study aid · Calculators</span>${sel('c-rates','Rate set',[['cur','Current (base × 1.25, as in the guide)'],['base','2017 base (official O.M.)']])}
<h3>Food DA by absence</h3>${sel('c-flevel','Pay Level',LV)}${num('c-hours','Hours away each calendar day (comma-separated)','16, 24, 8','text')}<p id="o-food" aria-live="polite"></p>
<h3>Hotel with GST</h3>${sel('c-hlevel','Pay Level',LV)}${num('c-tariff','Actual room tariff per night (₹)',4000)}${num('c-gst','GST %',12)}${num('c-nights','Nights',2)}<p id="o-hotel" aria-live="polite"></p>
<h3>Composite Transfer Grant</h3>${num('c-basic','Last month’s basic pay (₹)',70000)}${sel('c-ctg','Case',[['t20','Transfer, ≥ 20 km'],['t20r','Transfer < 20 km / same city, residence changes'],['t20n','Transfer < 20 km / same city, no residence change'],['isl','Transfer to/from A&N or Lakshadweep'],['sp50','Spouse transferred later (> 60 days after the first)'],['sp0','Spouse transferred later (within 60 days)'],['rr','Retirement, residence actually changes'],['rn','Retirement, no change of residence']])}<p id="o-ctg" aria-live="polite"></p>
<h3>Road mileage</h3>${sel('c-mode','Mode',[['car','Own car / taxi'],['auto','Auto-rickshaw / own scooter'],['foot','On foot (additional)']])}${num('c-km','Kilometres',50)}<p><label><input type="checkbox" id="c-dead"> Deduct first (“dead”) km for own car — not in the 2017 O.M.</label></p><p id="o-mile" aria-live="polite"></p>
<h3>Personal effects by road</h3>${sel('c-elevel','Level',[['L6','Level 6 and above'],['L5','Level 5'],['L4','Level 4 and below']])}${num('c-ekm','Kilometres',400)}<p id="o-eff" aria-live="polite"></p>
<h3>Claim deadline</h3>${sel('c-claim','Claim',[['tour','Tour / transfer / training (60 days)'],['ret','Retirement (180 days)']])}<p><label for="c-date">Journey completed on</label> <input id="c-date" type="date" value="2027-01-10"></p><p id="o-dead" aria-live="polite"></p></div></section>`;
offIdx.push({seg:'off',id:'sec-calc',head:'Calculators (offline learning aids)',type:'card',sl:'study aid'});
// ---------- paths, facts, cheat sheets, log ----------
const pathsHtml=`<section class="chapter" id="sec-paths" aria-labelledby="paths-h"><h2 id="paths-h">Reading paths</h2><div class="front-grid">${META.PATHS.map(pp=>`<div class="fcard"><h3>${esc(pp[0])}</h3><ol>${pp[1].map(x=>`<li><a href="#${x[0]}">${esc(x[1])}</a></li>`).join('')}</ol></div>`).join('')}</div></section>`;
const BADGE=st=>/^Official-checked/.test(st)?'tb-order':/Source only/.test(st)?'tb-explanation':/Conflict|Not in/.test(st)?'tb-exception':'tb-proviso';
const factsHtml=`<section class="chapter" id="sec-facts" aria-labelledby="facts-h"><h2 id="facts-h">Key-facts register — what is verified and what is not</h2><p class="secmeta">Status is for the fact as stated; it tells you how far to trust it. “Official-checked” = read in the official PDF on 26.11.2026.</p><div class="study-aid" data-chrome="1"><span class="aid-label">Study aid · Verification badges</span><div class="tablewrap" tabindex="0" role="region" aria-label="Key facts"><table><thead><tr><th scope="col">Fact</th><th scope="col">Status</th><th scope="col">Where</th></tr></thead><tbody>${META.FACTS.map(f=>`<tr><th scope="row">${esc(f[0])}</th><td><span class="tb ${BADGE(f[1])}">${esc(f[1])}</span></td><td>${esc(f[2])}</td></tr>`).join('')}</tbody></table></div></div>
<div class="study-aid" data-chrome="1"><span class="aid-label">Study aid · Corrected answer sheet (where the guide and the official text differ)</span><div class="tablewrap" tabindex="0" role="region" aria-label="Corrected answers"><table><thead><tr><th scope="col">Topic</th><th scope="col">Memorise this</th></tr></thead><tbody>${META.CORR.map(c=>`<tr><th scope="row">${esc(c[0])}</th><td>${esc(c[1])}</td></tr>`).join('')}</tbody></table></div></div></section>`;
const tb=(t)=>`<div class="cheat"><div class="tablewrap" tabindex="0" role="region" aria-label="${esc(t.title)}"><table><caption>${esc(t.title)} <small>— ${esc(t.cite)}</small></caption><thead><tr>${t.head.map(c=>`<th scope="col">${esc(c)}</th>`).join('')}</tr></thead><tbody>${t.rows.map(r=>`<tr>${r.map((c,i)=>i?`<td>${esc(c)}</td>`:`<th scope="row">${esc(c)}</th>`).join('')}</tr>`).join('')}</tbody></table></div></div>`;
const pick=k=>TABLES.find(t=>t.title.startsWith(k));
const cheatHtml=`<section class="chapter" id="sec-cheat" aria-labelledby="cheat-h"><h2 id="cheat-h">Cheat sheets (printable)</h2><p class="noprint"><button class="btn" id="printcheat">Print / save cheat sheets as PDF</button> <span class="secmeta">Prints only this section, one topic per page. Study aid, built from the verified tables above.</span></p>
<div class="study-aid" data-chrome="1"><span class="aid-label">Study aid · Cheat sheets</span>${[OFF2.TABLES[0],OFF2.TABLES[1],pick('Food DA by absence'),pick('CTG at a glance'),OFF2.TABLES[3],OFF2.TABLES[2]].map(tb).join('')}<div class="cheat"><p><b>Five-step audit (from the source’s AO module):</b> Sanction → Entitlement → DA and hotel → Transfer/retirement → Settlement (60/180 days).</p><p><b>Always check:</b> pay level; date of journey completion; advance vs claim clock; official order number; Official-text check boxes for that rule.</p></div></div></section>`;
const logHtml=`<section class="chapter" id="sec-log" aria-labelledby="log-h"><h2 id="log-h">Change log and currency check</h2><div class="study-aid" data-chrome="1"><span class="aid-label">Study aid · Change log</span><ul>${META.LOG.map(l=>`<li><b>${esc(l[0])}:</b> ${esc(l[1])}</li>`).join('')}</ul></div><div class="study-aid unc" data-chrome="1"><span class="aid-label">Re-check before relying on this file</span><ul>${META.RECHECK.map(r=>`<li>${esc(r)}</li>`).join('')}</ul></div></section>`;
[['sec-paths','Reading paths'],['sec-facts','Key-facts register'],['sec-cheat','Cheat sheets (printable)'],['sec-log','Change log and currency check']].forEach(x=>offIdx.push({seg:'off',id:x[0],head:x[1],type:'card',sl:'study aid'}));
// ---------- TA vs LTC comparison (common areas only) ----------
LTC.MCQ.forEach(m=>deck.mcqs.push({seg:'ltc',segt:'TA vs LTC comparison',q:m.q,o:m.o,a:m.a,w:m.w,c:m.c}));
LTC.CARDS.forEach(c=>deck.cards.push({seg:'ltc',segt:'TA vs LTC comparison',f:c[0],b:c[1],c:c[2]}));
const stB=st=>/^Official$/.test(st)?'tb-order':/Source only/.test(st)?'tb-explanation':/Conflict/.test(st)?'tb-exception':'tb-proviso';
const ltcHtml=`<section class="chapter" id="sec-ltc" aria-labelledby="ltc-h"><h2 id="ltc-h">TA and LTC — comparison of the common areas</h2>
<p class="secmeta">Scope: this guide covers the CCS Travelling Allowance rules. Leave Travel Concession is <b>not</b> studied here; only the areas where TA and LTC overlap or are often confused are compared. “Official” = read in the official order (DoPT orders from a staffnews.in-hosted copy; GFR; DoE O.M.s). “Source only” = stated by the study-guide source but not checked against the CCS (LTC) Rules, which could not be retrieved.</p>
<details class="rule" id="off-ltc" data-types="om order exception" data-sl="comparison" open><summary><span class="rno" data-chrome="1">off-ltc</span><h3>${LTC.ROWS.length} common areas compared side by side</h3><span class="tb tb-om" data-chrome="1">O.M.s</span></summary><div class="rbody"><div class="rtools" data-chrome="1"><span>Study aid</span><label><input type="checkbox" class="rv" aria-label="Mark off-ltc as reviewed"> Reviewed</label></div><div class="study-aid" data-chrome="1"><span class="aid-label">Study aid · Comparison table</span><div class="tablewrap" tabindex="0" role="region" aria-label="TA vs LTC"><table><thead><tr><th scope="col">Area</th><th scope="col">CCS Travelling Allowance</th><th scope="col">LTC (comparison only)</th><th scope="col">Status</th></tr></thead><tbody>${LTC.ROWS.map(r=>`<tr><th scope="row">${esc(r[0])}</th><td>${esc(r[1])}</td><td>${esc(r[2])}</td><td><span class="tb ${stB(r[3])}">${esc(r[3])}</span></td></tr>`).join('')}</tbody></table></div></div>${svgBlock(LTC.SVG)}
<div class="study-aid" data-chrome="1"><span class="aid-label">Study aid · Practice MCQs</span>${LTC.MCQ.map((m,i)=>`<details class="mcq"><summary>Q${i+1}. ${esc(m.q)}</summary><ol type="a">${m.o.map(o=>`<li>${esc(o)}</li>`).join('')}</ol><p><b>Answer: (${String.fromCharCode(97+m.a)})</b> ${esc(m.o[m.a])} — ${esc(m.w)} <small>Citation: ${esc(m.c)}</small></p></details>`).join('')}</div>
<div class="study-aid" data-chrome="1"><span class="aid-label">Study aid · Flashcards</span>${LTC.CARDS.map(c=>`<div class="fc"><button class="fcflip btn" aria-expanded="false">${esc(c[0])}</button><div class="fcback" hidden>${esc(c[1])} <small>Source: ${esc(c[2])}</small></div></div>`).join('')}</div></div></details></section>`;
offIdx.push({seg:'off',id:'sec-ltc',head:'TA and LTC — comparison of the common areas',type:'card',sl:'study aid'});
// ---------- FR/SR Part II (secondary summaries) ----------
FRSR.MCQ.forEach(m=>deck.mcqs.push({seg:'frsr',segt:'FR/SR Part II (secondary summaries)',q:m.q,o:m.o,a:m.a,w:m.w,c:m.c}));
FRSR.CARDS.forEach(c=>deck.cards.push({seg:'frsr',segt:'FR/SR Part II (secondary summaries)',f:c[0],b:c[1],c:c[2]}));
const frBadge=st=>/Gap/.test(st)?'tb-exception':/Conflicting|differs/.test(st)?'tb-exception':'tb-proviso';
const frsrHtml=`<section class="chapter" id="sec-frsr" aria-labelledby="frsr-h"><h2 id="frsr-h">FR / SR Part II — secondary summaries (from the compilation you supplied)</h2>
<p class="secmeta">${FRSR.NOTES.map(esc).join(' ')}</p>
<details class="rule" id="off-frsr" data-types="proviso exception" data-sl="secondary" open><summary><span class="rno" data-chrome="1">off-frsr</span><h3>SR-by-SR summaries (${FRSR.ROWS.length} entries) — not primary text</h3><span class="tb tb-proviso" data-chrome="1">Proviso</span></summary><div class="rbody"><div class="rtools" data-chrome="1"><span>Secondary</span><label><input type="checkbox" class="rv" aria-label="Mark off-frsr as reviewed"> Reviewed</label></div><div class="study-aid unc" data-chrome="1"><span class="aid-label">Secondary summaries — verify before relying on them</span><div class="tablewrap" tabindex="0" role="region" aria-label="FR/SR summaries"><table><thead><tr><th scope="col">SR</th><th scope="col">Summary (paraphrase, not rule text)</th><th scope="col">Status</th><th scope="col">Drawn from</th></tr></thead><tbody>${FRSR.ROWS.map(r=>`<tr id="${r[0]}"><th scope="row">${esc(r[2])}</th><td>${esc(r[3])}</td><td><span class="tb ${frBadge(r[4])}">${esc(r[4])}</span></td><td>${esc(r[5])}</td></tr>`).join('')}</tbody></table></div></div>
<div class="study-aid" data-chrome="1"><span class="aid-label">Where the compilation and the official orders disagree</span><div class="tablewrap" tabindex="0" role="region" aria-label="FR/SR discrepancies"><table><thead><tr><th scope="col">Point</th><th scope="col">What differs</th><th scope="col">Use</th></tr></thead><tbody>${FRSR.DISCREP.map(d=>`<tr><th scope="row">${esc(d[0])}</th><td>${esc(d[1])}</td><td>${esc(d[2])}</td></tr>`).join('')}</tbody></table></div></div>
<div class="study-aid" data-chrome="1"><span class="aid-label">Study aid · Practice MCQs (secondary summaries — treat as practice only)</span>${FRSR.MCQ.map((m,i)=>`<details class="mcq"><summary>Q${i+1}. ${esc(m.q)}</summary><ol type="a">${m.o.map(o=>`<li>${esc(o)}</li>`).join('')}</ol><p><b>Answer: (${String.fromCharCode(97+m.a)})</b> ${esc(m.o[m.a])} — ${esc(m.w)} <small>Citation: ${esc(m.c)}</small></p></details>`).join('')}</div>
<div class="study-aid" data-chrome="1"><span class="aid-label">Study aid · Flashcards</span>${FRSR.CARDS.map(c=>`<div class="fc"><button class="fcflip btn" aria-expanded="false">${esc(c[0])}</button><div class="fcback" hidden>${esc(c[1])} <small>Source: ${esc(c[2])}</small></div></div>`).join('')}</div></div></details></section>`;
offIdx.push({seg:'off',id:'sec-frsr',head:'FR/SR Part II — secondary summaries',type:'card',sl:'secondary'});
const FRMAP={};FRSR.ROWS.forEach(r=>r[1].forEach(k=>FRMAP[k]=r[0]));
// ---------- front matter ----------
const abbr=JSON.parse(fs.readFileSync(path.join(__dirname,'abbr.json'),'utf8'));
const tk=data.find(s=>s.key==='tk').pieces.find(p=>/id="glossary"/.test(p.html));
let glossary=clean(tk.html).replace(/\sid="[^"]*"/g,'').replace(/^\s*<div class="card">/,'<div>');
const flagsDisc=[
 ['Chapter 4 prose vs table (source L1213–1227)','The prose cites state RMA rates of ₹15–₹30/km (e.g. Delhi ₹27.50, Karnataka ₹28.75, Tripura ₹18.75); the sample table lists ₹12–₹24 (Delhi 22, Karnataka 23, Tripura 15). The source does not reconcile them.'],
 ['Chapter 6 exam-trap wording (source L1467)','The trap says a TA bill passed March 2023 “can be revised in June 2026 … Yes”, and in the same sentence calls it time-barred.'],
 ['SR range in the AO module (source L4085)','The AO baseline line says “SR 17–195”; Chapter 1 (L743–776) and its fact-sheet say SR 17–SR 246.'],
 ['DA band wording in the AO cheat sheet (source L4095)','The cheat sheet applies <6 h/6–12 h/>12 h percentages to “Food + Hotel + Local Travel”; Chapter 3 (L1069–1091) applies them to the food lump sum.'],
 ['Source markup defects repaired by the builder','Duplicated card opener at source L1317 and L1430 (dropped); missing card opener before L1350 and L1454 (added). A stray layout-wrapper element at L3264 was ignored. No text affected.']];
const front=`<section class="chapter" id="sec-start" aria-labelledby="start-h"><h2 id="start-h">Front matter</h2>
<div class="front-grid"><div class="fcard"><h3>Document version &amp; date</h3><ul><li><b>Source document:</b> “Travelling Allowance Rules — Updated Study Guide and Professor’s Toolkit — 22 November 2026” (its &lt;title&gt;).</li><li><b>Source file:</b> TA_Rules_Master_v4_2026-11-22_READABLE_FINAL.html — version marker <b>v4</b>, date <b>22 November 2026</b> (from the file name and title).</li><li><b>Legal basis named in the source:</b> DoE O.M. No. 19030/1/2017-E.IV dated 13.07.2017 (effective 01.07.2017) and selected later materials.</li><li><b>Official verification pass:</b> 26 November 2026 — the official DoE/GFR/DoPT-reproduction texts were read and compared; results are in <a href="#sec-official">Official verification</a>. The original source text is unchanged.</li><li><b>Scope:</b> the CCS Travelling Allowance rules. LTC is covered only in the “TA and LTC” comparison of common areas.</li><li><b>This guide:</b> single-file conversion with all source text kept verbatim; study aids are labelled and separate.</li></ul></div>
<div class="fcard"><h3>How to use this guide</h3><ul><li><b>Read the verbatim block first</b> (dashed left border), then the purple <i>Study aid</i> boxes. Study aids are never source text.</li><li><b>Search</b> (<kbd>/</kbd>): matches highlight; you can also type a block number (e.g. <code>ch05-004</code>) or a source line (e.g. <code>L743</code>) to filter.</li><li><b>Filters</b> show blocks tagged Proviso / Exception / O.M. / Order / FAQ / Explanation. Tags are an <i>automatic keyword heuristic</i> on the source wording — a guide to where to look, not a legal classification.</li><li><b>Collapse / expand</b> every block; mark blocks <b>Reviewed</b> (saved in this browser only); <kbd>j</kbd>/<kbd>k</kbd> move between blocks.</li><li><b>Flashcards</b>, <b>Spaced review</b> (saved schedule), <b>Quiz</b> and <b>Practice exam</b> (timed, mixed, weak-spots) in the top bar; the <a href="#sec-calc">Calculators</a> and <a href="#sec-traps">Exam traps</a> sections are offline study aids. Quiz questions use the guide’s own study aids; the source’s own MCQs (Chapter 16, Appendix B) are kept as-is and the source says their keys are unverified.</li><li><b>Superseded rules</b> (old one-third retirement CTG, flat 25% DA, the 16.02.2022 air entry) are collapsed and labelled; nothing is deleted — use “Show superseded” to see them. The ledger lists each one.</li><li><b>Amber “Official-text check” boxes</b> mark cards where the official PDF says something different or adds a point; the numbered errata (E1–E15) are in the Official verification chapter.</li><li>Status words from the source (“UNVERIFIED / HOLD”, “source status open”, “status varies”) are kept exactly; a study aid cannot upgrade them.</li></ul></div></div>
<h3>Abbreviations <small>(only those whose abbreviation and expansion both appear in the source)</small></h3><div class="tablewrap" tabindex="0" role="region" aria-label="Abbreviations"><table><thead><tr><th scope="col">Abbr.</th><th scope="col">Expansion as written in the source</th></tr></thead><tbody>${abbr.map(a=>`<tr><th scope="row">${esc(a[0])}</th><td>${esc(a[1])}</td></tr>`).join('')}</tbody></table></div>
<h3>Glossary <small>(copied from the source: “Glossary &amp; common confusions”, L4284–4301)</small></h3><div class="verbatim">${glossary}</div>
<h3>Discrepancies noticed inside the source <small>[uncertain — not resolved by this guide]</small></h3><ul>${flagsDisc.map(f=>`<li><b>${esc(f[0])}.</b> ${f[1].replace(/`/g,'')}</li>`).join('')}</ul></section>`;
allIdx.push(...offIdx);
const masterIdx=`<section class="chapter" id="toc" aria-labelledby="toc-h"><h2 id="toc-h">Master index of every block</h2><p class="secmeta">${allIdx.length} blocks (cards, notes, fact-sheets, recaps, cases, FAQs, verdicts). IDs are used for search and cross-references.</p><div class="idx">${[{key:'off',title:'Official verification — read first'}].concat(data).map(s=>{const L=allIdx.filter(x=>x.seg===s.key);return L.length?`<h3><a href="#${s.key==='off'?'sec-official':SECID(s.key)}">${esc(s.title)}</a></h3><ul>${L.map(x=>`<li><a href="#${x.id}">${esc(x.head||LABEL[x.type]||x.type)}</a> <small>${x.id} · ${x.sl}</small></li>`).join('')}</ul>`:''}).join('')}</div></section>`;
Object.keys(FRMAP).forEach(k=>{if(!XR[k]){const m=/^sr-(\d+)/.exec(k);XR[k]={label:'SR '+m[1],cites:[],n:+m[1]}}});
const xrefKeys=Object.keys(XR).sort((a,b)=>XR[a].n-XR[b].n||a.localeCompare(b));
const xrefSec=`<section class="chapter" id="sec-xref" aria-labelledby="xref-h"><h2 id="xref-h">Cross-reference index — where each SR is cited</h2><p class="secmeta">Generated at build time from the source text; each “SR n” in the text above links here. See also Appendix C (<a class="xref" href="#index">Reverse-Lookup Index</a>).</p><ul>${xrefKeys.map(k=>`<li id="xref-${k}"><b>${esc(XR[k].label)}</b>${FRMAP[k]?` — <a href="#${FRMAP[k]}">FR/SR summary (secondary)</a>`:''} — ${XR[k].cites.map(c=>`<a href="#${c.id}">${esc((c.head||c.id).slice(0,70))}</a> <small>(${c.id})</small>`).join('; ')}</li>`).join('')}</ul></section>`;
// ---------- assemble ----------
const GRP=t=>['~',t];
const sideLinks=[GRP('Start here'),['sec-start','Front matter'],['sec-paths','Reading paths'],['toc','Master index'],
 GRP('Verified layer and study tools'),['sec-official','Official verification (read first)'],['sec-facts','Key-facts register'],['sec-frsr','FR/SR Part II (secondary)'],['sec-traps','Exam traps'],['sec-ltc','TA vs LTC (common areas)'],['sec-cheat','Cheat sheets'],['sec-calc','Calculators'],
 GRP('Source chapters (verbatim)')].concat(data.map(s=>[SECID(s.key),s.title.replace(/ — .*$/,m=>m.length>46?m.slice(0,44)+'…':m)]),[GRP('Reference'),['sec-xref','Cross-reference index'],['sec-log','Change log & currency']]);
const css=fs.readFileSync(path.join(__dirname,'assets/style.css'),'utf8');let js=fs.readFileSync(path.join(__dirname,'assets/app.js'),'utf8');
const deckJson=JSON.stringify(deck).replace(/</g,'\\u003c');
const doc=`<!DOCTYPE html>
<html lang="en" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>TA Rules — Exam Study Guide (from TA Rules Master v4, 22 Nov 2026)</title>
<style>${css}</style></head><body>
<a class="skip" href="#main">Skip to main content</a>
<header id="topbar" role="banner"><button id="hamb" aria-controls="side" aria-expanded="false" aria-label="Toggle contents menu">☰ Contents</button>
<input id="q" type="search" placeholder="Search text or block no. (press /)" aria-label="Search the guide"><button id="clr" type="button">Clear</button><button id="toolsbtn" aria-expanded="false" aria-controls="tools">Tools ▾</button>
<button id="themebtn" aria-pressed="false">🌙 Dark</button><span id="hits" class="secmeta" aria-live="polite"></span>
<div id="tools"><fieldset class="filters" style="border:0;margin:0;padding:0"><legend class="secmeta" style="float:left;margin-right:8px">Show only:</legend>
${['proviso','exception','om','order','faq','explanation'].map(t=>`<label><input type="checkbox" value="${t}"> <span class="tb tb-${t}">${TL[t]}</span></label>`).join('')}</fieldset>
<button id="expall">Expand all</button><button id="colall">Collapse all</button><button id="supbtn" aria-pressed="false">Show superseded</button><button id="fcbtn">Flashcards</button><button id="srsbtn">Spaced review</button><button id="exbtn">Practice exam</button><button id="qzbtn">Quiz</button></div></header>
<div id="layout"><nav id="side" aria-label="Table of contents"><h2>Contents</h2><div id="prog" role="progressbar" aria-label="Review progress" aria-valuemin="0" aria-valuenow="0"><i></i></div><div class="secmeta"><span id="progtxt"></span> · <button id="progreset" class="btn" style="padding:2px 8px;font-size:.75rem">Reset</button></div>
<ol>${sideLinks.map(l=>l[0]==='~'?`<li class="grp">${esc(l[1])}</li>`:`<li><a href="#${l[0]}">${esc(l[1])}</a></li>`).join('')}</ol></nav>
<main id="main" tabindex="-1"><h1>Travelling Allowance Rules — Exam Study Guide</h1><p class="secmeta">Complete verbatim conversion of “TA Rules Master v4 — 22 November 2026”, with clearly labelled study aids.</p>
${front}${pathsHtml}${masterIdx}
${offHtml}
${factsHtml}
${frsrHtml}
${trapsHtml}
${ltcHtml}
${cheatHtml}
${calcHtml}
${data.map(s=>frags[s.key]).join('\n')}
${xrefSec}
${logHtml}</main></div>
<a href="#main" id="totop" class="noprint" aria-label="Back to top">↑ Top</a><div id="ov" role="dialog" aria-modal="true"><div id="ovbox"></div></div><div id="toast" role="status"></div>
<script type="application/json" id="deckdata">${deckJson}</script>
<script>${js}
${fs.readFileSync(path.join(__dirname,'assets/app2.js'),'utf8')}
(function(){function op(id){var e=id&&document.getElementById(id);if(!e)return;for(var n=e;n;n=n.parentElement){if(n.tagName==='DETAILS')n.open=true}}
window.addEventListener('hashchange',function(){op(location.hash.slice(1))});document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href^="#"]');if(a)op(a.getAttribute('href').slice(1))});if(location.hash)op(location.hash.slice(1))})();
</script></body></html>`;
fs.writeFileSync(OUT,doc);
console.log('built',OUT,(doc.length/1024).toFixed(0)+'KB','rules',allIdx.length,'mcqs',deck.mcqs.length,'cards',deck.cards.length,'xrefs',xrefKeys.length);
