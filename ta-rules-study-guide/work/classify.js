const {SEGS,pieces,lines}=require('./segment');
const strip=h=>h.replace(/<[^>]+>/g,' ').replace(/&nbsp;/g,' ').replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&rarr;/g,'→').replace(/\s+/g,' ').trim();
function pieceType(p){
  const f=p.lines.find(l=>l.trim())||'';
  if(/^\s*<!--/.test(f))return 'comment';
  let m=/class="([^"]*)"/.exec(f);const c=m?m[1]:'';
  if(/^\s*<aside/.test(f))return /chapter-study-note/.test(c)?'study-map':'aside';
  if(/chapbreak|part-break/.test(c))return 'anchor';
  if(/^\s*<details/.test(f))return 'flashcard';
  if(/^\s*<h1/.test(f))return 'title';
  if(/^\s*<h2/.test(f))return 'section';
  if(/^\s*<(p|table|ul|ol|a)\b/.test(f))return 'text';
  for(const k of ['chapter-banner','card','micronote','mfs','review','recap','case-box','verdict','worked','faq','cover','part-ii-update','flag','toc','study-hub'])if(new RegExp('(^|\\s)'+k+'(\\s|$)').test(c))return k;
  if(/<section/.test(f))return 'section-el';
  return 'other';
}
function heading(p){const m=/<h[1-4][^>]*>([\s\S]*?)<\/h[1-4]>/.exec(p.html);return m?strip(m[1]):'';}
const SUB=/^\s*<(div class="(src|simple|hook|pyq|trapx|solution[^"]*|verdict[^"]*|worked|comparison-note|micronote|faq-q|faq-a|flag|analogy|status-note|editor-note)"|p class="(comparison-note|trapnote)"|details>|table\b)/;
function subs(p){
  const out=[];
  p.lines.forEach((l,i)=>{const n=p.l1+i;const m=SUB.exec(l);
    if(m){const kind=(m[2]||m[3]||(m[1].startsWith('details')?'flashcard':'table')).split(' ')[0];
      const lb=/<span class="lbl">([\s\S]*?)<\/span>/.exec(l);const sm=/<summary>([\s\S]*?)<\/summary>/.exec(l);const cap=/<caption>([\s\S]*?)<\/caption>/.exec(l);
      out.push({n,kind,label:strip(lb?lb[1]:sm?sm[1]:cap?cap[1]:l).slice(0,90)});}
    else{const q=/^<p><b>(Q\d+[^<]{0,20})<\/b>/.exec(l.trim());if(q)out.push({n,kind:'mcq',label:strip(l).slice(0,90)});}
  });
  return out;
}
let _id=0;
function build(){
  const res=[];
  for(const s of SEGS){const ps=pieces(s);let k=0;
    for(const p of ps){const t=pieceType(p);p.type=t;p.id=s[0]+'-'+String(++k).padStart(3,'0');p.head=heading(p);p.subs=subs(p);}
    res.push({key:s[0],title:s[1],l1:s[2],l2:s[3],anchor:s[4],pieces:ps});
  }
  return res;
}
module.exports={build,strip,pieceType,heading,subs};
