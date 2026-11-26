(function(){'use strict';
var $=function(s,r){return (r||document).querySelector(s)},$$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};
var LS={get:function(k){try{return localStorage.getItem(k)}catch(e){return null}},set:function(k,v){try{localStorage.setItem(k,v)}catch(e){}}};
var DATA=JSON.parse($('#deckdata').textContent),cards=DATA.cards,mcqs=DATA.mcqs;
var ov=$('#ov'),box=$('#ovbox'),last=null;
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function open(html){last=document.activeElement;box.innerHTML=html;box.onkeydown=null;ov.classList.add('on');ov.setAttribute('aria-labelledby','ovt');var f=$('button,select',box);if(f)f.focus()}
function close(){ov.classList.remove('on');if(timer){clearInterval(timer);timer=null}if(last)last.focus()}
var timer=null;
function hash(s){var h=5381;for(var i=0;i<s.length;i++)h=((h<<5)+h+s.charCodeAt(i))|0;return 'h'+(h>>>0).toString(36)}
cards.forEach(function(c){c.id=hash(c.seg+'|'+c.f)});mcqs.forEach(function(m){m.id=hash(m.seg+'|'+m.q)});
function chOpts(extra){var seen={},h='<option value="">All chapters</option>';cards.concat(mcqs).forEach(function(x){if(!seen[x.seg]){seen[x.seg]=1;h+='<option value="'+x.seg+'">'+esc(x.segt)+'</option>'}});return h}
/* ---------- spaced repetition (Leitner boxes) ---------- */
var INT=[0,1,3,7,16],DAY=86400000;
function srsLoad(){try{return JSON.parse(LS.get('ta-srs')||'{}')}catch(e){return {}}}
function srsSave(d){LS.set('ta-srs',JSON.stringify(d))}
function srs(){var st=srsLoad(),seg='';
function stats(){var now=Date.now(),nw=0,due=0,lr=0;cards.forEach(function(c){var s=st[c.id];if(seg&&c.seg!==seg)return;if(!s)nw++;else{if(s.due<=now)due++;if(s.box>=4)lr++}});return {nw:nw,due:due,lr:lr}}
function queue(){var now=Date.now();return cards.filter(function(c){if(seg&&c.seg!==seg)return false;var s=st[c.id];return !s||s.due<=now}).sort(function(a,b){var sa=st[a.id],sb=st[b.id];return (sa?sa.due:0)-(sb?sb.due:0)})}
var q=queue(),i=0,shown=false;
function shell(){return '<h2 id="ovt" style="margin-top:0">Spaced review <small>(study aid)</small></h2><div class="noprint"><label>Chapter <select id="sseg">'+chOpts()+'</select></label> <button class="btn" id="sx">Close</button> <button class="btn" id="srst">Reset schedule</button></div><p id="sst" aria-live="polite"></p><div class="face" id="sface" tabindex="0"></div><p id="sbt"></p><p class="secmeta">Boxes 1–5 re-appear after 0, 1, 3, 7 and 16 days. “Again” = source check: it returns tomorrow’s first and goes back to box 1. Progress is saved in this browser only.</p>'}
function draw(){var s=stats();$('#sst').textContent='New: '+s.nw+' · Due: '+s.due+' · Learned (box 5): '+s.lr+' · In this session: '+(q.length-i);var c=q[i];var f=$('#sface'),b=$('#sbt');if(!c){f.innerHTML='<b>Nothing due.</b><div>Come back later, or pick another chapter.</div>';b.innerHTML='';return}
var cs=st[c.id];f.innerHTML='<small class="secmeta">'+esc(c.segt)+' · box '+(cs?cs.box+1:'new')+'</small><b>'+(shown?'Back':'Front')+'</b><div>'+esc(shown?c.b:c.f)+'</div>'+(shown?'<small class="secmeta">Source: '+esc(c.c)+'</small>':'');
b.innerHTML=shown?'<button class="btn" data-g="0">Again (source check)</button> <button class="btn" data-g="1">Unsure</button> <button class="btn" data-g="2">Know it</button>':'<button class="btn" id="sshow">Show answer</button>';
var bb=$('#sshow');if(bb){bb.focus();bb.addEventListener('click',function(){shown=true;draw()})}else{$$('button[data-g]',b).forEach(function(x){x.addEventListener('click',function(){grade(+x.getAttribute('data-g'))})});$('button[data-g="2"]',b).focus()}}
function grade(g){var c=q[i],s=st[c.id]||{box:0},now=Date.now();if(g===0){s.box=0;s.due=now+DAY;q.push(c)}else if(g===1){s.box=Math.max(s.box,0);s.due=now+Math.max(DAY,INT[Math.min(s.box,4)]*DAY)}else{s.box=Math.min(4,s.box+1);s.due=now+INT[s.box]*DAY}
st[c.id]=s;srsSave(st);i++;shown=false;draw()}
open(shell());$('#sseg').addEventListener('change',function(){seg=this.value;q=queue();i=0;shown=false;draw()});$('#sx').addEventListener('click',close);$('#srst').addEventListener('click',function(){if(confirm('Reset the whole review schedule?')){st={};srsSave(st);q=queue();i=0;shown=false;draw()}});draw()}
$('#srsbtn').addEventListener('click',srs);
/* ---------- practice exam ---------- */
function missLoad(){try{return JSON.parse(LS.get('ta-miss')||'{}')}catch(e){return {}}}
function exam(){var miss=missLoad();
function setup(){var nm=Object.keys(miss).length;open('<h2 id="ovt" style="margin-top:0">Practice exam <small>(study aid)</small></h2><form id="exf"><p><label>Chapter <select id="eseg">'+chOpts()+'</select></label></p><p><label>Questions <select id="enum"><option>10</option><option selected>20</option><option>30</option><option value="999">All available</option></select></label> <label>Time per question <select id="etim"><option value="0">Untimed</option><option value="45">45 s</option><option value="60" selected>60 s</option><option value="90">90 s</option></select></label></p><p><label><input type="checkbox" id="ewk"> Weak spots only ('+nm+' missed so far)</label></p><p><button class="btn" type="submit">Start exam</button> <button class="btn" type="button" id="ex">Close</button></p></form><p class="secmeta">No answers are shown until you finish. Questions were written for this guide; each answer cites its source block or official order.</p>');
$('#ex').addEventListener('click',close);$('#exf').addEventListener('submit',function(e){e.preventDefault();start($('#eseg').value,+$('#enum').value,+$('#etim').value,$('#ewk').checked)})}
function start(seg,n,tl,weak){var pool=mcqs.filter(function(m){return (!seg||m.seg===seg)&&(!weak||miss[m.id])});pool.sort(function(){return Math.random()-.5});pool=pool.slice(0,n);if(!pool.length){open('<h2 id="ovt">Practice exam</h2><p>No questions match. '+(weak?'You have no recorded weak spots in this selection.':'')+'</p><button class="btn" id="eb">Back</button>');$('#eb').addEventListener('click',setup);return}
var ans=[],i=0,left=tl*pool.length;
function draw(){var m=pool[i];var h='<h2 id="ovt" style="margin-top:0">Question '+(i+1)+' of '+pool.length+'</h2><p class="secmeta">'+esc(m.segt)+(tl?' · <span id="etm" aria-live="off"></span>':'')+'</p><div class="face"><b>'+esc(m.q)+'</b></div><div class="opts" role="group" aria-label="Options">';m.o.forEach(function(o,k){h+='<button data-k="'+k+'"'+(ans[i]===k?' class="good"':'')+'>'+String.fromCharCode(97+k)+') '+esc(o)+'</button>'});h+='</div><p><button class="btn" id="ep"'+(i?'':' disabled')+'>◀ Back</button> <button class="btn" id="en">'+(i+1<pool.length?'Next ▶':'Finish')+'</button> <button class="btn" id="ex2">Abandon</button></p>';open(h);
$$('.opts button',box).forEach(function(b){b.addEventListener('click',function(){ans[i]=+b.getAttribute('data-k');$$('.opts button',box).forEach(function(x){x.classList.remove('good')});b.classList.add('good')})});
$('#ep').addEventListener('click',function(){i--;draw()});$('#en').addEventListener('click',function(){if(i+1<pool.length){i++;draw()}else finish()});$('#ex2').addEventListener('click',close);tick()}
function tick(){var e=$('#etm');if(!tl||!e)return;var mm=Math.floor(left/60),ss=left%60;e.textContent='Time left: '+mm+':'+(ss<10?'0':'')+ss}
function startTimer(){if(!tl)return;timer=setInterval(function(){if(!ov.classList.contains('on')){clearInterval(timer);timer=null;return}left--;tick();if(left<=0){clearInterval(timer);timer=null;finish()}},1000)}
function finish(){if(timer){clearInterval(timer);timer=null}var sc=0,h='';pool.forEach(function(m,k){var ok=ans[k]===m.a;if(ok){sc++;delete miss[m.id]}else miss[m.id]=1;h+='<li class="'+(ok?'':'bad')+'"><b>'+esc(m.q)+'</b><br>Your answer: '+(ans[k]===undefined?'<i>none</i>':String.fromCharCode(97+ans[k])+') '+esc(m.o[ans[k]]))+'<br>Correct: '+String.fromCharCode(97+m.a)+') '+esc(m.o[m.a])+' — '+esc(m.w)+' <small>Source: '+esc(m.c)+'</small></li>'});LS.set('ta-miss',JSON.stringify(miss));
open('<h2 id="ovt" style="margin-top:0">Result</h2><p><b>Score: '+sc+' / '+pool.length+' ('+Math.round(100*sc/pool.length)+'%)</b> — study aid only; the pass mark of your real exam is not known to this guide.</p><p><button class="btn" id="er">New exam</button> <button class="btn" id="ex3">Close</button></p><ol class="exrev">'+h+'</ol>');$('#er').addEventListener('click',setup);$('#ex3').addEventListener('click',close)}
draw();startTimer()}
setup()}
$('#exbtn').addEventListener('click',exam);
/* ---------- calculators (offline; learning aids) ---------- */
var BASE={hotel:{L14:7500,L12:4500,L9:2250,L6:750,L5:450},taxi:{L9:338,L6:225,L5:113},food:{L14:1200,L12:1000,L9:900,L6:800,L5:500},km:{car:24,auto:12,foot:12},eff:{L6:50,L5:25,L4:15}};
function mult(){return $('#c-rates').value==='base'?1:1.25}
function rs(n){return '₹'+(Math.round(n*100)/100).toLocaleString('en-IN',{minimumFractionDigits:2,maximumFractionDigits:2})}
function lvl(v){return v}
function calc(){
var m=mult();
// food DA
var fl=$('#c-flevel').value,hrs=$('#c-hours').value.split(/[,\s]+/).filter(Boolean).map(Number),lump=BASE.food[fl]*m,tot=0,det=[];
hrs.forEach(function(h,i){if(isNaN(h)||h<0||h>24){det.push('Day '+(i+1)+': enter hours 0–24');return}var p=h<6?.3:(h<=12?.7:1);tot+=lump*p;det.push('Day '+(i+1)+': '+h+' h → '+Math.round(p*100)+'% = '+rs(lump*p))});
$('#o-food').innerHTML='Food lump sum '+rs(lump)+'/day. '+det.join('; ')+'. <b>Total '+rs(tot)+'</b>. (Exactly 6 h or 12 h is shown in the 6–12 h band; the O.M. says “between 6–12 hours”.)';
// hotel + GST
var hl=$('#c-hlevel').value,ceil=BASE.hotel[hl]*m,t=+$('#c-tariff').value||0,g=(+$('#c-gst').value||0)/100,nn=+$('#c-nights').value||1,within=Math.min(t,ceil);
$('#o-hotel').innerHTML='Ceiling '+rs(ceil)+'/night (GST excluded). Rent reimbursed '+rs(within)+' + GST on that amount '+rs(within*g)+' = <b>'+rs((within+within*g)*nn)+'</b> for '+nn+' night(s). Excess tariff and excess GST are borne by the employee. (O.M. 29.06.2018.) Class-X voucher clause for Levels 8 and below is not modelled.';
// CTG
var bp=+$('#c-basic').value||0,cs=$('#c-ctg').value,r={t20:[.8,'Transfer ≥ 20 km: 80%'],t20r:[.8/3,'Transfer < 20 km / same city with actual residence change: one-third of 80%'],t20n:[0,'Transfer < 20 km / same city, no residence change: nil'],isl:[1,'A&N / Lakshadweep: 100%'],sp50:[.4,'Spouse transferred later (> 60 days after the first, ≥ 20 km): 50% of the normal grant'],sp0:[0,'Spouse transferred later within 60 days: no grant'],rr:[.8,'Retirement with actual change of residence: 80%'],rn:[0,'Retirement without change of residence: nil']}[cs];
$('#o-ctg').innerHTML=r[1]+' → <b>'+rs(bp*r[0])+'</b> on last month’s basic pay '+rs(bp)+' (NPA/MSP excluded from basic pay).';
// mileage
var md=$('#c-mode').value,km=+$('#c-km').value||0,dead=$('#c-dead').checked,bill=dead&&md==='car'?Math.max(0,km-1):km;
$('#o-mile').innerHTML=km+' km × '+rs(BASE.km[md]*m)+'/km'+(dead&&md==='car'?' (first km deducted — this is NOT in the 2017 O.M.)':'')+' = <b>'+rs(bill*BASE.km[md]*m)+'</b>. State-notified rates override these defaults where they exist.';
// effects
var el=$('#c-elevel').value,ek=+$('#c-ekm').value||0;$('#o-eff').innerHTML=ek+' km × '+rs(BASE.eff[el]*m)+'/km = <b>'+rs(ek*BASE.eff[el]*m)+'</b>. Vouchers are mandatory (including NER/A&N/Lakshadweep/Ladakh, subject to the 16.06.2022 relaxation).';
// deadline
var dv=$('#c-date').value,ty=$('#c-claim').value;if(dv){var d=new Date(dv+'T00:00:00'),days=ty==='ret'?180:60,a=new Date(d.getTime()+days*DAY),b=new Date(d.getTime()+(days+1)*DAY),f=function(x){return x.toLocaleDateString('en-GB',{day:'2-digit',month:'short',year:'numeric'})};
$('#o-dead').innerHTML='Journey completed '+f(d)+'. O.M. reading (“within '+days+' days succeeding the date of completion”): last day <b>'+f(a)+'</b>. GFR 290 reading (due the next day, then '+days+' days): '+f(b)+'. Plan to the earlier date. This does not cover advance adjustment, LTC or family/effects triggers.'}else $('#o-dead').textContent='Enter the date the journey was completed.'}
$$('#sec-calc input,#sec-calc select').forEach(function(e){e.addEventListener('input',calc);e.addEventListener('change',calc)});calc();
})();
