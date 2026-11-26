(function(){'use strict';
var $=function(s,r){return (r||document).querySelector(s)},$$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};
var LS={get:function(k){try{return localStorage.getItem(k)}catch(e){return null}},set:function(k,v){try{localStorage.setItem(k,v)}catch(e){}}};
var rules=$$('details.rule');
/* theme */
var root=document.documentElement;var th=LS.get('ta-theme')||(window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');
function setTheme(t){root.setAttribute('data-theme',t);var b=$('#themebtn');if(b){b.setAttribute('aria-pressed',t==='dark');b.textContent=t==='dark'?'☀ Light':'🌙 Dark'}LS.set('ta-theme',t)}
setTheme(th);$('#themebtn').addEventListener('click',function(){setTheme(root.getAttribute('data-theme')==='dark'?'light':'dark')});
/* topbar height var + tools toggle */
function tb(){var h=$('#topbar').offsetHeight;root.style.setProperty('--tb',h+'px')}tb();window.addEventListener('resize',tb);if(window.ResizeObserver)new ResizeObserver(tb).observe($('#topbar'));
$('#toolsbtn').addEventListener('click',function(){var o=document.body.classList.toggle('tools-open');this.setAttribute('aria-expanded',o);tb()});
/* nav */
$('#hamb').addEventListener('click',function(){var o=document.body.classList.toggle('nav-open');this.setAttribute('aria-expanded',o)});
$$('#side a').forEach(function(a){a.addEventListener('click',function(){document.body.classList.remove('nav-open');$('#hamb').setAttribute('aria-expanded','false')})});
/* scroll spy */
var links={};$$('#side a[href^="#"]').forEach(function(a){links[a.getAttribute('href').slice(1)]=a});
if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){$$('#side a.active').forEach(function(x){x.classList.remove('active');x.removeAttribute('aria-current')});var a=links[e.target.id];if(a){a.classList.add('active');a.setAttribute('aria-current','true');if(a.scrollIntoView&&!document.body.classList.contains('nav-open')){var s=$('#side'),r=a.getBoundingClientRect(),sr=s.getBoundingClientRect();if(r.top<sr.top||r.bottom>sr.bottom)s.scrollTop+=r.top-sr.top-80}}}})},{rootMargin:'-70px 0px -70% 0px'});
$$('section.chapter').forEach(function(s){io.observe(s)})}
/* expand/collapse */
$('#expall').addEventListener('click',function(){rules.forEach(function(d){d.open=true})});$('#colall').addEventListener('click',function(){rules.forEach(function(d){d.open=false})});
/* progress */
function key(d){return 'ta-rev:'+d.id}
function prog(){var n=0,vis=rules.length;rules.forEach(function(d){if(d.classList.contains('reviewed'))n++});$('#progtxt').textContent=n+' / '+vis+' reviewed';$('#prog>i').style.width=(vis?100*n/vis:0)+'%';$('#prog').setAttribute('aria-valuenow',n);$('#prog').setAttribute('aria-valuemax',vis)}
rules.forEach(function(d){var cb=$('input.rv',d);if(!cb)return;var on=LS.get(key(d))==='1';cb.checked=on;d.classList.toggle('reviewed',on);cb.addEventListener('change',function(){d.classList.toggle('reviewed',cb.checked);LS.set(key(d),cb.checked?'1':'0');prog()})});
$('#progreset').addEventListener('click',function(){if(!confirm('Clear all “reviewed” marks?'))return;rules.forEach(function(d){LS.set(key(d),'0');d.classList.remove('reviewed');var c=$('input.rv',d);if(c)c.checked=false});prog()});prog();
/* search + filters */
var q=$('#q'),tmr;
function clearMarks(){$$('mark.sm').forEach(function(m){var p=m.parentNode;p.replaceChild(document.createTextNode(m.textContent),m);p.normalize()})}
function markIn(el,needle){var w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT,{acceptNode:function(n){var p=n.parentNode.nodeName;return /^(SCRIPT|STYLE|MARK)$/.test(p)||!n.nodeValue.trim()?NodeFilter.FILTER_REJECT:NodeFilter.FILTER_ACCEPT}});var ns=[],n;while((n=w.nextNode()))ns.push(n);var c=0;ns.forEach(function(t){var v=t.nodeValue,lv=v.toLowerCase(),i=lv.indexOf(needle);if(i<0)return;var frag=document.createDocumentFragment(),last=0;while(i>=0&&c<400){frag.appendChild(document.createTextNode(v.slice(last,i)));var m=document.createElement('mark');m.className='sm';m.textContent=v.slice(i,i+needle.length);frag.appendChild(m);last=i+needle.length;c++;i=lv.indexOf(needle,last)}frag.appendChild(document.createTextNode(v.slice(last)));t.parentNode.replaceChild(frag,t)});return c}
function apply(){clearMarks();var needle=q.value.trim().toLowerCase();var on=$$('.filters input:checked').map(function(c){return c.value});var shown=0,hits=0;
rules.forEach(function(d){var ok=true;if(on.length){var ty=(d.getAttribute('data-types')||'').split(' ');ok=on.some(function(t){return ty.indexOf(t)>-1})}
if(ok&&needle){var txt=(d.id+' '+(d.getAttribute('data-sl')||'')+' '+d.textContent).toLowerCase();ok=txt.indexOf(needle)>-1}
d.classList.toggle('is-hidden',!ok);if(ok){shown++;if(needle){d.open=true;hits+=markIn(d,needle)}}});
$$('[data-t].hlt').forEach(function(e){e.classList.remove('hlt')});if(on.length){on.forEach(function(t){$$('details.rule:not(.is-hidden) [data-t~="'+t+'"]').forEach(function(e){e.classList.add('hlt')})})}
$$('section.chapter').forEach(function(s){var any=$$('details.rule:not(.is-hidden)',s).length>0;s.classList.toggle('is-hidden',(needle||on.length)&&!any&&!$('.aidsec',s))});
$('#hits').textContent=(needle||on.length)?(shown+' of '+rules.length+' blocks'+(needle?' · '+hits+' highlights':'')):''}
q.addEventListener('input',function(){clearTimeout(tmr);tmr=setTimeout(apply,180)});$$('.filters input').forEach(function(c){c.addEventListener('change',apply)});
$('#clr').addEventListener('click',function(){q.value='';$$('.filters input').forEach(function(c){c.checked=false});apply();q.focus()});
/* keyboard */
document.addEventListener('keydown',function(e){var t=e.target.tagName;if(e.key==='Escape'){if($('#ov').classList.contains('on')){closeOv();return}}
if(/^(INPUT|TEXTAREA|SELECT)$/.test(t)||e.ctrlKey||e.metaKey||e.altKey)return;
if(e.key==='/'){e.preventDefault();q.focus()}
else if(e.key==='j'||e.key==='k'){var vs=rules.filter(function(d){return !d.classList.contains('is-hidden')});var cur=document.activeElement&&document.activeElement.closest?document.activeElement.closest('details.rule'):null;var i=vs.indexOf(cur);i=e.key==='j'?Math.min(vs.length-1,i+1):Math.max(0,i-1);if(vs[i]){var s=$('summary',vs[i]);s.focus();s.scrollIntoView({block:'center'})}}});
/* print */
var prior=[];window.addEventListener('beforeprint',function(){prior=rules.map(function(d){return d.open});$$('details').forEach(function(d){d.open=true})});window.addEventListener('afterprint',function(){var i=0;$$('details').forEach(function(d){if(d.classList.contains('rule')){d.open=prior[i++]}})});
/* data */
var DATA=JSON.parse($('#deckdata').textContent);var cards=DATA.cards,mcqs=DATA.mcqs;
function chOpts(sel){var seen={};var h='<option value="">All chapters</option>';(cards.concat(mcqs)).forEach(function(x){if(!seen[x.seg]){seen[x.seg]=1;h+='<option value="'+x.seg+'">'+x.segt+'</option>'}});sel.innerHTML=h}
var ov=$('#ov'),box=$('#ovbox'),lastFocus=null;
function openOv(html){lastFocus=document.activeElement;box.innerHTML=html;ov.classList.add('on');var f=$('button,select',box);if(f)f.focus()}
function closeOv(){ov.classList.remove('on');if(lastFocus)lastFocus.focus()}
ov.addEventListener('click',function(e){if(e.target===ov)closeOv()});
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
/* flashcards */
function flash(){var list=cards.slice(),i=0,flipped=false,seg='';
function shell(){return '<h2 id="ovt" style="margin-top:0">Flashcards <small>(study aid)</small></h2><div class="noprint"><label>Chapter <select id="fcseg"></select></label> <button class="btn" id="fcsh">Shuffle</button> <button class="btn" id="fcx">Close</button></div><p id="fcn" aria-live="polite"></p><div class="face" id="fcface" tabindex="0"></div><p><button class="btn" id="fcp">◀ Prev</button> <button class="btn" id="fcf" aria-pressed="false">Flip (Space)</button> <button class="btn" id="fcnx">Next ▶</button></p><p class="secmeta">Keys: ←/→ move · Space flips · Esc closes</p>'}
function draw(){var c=list[i];if(!c){$('#fcface').textContent='No cards.';return}$('#fcn').textContent='Card '+(i+1)+' of '+list.length+' · '+c.segt;$('#fcface').innerHTML=(flipped?'<b>Back</b><div>'+esc(c.b)+'</div>':'<b>Front</b><div>'+esc(c.f)+'</div>')+'<small class="secmeta">Source: '+esc(c.c)+'</small>';$('#fcf').setAttribute('aria-pressed',flipped)}
function filt(){list=cards.filter(function(c){return !seg||c.seg===seg});i=0;flipped=false;draw()}
openOv(shell());ov.setAttribute('aria-labelledby','ovt');chOpts($('#fcseg'));
$('#fcseg').addEventListener('change',function(){seg=this.value;filt()});$('#fcsh').addEventListener('click',function(){list.sort(function(){return Math.random()-.5});i=0;flipped=false;draw()});
$('#fcx').addEventListener('click',closeOv);$('#fcp').addEventListener('click',function(){i=(i-1+list.length)%list.length;flipped=false;draw()});$('#fcnx').addEventListener('click',function(){i=(i+1)%list.length;flipped=false;draw()});$('#fcf').addEventListener('click',function(){flipped=!flipped;draw()});
box.onkeydown=function(e){if(e.target.tagName==='SELECT')return;if(e.key==='ArrowRight'){$('#fcnx').click()}else if(e.key==='ArrowLeft'){$('#fcp').click()}else if(e.key===' '&&e.target.id==='fcface'){e.preventDefault();$('#fcf').click()}};draw()}
$('#fcbtn').addEventListener('click',flash);
/* quiz */
function quiz(){var list=mcqs.slice(),i=0,score=0,done=0,seg='',ans=false;
function shell(){return '<h2 id="ovt" style="margin-top:0">Quiz <small>(study aid — questions written for this guide)</small></h2><div class="noprint"><label>Chapter <select id="qzseg"></select></label> <button class="btn" id="qzsh">Shuffle</button> <button class="btn" id="qzx">Close</button></div><p id="qzn" aria-live="polite"></p><div id="qzq"></div><p id="qzs" aria-live="polite"></p>'}
function draw(){var el=$('#qzq');if(i>=list.length){el.innerHTML='<p><b>Finished.</b> Score: '+score+' / '+list.length+'</p><button class="btn" id="qzr">Restart</button>';$('#qzr').addEventListener('click',function(){i=0;score=0;done=0;draw()});$('#qzn').textContent='';$('#qzs').textContent='';return}
var m=list[i];ans=false;$('#qzn').textContent='Question '+(i+1)+' of '+list.length+' · '+m.segt;var h='<div class="face"><b>'+esc(m.q)+'</b></div><div class="opts" role="group" aria-label="Options">';m.o.forEach(function(o,k){h+='<button data-k="'+k+'">'+String.fromCharCode(97+k)+') '+esc(o)+'</button>'});h+='</div><div id="qzfb" aria-live="polite"></div>';el.innerHTML=h;$('#qzs').textContent='Score: '+score+' / '+done;
$$('.opts button',el).forEach(function(b){b.addEventListener('click',function(){if(ans)return;ans=true;done++;var k=+b.getAttribute('data-k');var ok=k===m.a;if(ok)score++;$$('.opts button',el).forEach(function(x,j){if(j===m.a)x.classList.add('good');else if(j===k)x.classList.add('bad');x.disabled=true});$('#qzfb').innerHTML='<p><b>'+(ok?'Correct.':'Answer: '+String.fromCharCode(97+m.a)+') '+esc(m.o[m.a]))+'</b> '+esc(m.w)+' <small>Source: '+esc(m.c)+'</small></p><button class="btn" id="qzn2">'+(i+1<list.length?'Next ▶':'See score')+'</button>';$('#qzs').textContent='Score: '+score+' / '+done;var nb=$('#qzn2');nb.focus();nb.addEventListener('click',function(){i++;draw()})})})}
function filt(){list=mcqs.filter(function(c){return !seg||c.seg===seg});i=0;score=0;done=0;draw()}
openOv(shell());ov.setAttribute('aria-labelledby','ovt');chOpts($('#qzseg'));$('#qzseg').addEventListener('change',function(){seg=this.value;filt()});$('#qzsh').addEventListener('click',function(){list.sort(function(){return Math.random()-.5});i=0;score=0;done=0;draw()});$('#qzx').addEventListener('click',closeOv);box.onkeydown=null;draw()}
$('#qzbtn').addEventListener('click',quiz);
/* inline flashcards */
$$('button.fcflip').forEach(function(b){b.addEventListener('click',function(){var a=b.nextElementSibling;var s=a.hidden;a.hidden=!s;b.setAttribute('aria-expanded',s)})});
window.__ta={rules:rules.length,cards:cards.length,mcqs:mcqs.length};
})();
