const fs=require('fs');const {build,strip}=require('./classify');
const data=build();
function txt(html){
  html=html.replace(/<div class="simple">[\s\S]*?<\/ul>\s*<\/div>/g,'[Hinglish block omitted from dump]');
  html=html.replace(/<\/(tr)>/g,'\n').replace(/<\/(th|td)>/g,' | ').replace(/<\/(p|li|h[1-6]|div|summary|details|caption)>/g,'\n');
  return strip(html.replace(/\n/g,'¶')).replace(/¶ ?/g,'\n').replace(/ +\n/g,'\n');
}
for(const s of data){let o='';for(const p of s.pieces){if(['comment','anchor','study-map','chapter-banner'].includes(p.type)&&p.type!=='study-map'&&p.type!=='chapter-banner')continue;o+=`\n### [${p.id}] ${p.type} L${p.l1}-${p.l2} ${p.head}\n`+txt(p.html)+'\n';}
 fs.writeFileSync(`dump/${s.key}.txt`,o);console.log(s.key,o.length);}
