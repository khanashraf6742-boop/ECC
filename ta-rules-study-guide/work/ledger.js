const fs=require('fs');const {build}=require('./classify');
const done=fs.existsSync(__dirname+'/done.json')?JSON.parse(fs.readFileSync(__dirname+'/done.json','utf8')):{};
const data=build();
const EXC=[
 ['EX-01','506–515','Inline <style> block and 507–515 CSS (presentation of the original page; replaced by this guide’s own inline CSS)'],
 ['EX-02','516–528','“TA AO Quick-Jump” nav bar (navigation chrome; replaced by sticky sidebar). Every target section is retained.'],
 ['EX-03','679–728','Source “Table of Contents” list (navigation chrome; replaced by generated sidebar TOC + master index)'],
 ['EX-04','3252','“↑ Top” back-link (navigation chrome)'],
 ['EX-06','530, 1317, 1430, 3264','Layout-only wrapper tags (<div class="wrap"> openers at L530/L3264) and duplicated stray card openers at L1317/L1430 (markup defects, no text)'],
 ['EX-05','4350','Injected third-party <script> (Cloudflare challenge loader, line 4350 — not source content; fetches external resource)'],
];
const nComments=data.reduce((a,sg)=>a+sg.pieces.filter(p=>p.type==='comment').length,0);EXC.push(['EX-07','various',nComments+' HTML comments (<!-- … CHAPTER n … --> section markers; no reader-visible text)']);
let tot={}, rows=[], nPieces=0,nSubs=0;
for(const s of data){
  rows.push(`\n## ${s.title}  _(source lines ${s.l1}–${s.l2})_\n`);
  rows.push('| ID | Type | Heading / label | Source lines | Status |','|---|---|---|---|---|');
  for(const p of s.pieces){
    if(p.type==='comment')continue;
    nPieces++;tot[p.type]=(tot[p.type]||0)+1;
    const st=done[s.key]?'DONE':'PENDING';
    rows.push(`| ${p.id} | ${p.type} | ${(p.head||'—').replace(/\|/g,'/')} | ${p.l1}–${p.l2} | ${st} |`);
    p.subs.forEach((u,i)=>{nSubs++;tot['sub:'+u.kind]=(tot['sub:'+u.kind]||0)+1;
      rows.push(`| ${p.id}.${String(i+1).padStart(2,'0')} | ↳ ${u.kind} | ${u.label.replace(/\|/g,'/')} | ${u.n} | ${st} |`);});
  }
}
const head=`# Ledger — TA Rules study guide (source: TA_Rules_Master_v4_2026-11-22_READABLE_FINAL.html, 4,351 lines)

Unit definition: the source is a secondary study guide (chapters → cards/notes/fact-sheets/recaps/cases/FAQs → labelled sub-blocks), not clause-numbered rule text. Each **top-level piece** (rule-card, note, fact-sheet, review, recap, case, verdict, FAQ, flashcard, MCQ card, banner, study-map…) is a ledger row; **↳ rows** are the labelled sub-blocks inside it (Exact-Source Fact Card, Simple Terms, Memory Hook, Exam Angle, trap, solution, verdict, worked, tables, flashcards, MCQs). Every piece is extracted verbatim by script (build.js), so no clause-level paraphrase occurs.

No item in the source carries an “obsolete / omitted / rescinded / superseded-and-removed” marker that removes it from the guide. Items the source marks “status varies”, “UNVERIFIED / HOLD” or “source status open” are **kept** and keep their badge. The EXCLUDED rows below are page chrome / non-content only.

## EXCLUDED
| ID | Source lines | Reason / marker |
|---|---|---|
${EXC.sort((a,b)=>a[0]<b[0]?-1:1).map(e=>`| ${e[0]} | ${e[1]} | ${e[2]} | EXCLUDED |`).join('\n')}

## Superseded passages (collapsed and labelled, not deleted)
- L1743 (ch07-013): old one-third retirement CTG statement — superseded by O.M. 06.01.2022
- L1628 (ch07-008) and L1635 (Hinglish): flat 25% DA — superseded by O.M. 01.02.2018
- L1544 (ch07-004): 16.02.2022 air row — superseded by O.M. 16.06.2022 para 16
- L1849–1850 (ch07-017): 16.02.2022 “Best Available Fare” item — superseded by O.M. 16.06.2022 para 16

## Totals
- Top-level pieces: **${nPieces}**; labelled sub-blocks: **${nSubs}**
- By type: ${Object.entries(tot).sort().map(([k,v])=>k+'='+v).join(', ')}
- PENDING: ${rows.filter(r=>/\| PENDING \|$/.test(r)).length}  DONE: ${rows.filter(r=>/\| DONE \|$/.test(r)).length}  EXCLUDED: ${EXC.length}
`;
fs.writeFileSync(__dirname+'/ledger.md',head+rows.join('\n')+'\n');
console.log(head.split('## Totals')[1]);
