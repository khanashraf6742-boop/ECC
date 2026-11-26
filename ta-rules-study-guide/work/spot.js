const {chromium}=require('playwright');const path=require('path'),fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage();const L=fs.readFileSync(__dirname+'/source.html','utf8').split('\n');
let seed=20261122;const rnd=()=>{seed=(seed*1664525+1013904223)%4294967296;return seed/4294967296};
const cands=[];for(let n=745;n<=4340;n++){if(n>=3252&&n<=3255)continue;const t=L[n-1];if(t.replace(/<[^>]+>/g,'').trim().length>120&&!/<style|<script/.test(t))cands.push(n)}
const pick=[];while(pick.length<15){const n=cands[Math.floor(rnd()*cands.length)];if(!pick.includes(n))pick.push(n)}pick.sort((a,b)=>a-b);
await p.goto('file://'+path.resolve(__dirname,'../TA_Rules_Study_Guide.html'));
const res=await p.evaluate(lines=>{const norm=s=>s.replace(/\s+/g,'');const main=norm(document.querySelector('main').textContent);return lines.map(([n,h])=>{const d=document.createElement('div');d.innerHTML=h;const t=d.textContent.trim();const tn=norm(t);return {n,len:t.length,found:main.includes(tn),sample:t.slice(0,70)}})},pick.map(n=>[n,L[n-1]]));
res.forEach(r=>console.log(r.found?'OK  ':'FAIL','L'+r.n,'('+r.len+' chars)',JSON.stringify(r.sample)));console.log(res.filter(r=>r.found).length+'/15 exact');await b.close()})();
