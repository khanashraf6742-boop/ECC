p = 'build.js'
s = open(p).read()
s = s.replace("META=require('./meta');", "META=require('./meta'),LTC=require('./ltc');")

block = r'''// ---------- TA vs LTC comparison (common areas only) ----------
LTC.MCQ.forEach(m=>deck.mcqs.push({seg:'ltc',segt:'TA vs LTC comparison',q:m.q,o:m.o,a:m.a,w:m.w,c:m.c}));
LTC.CARDS.forEach(c=>deck.cards.push({seg:'ltc',segt:'TA vs LTC comparison',f:c[0],b:c[1],c:c[2]}));
const stB=st=>/^Official$/.test(st)?'tb-order':/Source only/.test(st)?'tb-explanation':/Conflict/.test(st)?'tb-exception':'tb-proviso';
const ltcHtml=`<section class="chapter" id="sec-ltc" aria-labelledby="ltc-h"><h2 id="ltc-h">TA and LTC — comparison of the common areas</h2>
<p class="secmeta">Scope: this guide covers the CCS Travelling Allowance rules. Leave Travel Concession is <b>not</b> studied here; only the areas where TA and LTC overlap or are often confused are compared. “Official” = read in the official order (DoPT orders from a staffnews.in-hosted copy; GFR; DoE O.M.s). “Source only” = stated by the study-guide source but not checked against the CCS (LTC) Rules, which could not be retrieved.</p>
<details class="rule" id="off-ltc" data-types="om order exception" data-sl="comparison" open><summary><span class="rno" data-chrome="1">off-ltc</span><h3>${LTC.ROWS.length} common areas compared side by side</h3><span class="tb tb-om" data-chrome="1">O.M.s</span></summary><div class="rbody"><div class="rtools" data-chrome="1"><span>Study aid</span><label><input type="checkbox" class="rv" aria-label="Mark off-ltc as reviewed"> Reviewed</label></div><div class="study-aid" data-chrome="1"><span class="aid-label">Study aid · Comparison table</span><div class="tablewrap" tabindex="0" role="region" aria-label="TA vs LTC"><table><thead><tr><th scope="col">Area</th><th scope="col">CCS Travelling Allowance</th><th scope="col">LTC (comparison only)</th><th scope="col">Status</th></tr></thead><tbody>${LTC.ROWS.map(r=>`<tr><th scope="row">${esc(r[0])}</th><td>${esc(r[1])}</td><td>${esc(r[2])}</td><td><span class="tb ${stB(r[3])}">${esc(r[3])}</span></td></tr>`).join('')}</tbody></table></div></div>${svgBlock(LTC.SVG)}
<div class="study-aid" data-chrome="1"><span class="aid-label">Study aid · Practice MCQs</span>${LTC.MCQ.map((m,i)=>`<details class="mcq"><summary>Q${i+1}. ${esc(m.q)}</summary><ol type="a">${m.o.map(o=>`<li>${esc(o)}</li>`).join('')}</ol><p><b>Answer: (${String.fromCharCode(97+m.a)})</b> ${esc(m.o[m.a])} — ${esc(m.w)} <small>Citation: ${esc(m.c)}</small></p></details>`).join('')}</div>
<div class="study-aid" data-chrome="1"><span class="aid-label">Study aid · Flashcards</span>${LTC.CARDS.map(c=>`<div class="fc"><button class="fcflip btn" aria-expanded="false">${esc(c[0])}</button><div class="fcback" hidden>${esc(c[1])} <small>Source: ${esc(c[2])}</small></div></div>`).join('')}</div></div></details></section>`;
offIdx.push({seg:'off',id:'sec-ltc',head:'TA and LTC — comparison of the common areas',type:'card',sl:'study aid'});
'''
s = s.replace("// ---------- front matter ----------", block + "// ---------- front matter ----------", 1)
s = s.replace("${factsHtml}\n${trapsHtml}", "${factsHtml}\n${trapsHtml}\n${ltcHtml}")

# sidebar groups
old_start = s.index("const sideLinks=[")
old_end = s.index("\n", s.index("];", old_start)) if False else s.index("const css=")
new_side = r'''const GRP=t=>['~',t];
const sideLinks=[GRP('Start here'),['sec-start','Front matter'],['sec-paths','Reading paths'],['toc','Master index'],
 GRP('Verified layer and study tools'),['sec-official','Official verification (read first)'],['sec-facts','Key-facts register'],['sec-traps','Exam traps'],['sec-ltc','TA vs LTC (common areas)'],['sec-cheat','Cheat sheets'],['sec-calc','Calculators'],
 GRP('Source chapters (verbatim)')].concat(data.map(s=>[SECID(s.key),s.title.replace(/ — .*$/,m=>m.length>46?m.slice(0,44)+'…':m)]),[GRP('Reference'),['sec-xref','Cross-reference index'],['sec-log','Change log & currency']]);
'''
s = s[:old_start] + new_side + s[old_end:]
s = s.replace("<ol>${sideLinks.map(l=>`<li><a href=\"#${l[0]}\">${esc(l[1])}</a></li>`).join('')}</ol>",
              "<ol>${sideLinks.map(l=>l[0]==='~'?`<li class=\"grp\">${esc(l[1])}</li>`:`<li><a href=\"#${l[0]}\">${esc(l[1])}</a></li>`).join('')}</ol>")
# scope note + back to top
s = s.replace("<li><b>This guide:</b>", "<li><b>Scope:</b> the CCS Travelling Allowance rules. LTC is covered only in the “TA and LTC” comparison of common areas.</li><li><b>This guide:</b>")
s = s.replace("<div id=\"ov\"", "<a href=\"#main\" id=\"totop\" class=\"noprint\" aria-label=\"Back to top\">↑ Top</a><div id=\"ov\"")
open(p, 'w').write(s)

css = '''
#side li.grp{margin:10px 0 2px;padding:2px 8px;font:700 .68rem/1.3 system-ui;text-transform:uppercase;letter-spacing:.07em;color:var(--mute)}
#totop{position:fixed;right:14px;bottom:14px;z-index:60;padding:6px 12px;border-radius:999px;background:var(--acc);color:var(--bg);text-decoration:none;font-weight:700;font-size:.85rem}
'''
open('assets/style.css', 'a').write(css)

# register + facts
o = open('official.js').read()
row = "['DoPT O.M. F.No. 31011/15/2022-Estt.A-IV, 09.09.2026, with enclosures DoPT O.M.s 29.08.2022 and October 2023 (air booking) — used only for the TA vs LTC comparison','https://www.staffnews.in/wp-content/uploads/2026/09/SPECIAL-DISPENSATION-SCHEME.pdf','Read (9 pages, text layer); secondary-hosted copy (staffnews.in)','Comparison of common areas only; LTC itself is out of scope.'],\n"
o = o.replace("['DoE O.M. 21/1/2018-E.II(B), 29.07.2025", row + "['DoE O.M. 21/1/2018-E.II(B), 29.07.2025", 1)
open('official.js', 'w').write(o)

m = open('meta.js').read()
m = m.replace("['Para 3.6.3: TTA for temporary staff under 3 years'", "['TA and LTC common air-booking regime (three ATAs, slots, 10% band, no mileage points)',OFFC+' (DoPT copy secondary-hosted)','TA vs LTC table'],\n['LTC claim period: GFR 292 (30/60 days) vs source (1/3 months)',CONF+' (no-advance case)','TA vs LTC table'],\n['Para 3.6.3: TTA for temporary staff under 3 years'", 1)
m = m.replace("const LOG=[\n", "const LOG=[\n['26 Nov 2026','Added the “TA and LTC” comparison of common areas (LTC itself remains out of scope); sidebar grouped; scope note and back-to-top added.'],\n", 1)
open('meta.js', 'w').write(m)
