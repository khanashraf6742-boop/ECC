const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:900}});const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
await p.goto('file://'+path.resolve(__dirname,'../TA_Rules_Study_Guide.html'));const r={};
// calculators
r.food=await p.textContent('#o-food');r.hotel=await p.textContent('#o-hotel');r.ctg=await p.textContent('#o-ctg');r.mile=await p.textContent('#o-mile');r.eff=await p.textContent('#o-eff');r.dead=await p.textContent('#o-dead');
await p.selectOption('#c-ctg','sp50');r.sp=await p.textContent('#o-ctg');
// SRS
await p.click('#srsbtn');r.srs1=(await p.textContent('#sst'));await p.click('#sshow');await p.click('button[data-g="2"]');r.srs2=await p.textContent('#sst');r.ls=await p.evaluate(()=>Object.keys(JSON.parse(localStorage.getItem('ta-srs'))).length);await p.keyboard.press('Escape');
// exam
await p.click('#exbtn');await p.selectOption('#enum','10');await p.selectOption('#etim','0');await p.click('#exf button[type=submit]');
for(let i=0;i<10;i++){await p.click('.opts button >> nth=0');await p.click('#en')}
r.res=(await p.textContent('#ovbox')).slice(0,90);r.miss=await p.evaluate(()=>Object.keys(JSON.parse(localStorage.getItem('ta-miss')||'{}')).length);
await p.click('#er');await p.check('#ewk');await p.click('#exf button[type=submit]');r.weakQ=(await p.textContent('#ovt'));await p.keyboard.press('Escape');
r.mcqs=await p.evaluate(()=>window.__ta.mcqs);
await p.addStyleTag({content:'html{scroll-behavior:auto!important}'});await p.evaluate(()=>document.getElementById('sec-calc').scrollIntoView());await p.waitForTimeout(400);await p.screenshot({path:'shot-calc.png'});
console.log(JSON.stringify(r,null,1));console.log('ERR',errs);await b.close()})();
