p = 'build.js'
s = open(p).read()
s = s.replace("EXTRA=require('./extra');", "EXTRA=require('./extra'),META=require('./meta');")
s = s.replace(
    "  h=h.replace(/target=\"_blank\"/g",
    "  h=h.replace(/<div class=\"simple\"><span class=\"lbl\">/g,'<div class=\"simple\"><span class=\"lbl\" role=\"button\" tabindex=\"0\" aria-expanded=\"false\">');\n  h=h.replace(/target=\"_blank\"/g",
    1)

meta = r'''// ---------- paths, facts, cheat sheets, log ----------
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
'''
s = s.replace("// ---------- front matter ----------", meta + "// ---------- front matter ----------", 1)
s = s.replace(
    "${front}${masterIdx}\n${offHtml}\n${trapsHtml}\n${calcHtml}",
    "${front}${pathsHtml}${masterIdx}\n${offHtml}\n${factsHtml}\n${trapsHtml}\n${cheatHtml}\n${calcHtml}")
s = s.replace(
    "['sec-traps','Exam traps'],['sec-calc','Calculators']]",
    "['sec-facts','Key-facts register'],['sec-traps','Exam traps'],['sec-cheat','Cheat sheets'],['sec-calc','Calculators']]")
s = s.replace(
    "const sideLinks=[['sec-start','Front matter'],",
    "const sideLinks=[['sec-start','Front matter'],['sec-paths','Reading paths'],")
s = s.replace("['sec-xref','Cross-reference index']]", "['sec-xref','Cross-reference index'],['sec-log','Change log & currency']]")
s = s.replace("${xrefSec}</main>", "${xrefSec}\n${logHtml}</main>")
open(p, 'w').write(s)

p = 'assets/app2.js'
s = open(p).read()
i = s.rindex('})();')
add = r'''/* print cheat sheets, collapsible Hinglish blocks */
var pc=$('#printcheat');if(pc)pc.addEventListener('click',function(){document.body.classList.add('print-cheat');window.print()});window.addEventListener('afterprint',function(){document.body.classList.remove('print-cheat')});
function tg(l){var d=l.parentNode;var o=d.classList.toggle('open');l.setAttribute('aria-expanded',o)}
document.addEventListener('click',function(e){var l=e.target.closest&&e.target.closest('.simple>.lbl');if(l)tg(l)});
document.addEventListener('keydown',function(e){if((e.key==='Enter'||e.key===' ')&&e.target.matches&&e.target.matches('.simple>.lbl')){e.preventDefault();tg(e.target)}});
var ea=$('#expall'),ca=$('#colall');if(ea)ea.addEventListener('click',function(){$$('.simple').forEach(function(d){d.classList.add('open');$('.lbl',d).setAttribute('aria-expanded','true')})});if(ca)ca.addEventListener('click',function(){$$('.simple').forEach(function(d){d.classList.remove('open');$('.lbl',d).setAttribute('aria-expanded','false')})});
var qq=$('#q');if(qq)qq.addEventListener('input',function(){setTimeout(function(){$$('.simple').forEach(function(d){if($('mark.sm',d)){d.classList.add('open')}})},450)});
'''
s = s[:i] + add + s[i:]
open(p, 'w').write(s)

css = '''
.simple:not(.open)>*:not(.lbl){display:none}.simple>.lbl{cursor:pointer}.simple>.lbl:after{content:" ▸ show";text-transform:none;font-weight:600;color:var(--acc)}.simple.open>.lbl:after{content:" ▾ hide"}
@media print{.simple>*{display:block!important}body.print-cheat main>section:not(#sec-cheat),body.print-cheat main>h1,body.print-cheat main>p{display:none!important}body.print-cheat #sec-cheat .cheat{break-after:page}}
'''
open('assets/style.css', 'a').write(css)
