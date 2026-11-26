p = 'build.js'
s = open(p).read()

sup_js = r'''// ---------- superseded passages (collapsed, never deleted) ----------
const SUPERSEDED=[
 ['Under the base O.M. dated 13.07.2017, retired employees settling','Superseded by DoE O.M. 06.01.2022 (retirement CTG: 20-km condition removed)'],
 ['The 25% Flat DA Abolition: Under 5th','Superseded by DoE O.M. 01.02.2018 (flat 25% DA discontinued)'],
 ['Purana rule (6th CPC): Pehle agar stay aur food dono free','Superseded by DoE O.M. 01.02.2018 (flat 25% DA discontinued)'],
 ['16.02.2022No. 19024/03/2021-E.IVEarlier best-available-fare','Superseded by DoE O.M. 16.06.2022 para 16 (supersedes all earlier air instructions); content also mis-described — see E6'],
 ['2. DoE O.M. of even number dated 16.02.2022 (Guidelines on Best Available Fare)','Superseded by DoE O.M. 16.06.2022 para 16; the 16.02.2022 O.M. itself only allowed private airlines — see E6']];
const supStats=[];
function markSup(html){
  const one=(m,open,a,b)=>{const t=strip(b).replace(/\s+/g,' ');const e=SUPERSEDED.find(x=>t.startsWith(x[0].replace(/\s+/g,' ')));if(!e)return null;supStats.push(e[1]);const cls=/class="/.test(a)?a.replace(/class="/,'class="sup '):a+' class="sup"';return `<${open}${cls} data-sup="${esc(e[1])}">`;};
  html=html.replace(/<li\b([^>]*)>([\s\S]*?)(?=<\/li>|<li\b|<\/ul>)/g,(m,a,b)=>{const r=one(m,'li',a,b);return r?r+b:m});
  html=html.replace(/<tr\b([^>]*)>([\s\S]*?)<\/tr>/g,(m,a,b)=>{const r=one(m,'tr',a,b);return r?r+b+'</tr>':m});
  html=html.replace(/<p\b([^>]*)>([\s\S]*?)(?=<\/p>)/g,(m,a,b)=>{const r=one(m,'p',a,b);return r?r+b:m});
  return html;
}
'''
s = s.replace("// ---------- render ----------", sup_js + "// ---------- render ----------", 1)
s = s.replace("  let inner=autolink(tagInner(body),p,collect);",
              "  let inner=autolink(markSup(tagInner(body)),p,collect);\n  const nSup=(inner.match(/class=\"sup\\b|class=\"sup /g)||[]).length;")
s = s.replace("<span>Source ${sl}</span><label>",
              "<span>Source ${sl}</span>${nSup?`<span class=\"tb tb-exception\">${nSup} superseded line${nSup>1?'s':''} hidden — use “Show superseded”</span>`:''}<label>")
s = s.replace('<button id="fcbtn">Flashcards</button>',
              '<button id="supbtn" aria-pressed="false">Show superseded</button><button id="fcbtn">Flashcards</button>')
s = s.replace("<li><b>Amber “Official-text check” boxes</b>",
              "<li><b>Superseded rules</b> (old one-third retirement CTG, flat 25% DA, the 16.02.2022 air entry) are collapsed and labelled; nothing is deleted — use “Show superseded” to see them. The ledger lists each one.</li><li><b>Amber “Official-text check” boxes</b>")
s = s.replace("['22 Nov 2026','Source document", "['26 Nov 2026','Superseded passages collapsed and labelled (5 lines); not deleted.'],\n['22 Nov 2026','Source document") if False else s
open(p, 'w').write(s)

m = open('meta.js').read()
m = m.replace("const LOG=[\n", "const LOG=[\n['26 Nov 2026','Five source passages describing rules replaced by later official orders are collapsed and labelled “Superseded” (not deleted); toggle with “Show superseded”.'],\n")
open('meta.js', 'w').write(m)

a = open('assets/app2.js').read()
i = a.rindex('})();')
a = a[:i] + r'''var sb=$('#supbtn');if(sb)sb.addEventListener('click',function(){var o=document.body.classList.toggle('show-sup');sb.setAttribute('aria-pressed',o);sb.textContent=o?'Hide superseded':'Show superseded'});
''' + a[i:]
open('assets/app2.js', 'w').write(a)

open('assets/style.css', 'a').write('''
.sup{display:none!important}body.show-sup .sup{display:revert!important;opacity:.85;background:var(--bad-bg)}body.show-sup .sup:before{content:"SUPERSEDED — " attr(data-sup);display:block;font:700 .72rem/1.3 system-ui;color:var(--bad);margin-bottom:2px}
@media print{.sup{display:none!important}}
''')

l = open('ledger.js').read()
l = l.replace("## Totals", "## Superseded passages (collapsed and labelled, not deleted)\n- L1743 (ch07-013): old one-third retirement CTG statement — superseded by O.M. 06.01.2022\n- L1628 (ch07-008) and L1635 (Hinglish): flat 25% DA — superseded by O.M. 01.02.2018\n- L1544 (ch07-004): 16.02.2022 air row — superseded by O.M. 16.06.2022 para 16\n- L1849–1850 (ch07-017): 16.02.2022 “Best Available Fare” item — superseded by O.M. 16.06.2022 para 16\n\n## Totals", 1)
open('ledger.js', 'w').write(l)
