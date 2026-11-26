import re

# ---------------- frsr.js: drop rows replaced by reproduced text; keep residual secondary SR 71 items; update notes, MCQs, cards
p = 'frsr.js'
s = open(p).read()


def drop_row(s, rid):
    a = s.index("['" + rid + "'")
    # a row ends at the line that ends with "'],\n" or "']];"
    m = re.compile(r"\],\n(?=\[')|\]\];").search(s, a)
    end = m.end()
    return s[:a] + s[end:] if m.group(0) == "],\n" else s[:a].rstrip(",\n") + "];" + s[end:]


for rid in ['frsr-147', 'frsr-148', 'frsr-164']:
    s = drop_row(s, rid)

# residual SR 71 row: only the items NOT in the reproduced text
a = s.index("['frsr-71'")
b = s.index("],\n", a) + 3
s = s[:a] + """['frsr-71', ['sr-71-sec'], 'SR 71(2), clarifications and SR 72–73 extracts (not in the reproduced text)',
 'SR 71(2): TA for a local journey is admissible if the temporary place of duty is beyond 8 km from the normal place of duty, whether the journey starts from residence or office. After the 7th CPC, DA on tour has three components (hotel, travel within the city, food) and for a local journey beyond 8 km the prescribed components may be admissible. Practice: journeys beyond 8 km inside the urban agglomeration/municipality of headquarters are normally by bus, local train or own conveyance, as for the journey to the duty point. G.I.O.(4): DA on local journeys up to 180 days (one secondary training document). SR 72–73 extracts: a railway journey combined with steamer/road travel to a place at least eight kilometres from the railhead earns mileage for that leg with the time deducted from absence; evidence in a court within eight kilometres of headquarters earns no TA, and the court’s actual-expense payment may be accepted if no permanent TA is drawn.',
 SEC+' · '+UNRES+' for the at-or-below-8-km case', 'Staff News 2018; MCR HRDI; Lawyers Club India; Works Accounts FR-SR PDF'],
""" + s[b:]
s = s.replace("'A secondary summary of “SR-116” lists:", "'The reproduced text of SR 114 and SR 116 is given below; a secondary summary of “SR-116” also lists:")
s = s.replace("module.exports = {ROWS,", "const TEXTMAP = {'sr-71':'frsrt-71','sr-72':'frsrt-72','sr-73':'frsrt-73','sr-114':'frsrt-114','sr-116':'frsrt-116','sr-147':'frsrt-147','sr-148':'frsrt-148','sr-164':'frsrt-164'};\nmodule.exports = {TEXTMAP, ROWS,")
# discrepancies
s = s.replace(" ['SR 147 and SR 116 roles',", " ['SR 147 and SR 116 roles (secondary summary)',")
s = s.replace("'Official O.M. prevails; the compilation’s labels are not relied on.'", "'The reproduced SR text confirms SR 114 = transfer (public convenience), SR 116 = transfer entitlements, SR 147 = discretion for journeys of the kind in Rule 146 (retirement). The “SR 147 = Transfer TA” label is wrong.'")
s = s.replace("'The figure, if it exists, comes from FR/SR commentary, not the O.M.; keep it unverified.'", "'The reproduced text states that SR 73 is not printed and that Government orders give full DA for the first 180 days of a continuous halt and nil thereafter — so the figure comes from a GIO under SR 73, not the O.M. The GIO text itself was not seen.'")
s = s.replace("];\nconst MCQ", ",\n ['SR 164 clause (c)','The earlier secondary summary lists clause (c) (journeys during the course of training); the reproduced text lists only (a) and (b) plus the proviso.','[uncertain] — check against the official text.']];\nconst MCQ", 1) if False else s
open(p, 'w').write(s)

f = open(p).read()
f = f.replace("const MCQ = [", """const MCQ = [
{q:'SR 114 (reproduced text): a transfer at the Government servant’s own request is treated as a transfer for the public convenience:',o:['Always','Unless the authority, for recorded special reasons, otherwise directs it to be treated so — i.e. normally not','Only for Level 9+','Only within 20 km'],a:1,w:'SR 114: own-request transfer is not a transfer for public convenience unless the sanctioning authority, for special reasons recorded, otherwise directs.',c:'SR 114 (reproduced text)'},
{q:'SR 116(b)(iii) (reproduced text): a family member who follows within ___ of the transfer, or precedes by not more than one month, is treated as accompanying.',o:['One month','Three months','Six months','One year'],a:2,w:'Time limits extendable by the competent authority in special circumstances.',c:'SR 116(b)(iii)'},
{q:'SR 148 (reproduced text) provides that:',o:['The family gets TA at a fixed scale','A competent authority may grant the family of a servant who dies in service such TA as it deems fit','Only a 75% advance is allowed','No TA is ever admissible'],a:1,w:'One-sentence rule; the GIOs below it carry the detail.',c:'SR 148'},
""", 1)
f = f.replace("const CARDS = [", """const CARDS = [
['SR 114 in one line?','No TA on transfer unless it is for the public convenience and pay is drawn during the journey; own-request transfer does not qualify unless recorded special reasons direct otherwise.','SR 114'],
['SR 147 in one line?','A competent authority may, for recorded special reasons, allow TA for a journey of the kind in Rule 146 (retirement-type journeys).','SR 147'],
""", 1)
open(p, 'w').write(f)

# ---------------- build.js: reproduced SR text section from the user's markdown
p = 'build.js'
s = open(p).read()
blk = r'''// reproduced SR text (user-supplied markdown; verbatim)
const srMd=fs.readFileSync(path.join(__dirname,'official','user_SR_exact_text.md'),'utf8');
const mdInline=t=>esc(t).replace(/\*\*([^*]+)\*\*/g,'<b>$1</b>').replace(/\*([^*]+)\*/g,'<i>$1</i>');
const srSecs=srMd.split(/\n(?=## S\.R\. )/).filter(x=>x.startsWith('## S.R.')).map(x=>{const lines=x.replace(/\n---\s*$/,'').split('\n');const m=/^## S\.R\. (\d+)/.exec(lines[0]);const n=m[1];let h='';lines.slice(1).forEach(l=>{l=l.trimEnd();if(!l)return;if(/^### /.test(l))h+=`<h4>${mdInline(l.slice(4))}</h4>`;else if(/^\*Sources:/.test(l)||/^---/.test(l))return;else h+=`<p>${mdInline(l)}</p>`});return {n,id:'frsrt-'+n,h}});
const srTextHtml=srSecs.map(x=>{offIdx.push({seg:'off',id:x.id,head:'SR '+x.n+' — reproduced text',type:'card',sl:'reproduced'});return `<details class="rule" id="${x.id}" data-types="proviso exception" data-sl="reproduced" open><summary><span class="rno" data-chrome="1">${x.id}</span><h3>S.R. ${x.n} — reproduced rule text</h3><span class="tb tb-proviso" data-chrome="1">Proviso</span></summary><div class="rbody"><div class="rtools" data-chrome="1"><span>Reproduced text · not checked against an official host</span><label><input type="checkbox" class="rv" aria-label="Mark ${x.id} as reviewed"> Reviewed</label></div><div class="verbatim">${x.h}</div></div></details>`}).join('');
'''
s = s.replace("const frsrHtml=`", blk + "const frsrHtml=`", 1)
s = s.replace("<details class=\"rule\" id=\"off-frsr\"", "<p class=\"secmeta\"><b>Reproduced rule text.</b> The next blocks give the text of SR 71–73, 114, 116, 147, 148 and 164 exactly as supplied by you. The supplied file names its own sources as reproductions on worksaccounts.com, kupdf.net and teachmint — so it is rule text, but it is <i>not</i> checked against an official DoPT/DoE host. Gaps inside it (“Not printed”) are the reproduction’s own.</p>${srTextHtml}<details class=\"rule\" id=\"off-frsr\"", 1)
s = s.replace("const FRMAP={};FRSR.ROWS.forEach(r=>r[1].forEach(k=>FRMAP[k]=r[0]));", "const FRMAP={};FRSR.ROWS.forEach(r=>r[1].forEach(k=>FRMAP[k]=r[0]));Object.assign(FRMAP,FRSR.TEXTMAP);")
s = s.replace("<a href=\\\"#${FRMAP[k]}\\\">FR/SR summary (secondary)</a>", "<a href=\\\"#${FRMAP[k]}\\\">${/^frsrt/.test(FRMAP[k])?'reproduced SR text':'FR/SR summary (secondary)'}</a>")
open(p, 'w').write(s)

# ---------------- official.js errata updates + register row
o = open('official.js').read()
o = o.replace("['E16','SR 147 as “Transfer TA” and SR 116 as “general TA” in the supplied FR/SR compilation (CSD Rates summary).'", "['E16','SR 147 as “Transfer TA” and SR 116 as “general TA” in the first supplied FR/SR compilation (CSD Rates summary).'")
o = o.replace("'Use the official roles of SR 114 / 116 / 147.'", "'Confirmed by the reproduced SR text (supplied later): SR 114 = transfer for the public convenience; SR 116 = transfer entitlements; SR 147 = competent-authority discretion for journeys of the kind in Rule 146. Use these roles.'")
o = o.replace("'If it exists it comes from FR/SR commentary; keep it unverified.'", "'The reproduced SR text says SR 73 is not printed and that Government orders give full DA for 180 days of continuous halt, nil thereafter — a GIO under SR 73, not the 2017 O.M. The GIO text itself was not seen; keep unverified.'")
row = "['Reproduced text of SR 71–73, 114, 116, 147, 148, 164 supplied by the user (sources named in the file: worksaccounts.com, kupdf.net, teachmint)','(supplied file: work/official/user_SR_exact_text.md)','Read in full','Rule text, but from non-official reproductions; added verbatim to the FR/SR section. SR 164 clause (c) appears only in the earlier summary.'],\n"
o = o.replace("['DoE O.M. 21/1/2018-E.II(B), 29.07.2025", row + "['DoE O.M. 21/1/2018-E.II(B), 29.07.2025", 1)
open('official.js', 'w').write(o)

m = open('meta.js').read()
m = m.replace("['FR/SR Part II SR 30/31, 46, 51, 61, 71–73, 107, 110–116, 147, 164 summaries','Secondary summary (supplied compilation)','sec-frsr'],", "['FR/SR Part II SR 30/31, 46, 51, 58, 61, 107 summaries','Secondary summary (supplied compilation)','sec-frsr'],\n['SR 71–73, 114, 116, 147, 148, 164 text','Reproduced text (non-official hosts); not checked against an official host','sec-frsr'],")
m = m.replace("['SR 148, 172, 206 text','No text available','sec-frsr'],", "['SR 172, 206 text','No text available','sec-frsr'],")
m = m.replace("const LOG=[\n", "const LOG=[\n['26 Nov 2026','Added the reproduced rule text of SR 71–73, 114, 116, 147, 148 and 164 you supplied (sources named in the file are non-official reproductions); SR index entries now link to it; E16 confirmed, E18 updated (180 days = a GIO under SR 73).'],\n", 1)
open('meta.js', 'w').write(m)
