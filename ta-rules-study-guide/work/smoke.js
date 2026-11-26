const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:900},deviceScaleFactor:1});const errs=[];
p.on('console',m=>{if(m.type()==='error')errs.push('console: '+m.text())});p.on('pageerror',e=>errs.push('pageerror: '+e.message));p.on('requestfailed',r=>errs.push('reqfail '+r.url()));
await p.goto('file://'+path.resolve(__dirname,'../TA_Rules_Study_Guide.html'));await p.waitForTimeout(500);
const r={};r.rules=await p.$$eval('details.rule',e=>e.length);r.ta=await p.evaluate(()=>window.__ta);
// search
await p.fill('#q','Composite Transfer');await p.waitForTimeout(500);r.searchShown=await p.$$eval('details.rule:not(.is-hidden)',e=>e.length);r.marks=await p.$$eval('mark.sm',e=>e.length);r.hits=await p.textContent('#hits');
await p.fill('#q','ch05-004');await p.waitForTimeout(400);r.byNumber=await p.$$eval('details.rule:not(.is-hidden)',e=>e.map(x=>x.id));
await p.click('#clr');await p.waitForTimeout(300);
// filter
await p.check('.filters input[value=faq]');await p.waitForTimeout(300);r.faqShown=await p.$$eval('details.rule:not(.is-hidden)',e=>e.length);await p.uncheck('.filters input[value=faq]');
// toc click + spy
await p.click('#side a[href="#sec-ch05"]');await p.waitForTimeout(1800);r.active=await p.$$eval('#side a.active',e=>e.map(x=>x.getAttribute('href')));
// collapse/expand
await p.click('#colall');r.closed=await p.$$eval('details.rule[open]',e=>e.length);await p.click('#expall');r.opened=await p.$$eval('details.rule[open]',e=>e.length);
// reviewed
await p.evaluate(()=>{document.getElementById('ch05-004').scrollIntoView()});await p.check('#ch05-004 input.rv');r.rev=await p.textContent('#progtxt');
// flashcards
await p.click('#fcbtn');await p.waitForTimeout(200);r.fc1=await p.textContent('#fcface');await p.click('#fcf');r.fc2=await p.textContent('#fcface');await p.keyboard.press('Escape');
// quiz
await p.click('#qzbtn');await p.click('.opts button >> nth=0');r.qz=await p.textContent('#qzfb');await p.keyboard.press('Escape');
// theme
await p.click('#themebtn');r.theme=await p.getAttribute('html','data-theme');
// anchors
r.badAnchors=await p.evaluate(()=>{const bad=[];document.querySelectorAll('a[href^="#"]').forEach(a=>{const id=decodeURIComponent(a.getAttribute('href').slice(1));if(id&&!document.getElementById(id))bad.push(id)});return [...new Set(bad)]});
r.dupIds=await p.evaluate(()=>{const s={},d=[];document.querySelectorAll('[id]').forEach(e=>{if(s[e.id])d.push(e.id);s[e.id]=1});return d});
await p.screenshot({path:'shot-desktop.png'});
const m=await b.newPage({viewport:{width:390,height:800},deviceScaleFactor:1});await m.goto('file://'+path.resolve(__dirname,'../TA_Rules_Study_Guide.html'));await m.waitForTimeout(400);await m.click('#hamb');await m.waitForTimeout(300);await m.screenshot({path:'shot-mobile-menu.png'});await m.click('#side a[href="#sec-ch03"]');await m.waitForTimeout(2500);await m.screenshot({path:'shot-mobile.png'});
r.hscroll=await m.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth+2);
console.log(JSON.stringify(r,null,1));console.log('ERRORS',errs);await b.close()})();
