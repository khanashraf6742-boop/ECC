// Phase 1/2 helper: segments source into sections and pieces; used by ledger + build.
const fs=require('fs');
const raw=fs.readFileSync(__dirname+'/source.html','utf8');
const lines=raw.split('\n'); // lines[i] is source line i+1
const SEGS=[
 ['front','Front matter: cover, study hub, source-check log',532,677,'front'],
 ['ch01','Chapter 1 — Foundations: Legal Basis, Definitions & Kinds of TA',731,858,'ch1'],
 ['ch02','Chapter 2 — Travel Entitlements by Mode & Pay Level',860,934,'ch2'],
 ['ch03','Chapter 3 — TA on Tour & Daily Allowance',936,1174,'ch3'],
 ['ch04','Chapter 4 — Mileage Allowance for Road Journeys',1176,1256,'ch4'],
 ['ch05','Chapter 5 — TA on Transfer',1258,1402,'ch5'],
 ['ch06','Chapter 6 — TA on Retirement, Death-in-Service & Re-employment',1404,1510,'ch6'],
 ['ch07','Chapter 7 — Selected Amendment Chronology (2017–2026)',1511,1951,'ch7'],
 ['ch08','Chapter 8 — Dearness Allowance Crosses 50%',1952,2059,'ch8'],
 ['ch09','Chapter 9 — Worked Illustrations & TA-Bill Practice',2060,2125,'ch9'],
 ['ch10','Chapter 10 — Definitions, City Classification, Booking Rules & TA Advances',2126,2456,'ch10'],
 ['ch11','Chapter 11 — Extended Tour, Transfer, Retirement, Exam-TA & Disability Provisions',2457,2928,'ch11'],
 ['apA','Appendix A — Flashcard / Active-Recall Bank',2929,3024,'flash'],
 ['apB','Appendix B — Exam-Format Drill',3025,3166,'drill'],
 ['apC','Appendix C — Reverse-Lookup Index',3167,3256,'index'],
 ['p2','Part II — Technical Resignation, Transfer TA & Joining Pay (introduction)',3257,3285,'part-ii-technical-resignation'],
 ['ch12','Chapter 12 — Technical Resignation: Fundamentals',3286,3324,'ch12'],
 ['ch13','Chapter 13 — Joining Time & TTA: 2015 Amendment and 2022 Consolidation',3325,3366,'ch13'],
 ['ch14','Chapter 14 — Case Studies (not rulings)',3367,3650,'ch14'],
 ['ch15','Chapter 15 — Master Benefits Comparison',3651,3687,'ch15'],
 ['ch16','Chapter 16 — Exam-Format MCQs',3688,3978,'ch16'],
 ['ch17','Chapter 17 — Frequently Asked Questions',3979,4043,'ch17'],
 ['apD','Appendix D — Quick-Reference Index: Rules & Authorities',4044,4081,'appendix-d'],
 ['pack','AO Examination Mastery Module (AO quick-reference repeat & claim workflow)',4082,4147,'ta-professor-pack'],
 ['tk','Professor’s Addendum — evidence, claim workflow & study tools',4148,4347,'professor-toolkit'],
];
const FIX_DROP=new Set([1317,1430]);
const FIX_PREFIX={1350:'<div class="card">',1454:'<div class="card">'};
const TOP=/^\s*<(div class="(card|micronote|mfs|review|recap|case-box|verdict|worked|faq|chapter-banner|chapbreak|cover|part-ii-update|part-break|flag|toc)\b|aside\b|section\b|div id="ta-professor-pack"|details\b)/;
function bal(s){let d=0;const re=/<(\/?)(div|section|aside|details)\b[^>]*>/g;let m;while((m=re.exec(s)))d+=m[1]?-1:1;return d;}
function pieces(seg){
  const [key,title,a,b]=seg;const out=[];let cur=null;let depth=0;
  for(let n=a;n<=b;n++){
    let t=lines[n-1];
    if(FIX_DROP.has(n))continue;                           // duplicated stray <div class="card"> opener in source (markup defect)
    if(FIX_PREFIX[n])t=FIX_PREFIX[n]+'\n'+t;               // card opener missing in source (markup defect)
    if(key==='pack'&&(n===4082||n===4144))continue;      // wrapper div of AO module (layout only)
    if(key==='tk'&&(n===4148||n===4347))continue;        // wrapper section of addendum (layout only)
    if(n===3264&&/<div class="wrap">/.test(t))t='';           // stray nested .wrap opener (layout wrapper only)
    const startsNew=key==='pack'?/^\s*<(h1|h2|aside)\b/.test(t):depth<=0&&(TOP.test(t)||/^<!--/.test(t)||(/^<(h[1-4]|p|table|ul|ol)\b/.test(t)));
    const force=key!=='pack'&&/^<div class="(card|case-box|mfs|recap|review|micronote)"/.test(t)&&cur&&cur.lines.length&&!/^\s*<div class="(card|case-box|mfs|recap|review|micronote)"/.test(cur.lines[0]===undefined?'':'x');
    if(!cur||force&&depth>0||startsNew&&depth<=0&&cur.closed){ if(force&&depth>0)depth=0; if(cur)out.push(cur); cur={l1:n,l2:n,lines:[],closed:false}; }
    cur.lines.push(t);cur.l2=n;depth=Math.max(0,depth+bal(t));
    if(depth<=0||key==='pack')cur.closed=true;
  }
  if(cur)out.push(cur);
  for(const p of out){
    p.html=p.lines.join('\n');p.depthEnd=bal(p.html);
    if(p.depthEnd>0){p.repaired=p.depthEnd;p.html+=('\n</div>').repeat(p.depthEnd);p.depthEnd=0;}
    if(p.depthEnd<0){ // stray closers of layout wrappers the splitter treats as transparent
      const ls=p.lines.slice();p.strayClosers=0;
      for(let i=ls.length-1;i>=0&&bal(ls.join('\n'))<0;i--){ if(/^\s*<\/div>\s*$/.test(ls[i])){ls.splice(i,1);p.strayClosers++;} }
      p.html=ls.join('\n');p.depthEnd=bal(p.html);
    }
  }
  return out;
}
module.exports={raw,lines,SEGS,pieces,bal};
if(require.main===module){let tot=0;for(const s of SEGS){const ps=pieces(s);tot+=ps.length;const bad=ps.filter(p=>p.depthEnd!==0);console.log(s[0],ps.length,'pieces; unbalanced:',bad.map(p=>p.l1+'-'+p.l2+'('+p.depthEnd+')').join(' '));}console.log('total',tot);}
