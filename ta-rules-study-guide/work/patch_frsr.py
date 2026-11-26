p = 'build.js'
s = open(p).read()
s = s.replace("LTC=require('./ltc');", "LTC=require('./ltc'),FRSR=require('./frsr');")

block = r'''// ---------- FR/SR Part II (secondary summaries) ----------
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
'''
s = s.replace("// ---------- front matter ----------", block + "// ---------- front matter ----------", 1)
s = s.replace("${factsHtml}\n${trapsHtml}\n${ltcHtml}", "${factsHtml}\n${frsrHtml}\n${trapsHtml}\n${ltcHtml}")
s = s.replace("['sec-facts','Key-facts register'],['sec-traps','Exam traps']", "['sec-facts','Key-facts register'],['sec-frsr','FR/SR Part II (secondary)'],['sec-traps','Exam traps']")
# xref entries: add FR/SR summary link
s = s.replace("<b>${esc(XR[k].label)}</b> — ${XR[k].cites", "<b>${esc(XR[k].label)}</b>${FRMAP[k]?` — <a href=\"#${FRMAP[k]}\">FR/SR summary (secondary)</a>`:''} — ${XR[k].cites")
open(p, 'w').write(s)

# xref: also list SRs that exist only in the compilation
s = open(p).read()
s = s.replace("const xrefKeys=Object.keys(XR)", "Object.keys(FRMAP).forEach(k=>{if(!XR[k]){const m=/^sr-(\\d+)/.exec(k);XR[k]={label:'SR '+m[1],cites:[],n:+m[1]}}});\nconst xrefKeys=Object.keys(XR)")
open(p, 'w').write(s)

o = open('official.js').read()
row = "['FR/SR Part II compilation supplied by the user (secondary summaries: SR 30/31, 46, 51, 58, 61, 71–73, 107, 110–116, 147, 148, 164, 172, 206)','(supplied file: work/official/user_FR_SR_Part_II_secondary_compilation.html)','Read in full (HTML)','Secondary only — added as the “FR/SR Part II (secondary)” section; three conflicts with the official orders recorded (E16–E18).'],\n"
o = o.replace("['DoE O.M. 21/1/2018-E.II(B), 29.07.2025", row + "['DoE O.M. 21/1/2018-E.II(B), 29.07.2025", 1)
err = ("['E16','SR 147 as “Transfer TA” and SR 116 as “general TA” in the supplied FR/SR compilation (CSD Rates summary).','Official O.M. 13.07.2017: SR 114 = general conditions on transfer TA (para 3(i)(a)); SR 116 = conveyance on transfer (para 3(iv)); SR 147 = general conditions on TA on retirement (para 4).','Use the official roles of SR 114 / 116 / 147.'],\n"
       "['E17','The guide’s source cites SR 58 and SR 107 for steamer entitlements (ch10-006).','The supplied compilation records SR 58 as deleted (or an unrelated police text) and SR 107 as TA on re-appointment; the official O.M. para 2C does not cite an SR for steamer classes.','Unresolved — quote the O.M. para 2C, not an SR number.'],\n"
       "['E18','The 180-day figure (E2) has no origin in the O.M.','The compilation records a G.I.O.(4) 180-day limit on DA for local journeys in one secondary training document.','If it exists it comes from FR/SR commentary; keep it unverified.']];\nmodule.exports")
o = o.replace("];\nmodule.exports", "," + err[:-len("];\nmodule.exports")] + "];\nmodule.exports", 1) if False else o
open('official.js', 'w').write(o)
