import shutil
shutil.copy('frsr/mcr_ta.pdf', 'official/mcrhrdi_TA_rules_training_deck_Nov2025.pdf')

# ---- frsr.js: deck rows + notes
p = 'frsr.js'
s = open(p).read()
deck = r'''
const DECK = [
 ['Temporary transfer','A temporary transfer for a short period not exceeding 180 days: TA/DA as on tour; only actual transit time (no joining time); no advance of pay. If the temporary transfer runs beyond 180 days: issue a transfer order; DA is admitted till the date of issue of the transfer order and TA drawn is adjusted in the TA claim.','Corroborates the “180 days” notion in the guide’s source (Chapter 5) — but the reproduced SR 114 text contains no 180-day rule.'],
 ['SR 146, SR 114, SR 191','Slides cite SR 114 for transfer, SR 146 for journeys on retirement and SR 191 for the Controlling Officer’s signature on TA bills.','Consistent with the reproduced SR 114 / SR 147 text.'],
 ['Claim and advance','TA bill within sixty days of completing the journey on tour/training/transfer, else deemed relinquished; delay in settling an advance attracts penal interest; no second advance normally for a tour before the earlier advance is settled.','Matches the 60-day clock; the advance points are secondary and not in the DoE O.M.s read.'],
 ['Rules listed as applicable','FR 44; SR 17–91, 104–109, 112, 117, 120, 123–128, 130, 132–135, 140, 142–150, 151A, 153–158, 160–162, 164–165 and Government of India decisions quoted in FR/SR Part II.','Gives the range of TA SRs; SR 164–165 are named, with no text.'],
 ['Local journey food DA','Hotel not applicable; food DA 15% / 35% / 50% of the tour lump sum by absence band.','Matches the guide (signed DoE letter 12.09.2018).']]
'''
s = s.replace("const TEXTMAP", deck + "const TEXTMAP", 1)
s = s.replace("module.exports = {TEXTMAP,", "module.exports = {DECK, TEXTMAP,")
open(p, 'w').write(s)

# ---- build.js: render deck table in the FR/SR section
p = 'build.js'
s = open(p).read()
blk = r'''<div class="study-aid unc" data-chrome="1"><span class="aid-label">Corroboration from a Government-hosted training deck — secondary</span><p class="secmeta">MCRHRDI, “Sessions on Travelling Allowances Rules”, 25 Nov 2025 (a training presentation by a former ISTM faculty member, hosted on mcrhrdi.gov.in). It is training material, not rule text; it names SR 164–165 but quotes neither.</p><div class="tablewrap" tabindex="0" role="region" aria-label="Training deck"><table><thead><tr><th scope="col">Topic</th><th scope="col">What the deck says</th><th scope="col">Relation to the guide</th></tr></thead><tbody>${FRSR.DECK.map(d=>`<tr><th scope="row">${esc(d[0])}</th><td>${esc(d[1])}</td><td>${esc(d[2])}</td></tr>`).join('')}</tbody></table></div></div>
'''
s = s.replace("<div class=\"study-aid\" data-chrome=\"1\"><span class=\"aid-label\">Where the compilation and the official orders disagree</span>", blk + "<div class=\"study-aid\" data-chrome=\"1\"><span class=\"aid-label\">Where the compilation and the official orders disagree</span>", 1)
open(p, 'w').write(s)

# ---- official2.js checks
p = 'official2.js'
s = open(p).read()
s = s.replace("const checks={", "const checks={\n'ch05-005':'SR 114 (reproduced text) contains no 180-day rule; the 13.07.2017 O.M. only says SR 114’s general conditions continue. A Government-hosted training deck (MCRHRDI, Nov 2025) states a temporary transfer up to 180 days is TA/DA as on tour — secondary only; see the FR/SR section.',\n'ch11-004':'Secondary only: the MCRHRDI training deck (Nov 2025) says delay in settling an advance attracts penal interest and no second advance is normally given before the first is settled; the advance periods are still not established from a primary text.',", 1)
open(p, 'w').write(s)

# ---- official.js register row; meta.js
o = open('official.js').read()
row = "['MCRHRDI training deck “Sessions on Travelling Allowances Rules”, 25 Nov 2025 (mcrhrdi.gov.in) — secondary','https://mcrhrdi.gov.in/2025/splfc2025/weeks/week6/','Read (37 slides, text layer)','Training material, not rule text; corroborates 60 days, local-journey 15/35/50 and the 180-day temporary-transfer notion (FR/SR section).'],\n"
o = o.replace("['DoE O.M. 21/1/2018-E.II(B), 29.07.2025", row + "['DoE O.M. 21/1/2018-E.II(B), 29.07.2025", 1)
o = o.replace("'FR/SR Part II compilation supplied", "'FR/SR Part II compilation supplied", 1)
open('official.js', 'w').write(o)

m = open('meta.js').read()
m = m.replace("const LOG=[\n", "const LOG=[\n['26 Nov 2026','Searched for primary FR/SR Part II text: none is published on the DoE/DoPT hosts reachable here (DoPT carries Part I scans only; ISTM carries notes). Recorded a Government-hosted training deck (MCRHRDI, Nov 2025) as secondary corroboration; SR 30/31, 46, 51, 58, 61, 107 remain summaries, SR 172/206 gaps, SR 164(c) uncertain.'],\n", 1)
m = m.replace("['SR 172, 206 text','No text available','sec-frsr'],", "['SR 172, 206 text','No text available','sec-frsr'],\n['Temporary transfer up to 180 days = tour TA/DA (MCRHRDI Nov 2025)','Secondary (Government-hosted training deck)','sec-frsr'],")
open('meta.js', 'w').write(m)
