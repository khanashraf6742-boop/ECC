const {chromium}=require('playwright');const path=require('path'),fs=require('fs');
const {build}=require('./classify');
(async()=>{const data=build();const b=await chromium.launch();const p=await b.newPage({deviceScaleFactor:1});
await p.goto('file://'+path.resolve(__dirname,'../TA_Rules_Study_Guide.html'));
const pieces=[];data.forEach(s=>s.pieces.forEach(x=>{if(x.type!=='comment')pieces.push({id:x.id,type:x.type,html:x.html.replace(/<a class="back-top"[^>]*>[^<]*<\/a>/g,'').replace(/<script[\s\S]*?<\/script>/g,'')})}));
const res=await p.evaluate((pieces)=>{const norm=s=>s.replace(/\s+/g,'');const exp={};const d=document.createElement('div');
 pieces.forEach(x=>{d.innerHTML=x.html;exp[x.id]=norm(d.textContent)});
 const out={};const rules=document.querySelectorAll('details.rule');rules.forEach(r=>{const h=r.querySelector('summary h3,summary h4');const hv=h?norm(h.textContent):'';const v=r.querySelector('.verbatim');out[r.id]=norm((hv?hv+' ':'')+(v?v.textContent:''))});
 const whole=norm(document.querySelector('main').textContent);
 return {exp,out,whole}},pieces);
let ok=0,miss=[],struct=0,structMiss=[];
for(const x of pieces){const e=res.exp[x.id];
  if(res.out[x.id]!==undefined){ if(res.out[x.id]===e)ok++;else miss.push(x.id)}
  else{struct++;if(e&&!res.whole.includes(e))structMiss.push(x.id)}}
console.log('wrapped pieces identical:',ok,'mismatch:',miss.length,miss.join(','));console.log('structural pieces:',struct,'missing in output:',structMiss.length,structMiss.join(','));
// mismatch detail
for(const id of miss.slice(0,6)){const a=res.exp[id],o=res.out[id];let i=0;while(i<a.length&&a[i]===o[i])i++;console.log('--',id,'first diff @',i,'\n src:',JSON.stringify(a.slice(Math.max(0,i-30),i+60)),'\n out:',JSON.stringify(o.slice(Math.max(0,i-30),i+60)))}
// class-block counts (source vs output)
const src=fs.readFileSync(__dirname+'/source.html','utf8').split('\n').slice(529,4347).join('\n');const out=fs.readFileSync(__dirname+'/../TA_Rules_Study_Guide.html','utf8');
const ocount=(h,re)=>(h.match(re)||[]).length;
const classes=['trapx','pyq','solution','verdict','flag','comparison-note','analogy','worked','hook','simple','src','faq-q','faq-a','case-box','micronote','mfs','review','recap'];
console.log('class counts (source → output):');classes.forEach(c=>{const re=new RegExp('class="[^"]*\\b'+c+'\\b[^"]*"','g');const a=ocount(src,re);const bo=ocount(out.split('<script type="application/json"')[0],re);console.log(' ',c,a,'→',bo,a===bo?'':'  <-- differs (study-aid/chrome or glossary copy?)')});
// identifier counts
const srcText=await p.evaluate(()=>0);
const idRes={om:/\b\d{4,5}\/\d{1,2}(?:\/\d{2,4})?-?[A-Z][A-Za-z.()\-]*/g,sr:/\bSR(?:&nbsp;|\s)\d{1,3}/g,omn:/OM \d{1,2}:/g,mcq:/MCQ-T[AR]-\d+/g,q:/<b>Q\d+[.\s]/g,faq:/class="faq"/g,date:/\b\d{2}\.\d{2}\.\d{4}\b/g};
const srcBody=src.replace(/<a class="back-top"[^>]*>[^<]*<\/a>/g,'');const outMain=out.slice(out.indexOf('id="sec-ch01"'),out.indexOf('id="sec-xref"'));
console.log('identifier counts source-body vs output-chapters (output also holds study aids/tables/MCQs, so ≥ expected):');
for(const [k,re] of Object.entries(idRes)){console.log(' ',k,ocount(srcBody,re),ocount(outMain,re))}
fs.writeFileSync('verify-result.json',JSON.stringify({ok,miss,structMiss,struct},null,1));
await b.close()})();
