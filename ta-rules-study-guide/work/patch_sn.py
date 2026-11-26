import re, shutil

# ---- evidence copies
for f in ['SPECIAL-DISPENSATION-SCHEME.pdf', 'ECE_15694.pdf', 'Frequently-Asked-Questions-on-Procurement-and-Other-Financial-Matters.pdf']:
    shutil.copy('staffnews/' + f, 'official/staffnews_' + f)

# ---- official.js: register rows and not-retrieved list
p = 'official.js'
s = open(p).read()
SN = "https://www.staffnews.in/wp-content/uploads/"
rows = """['DoPT O.M. F.No. 31011/15/2022-Estt.A-IV, 09.09.2026 (LTC air Special Dispensation extended to 25.09.2028)','""" + SN + """2026/09/SPECIAL-DISPENSATION-SCHEME.pdf','Read (9 pages, text layer); copy hosted on staffnews.in (secondary host)','NOT in the guide: scheme extended 26.09.2026–25.09.2028; conditions in S12.'],
['DoPT O.M. 31011/12/2022-Estt.A-IV, 29.08.2022 (LTC air booking) — enclosure to the 09.09.2026 O.M.','""" + SN + """2026/09/SPECIAL-DISPENSATION-SCHEME.pdf','Read (text layer); secondary-hosted copy','Previously unreachable; guide’s 21-day / 30-day / 24-hour points are confirmed (S13).'],
['DoPT O.M. 31011/11/2023-Pers. Policy A-IV, October 2023 (LTC air modifications) — enclosure','""" + SN + """2026/09/SPECIAL-DISPENSATION-SCHEME.pdf','Read (text layer); secondary-hosted copy; day of month not clearly legible (another O.M. cites it as 20.10.2023)','NOT in the guide (S13).'],
['Dept of Posts order P-17/2/2024-PAP-DOP, 22.10.2026 and ECI order 23/WB/ES-II/2025 (SIR-M.O.), 25.02.2026 (TA/DA of Micro Observers)','""" + SN + """2026/11/ECE_15694.pdf','Order text read from the staffnews article; ECI PDF saved (4 pp)','Peripheral — S14.'],
['KVS “FAQs on Procurement and Other Financial Matters”, Section 7 (54 TA/DA/LTC FAQs), as published by staffnews.in','""" + SN + """2026/11/Frequently-Asked-Questions-on-Procurement-and-Other-Financial-Matters.pdf','Skimmed (secondary: a KVS document with visible typos)','Not used as authority. Dependency test (₹9,000 + DR) and base mileage ₹24/₹12 agree with the guide.'],
"""
s = s.replace("['DoE O.M. 21/1/2018-E.II(B), 29.07.2025", rows + "['DoE O.M. 21/1/2018-E.II(B), 29.07.2025", 1)
s = s.replace("'DoPT LTC FAQ 01.07.2025 and DoPT O.M. 29.08.2022 (documents.doptcirculars.nic.in) and the DoPT Joining Time Rules consolidation: the host reset the connection. I did not try to get round it, so those points stay as the source marks them.'",
              "'DoPT LTC FAQ 01.07.2025 and the DoPT Joining Time Rules consolidation (documents.doptcirculars.nic.in): the host reset the connection. I did not try to get round it, so those points stay as the source marks them. (DoPT O.M. 29.08.2022 was later read as an enclosure — see S13.)'")
open(p, 'w').write(s)

# ---- official2.js: supplements, checks, MCQs
p = 'official2.js'
s = open(p).read()
sup = r"""{id:'off-s12',title:'S12 — LTC air Special Dispensation Scheme extended to 25.09.2028 (DoPT O.M. 09.09.2026)',cite:'DoPT O.M. F.No. 31011/15/2022-Estt.A-IV, 09.09.2026, paras 1–3 (staffnews.in copy)',types:['om','proviso','exception'],
 body:`<ul class="hlist"><li><b>Extension:</b> the scheme allowing travel by air to NER, J&amp;K, Ladakh and A&amp;N is extended for two years, 26.09.2026 to 25.09.2028.</li><li><b>Conversion:</b> an eligible Government servant may use one Home Town LTC in a four-year block to visit any place in the four regions; no conversion where Home Town and headquarters are the same; if the Home Town is in one of the regions, conversion is for any one of the other three; fresh recruits may convert one of their three Home Town LTCs and get one additional conversion for J&amp;K/Ladakh.</li><li><b>Air-entitled employees:</b> may travel from headquarters in their entitled class by any airline, subject to the 29.08.2022 and October 2023 DoPT O.M.s.</li><li><b>Employees not entitled to air:</b> economy class by any airline (a) Kolkata/Guwahati ↔ NER; (b) Kolkata/Chennai/Visakhapatnam ↔ Port Blair; (c) Delhi/Amritsar ↔ J&amp;K/Ladakh, with the journey up to the gateway at the entitled mode; para 2(viii) also allows economy air directly from headquarters, but reimbursement then follows the 29.08.2022 conditions.</li><li>Applies whether the concession is used against Anywhere-in-India LTC or in lieu of Home Town LTC. Booking via the three ATAs, best fare, slots, advances and reimbursement rules of the 29.08.2022 O.M. also apply. Ministries are to spot-check air tickets with airlines for misuse.</li></ul>`},
{id:'off-s13',title:'S13 — DoPT LTC air-booking O.M.s of 29.08.2022 and October 2023 (read from the enclosures)',cite:'DoPT O.M. 31011/12/2022-Estt.A-IV, 29.08.2022; O.M. 31011/11/2023-Pers. Policy A-IV, October 2023',types:['om','order','proviso'],
 body:`<ul class="hlist"><li><b>29.08.2022:</b> for LTC air journeys tickets only from the three ATAs (choice left to the office/employee; no agency charges); cheapest fare in the entitled class, preferably non-stop, in the desired 3-hour slot with a 10% optimisation band; keep the ATA webpage print-out; booking at least 21 days ahead is <i>encouraged</i>; cancellation under 24 hours needs a self-declared justification (ATAs to give nil cancellation charges; till then reimbursed where beyond the employee’s control); one ticket per leg; register the official e-mail; unauthorised booking — relaxation by FA / HoD not below Joint Secretary; no mileage points.</li><li><b>Advances:</b> air-entitled employees may apply at least 30 days before the journey with the ATA print-out; non-entitled employees travelling by air outside the Special Dispensation Scheme apply with reference to rail/bus fare, and reimbursement is the lesser of actual air fare or entitled train/bus fare by the shortest route.</li><li><b>October 2023 modifications:</b> the three ATAs display the cheapest flight and flights up to 10% dearer in the desired slot — booking on their websites is itself proof of the cheapest fare; tickets carry the word “LTC”; ATAs register employees without official e-mail on the office’s request; the railhead print-out rule for Special Dispensation travel continues.</li></ul>`},
{id:'off-s14',title:'S14 — TA/DA for election Micro Observers (peripheral)',cite:'Dept of Posts order 22.10.2026 citing ECI order 25.02.2026',types:['order','exception'],
 body:`<p>The ECI clarified that the consolidated remuneration for Electoral Roll Micro Observers in the Special Intensive Revision is for the work done and is <b>not in lieu of TA/DA</b>; such officials may claim TA/DA from their parent Department/Organisation as per their entitlement, and the Department of Posts told its Circle to regulate claims accordingly. (Order text as published on staffnews.in; included only as an example of a recent TA/DA clarification.)</p>`},
"""
s = s.replace("{id:'off-s9'", sup + "{id:'off-s9'", 1)
s = s.replace("'ch10-007':'Official 16.06.2022 O.M. details (slots, 72-hour justification, certificate within 72 hours, FA/HoD relaxation): S8.'",
              "'ch10-007':'Official 16.06.2022 O.M. details (slots, 72-hour justification, certificate within 72 hours, FA/HoD relaxation): S8. The DoPT LTC-air O.M. of 29.08.2022 (read from an enclosure) confirms the 21-day encouragement, 30-day advance request and 24-hour cancellation justification: S13.'")
s = s.replace("'ch10-008':'GFR Rule 292 states 30 / 60 days for LTC claims",
              "'ch10-008':'LTC air Special Dispensation (NER/J&K/Ladakh/A&N): extended 26.09.2026–25.09.2028, and non-entitled employees may fly economy on stated sectors or directly from headquarters with limited reimbursement (S12). GFR Rule 292 states 30 / 60 days for LTC claims")
s = s.replace("const CARDS=[", """const CARDS=[
['LTC air Special Dispensation Scheme — validity now?','Extended by DoPT O.M. 09.09.2026 from 26.09.2026 to 25.09.2028.','DoPT O.M. 09.09.2026 (S12)'],
['LTC air: how many ATAs and what fare rule?','Three ATAs; cheapest fare in the 3-hour slot with a 10% band; Oct 2023: ATAs show cheapest and up to 10% dearer, booking itself is proof.','DoPT O.M.s 29.08.2022, Oct 2023 (S13)'],""", 1)
s = s.replace("const MCQ=[", """const MCQ=[
{q:'Until when has the LTC air Special Dispensation Scheme (NER, J&K, Ladakh, A&N) been extended?',o:['25.09.2026','25.09.2027','25.09.2028','Indefinitely'],a:2,why:'DoPT O.M. 09.09.2026 extends it for two years from 26.09.2026.',c:'S12'},
{q:'Under the DoPT LTC-air O.M. of 29.08.2022, cancelling less than 24 hours before travel requires:',o:['Nothing','A self-declared justification','FA permission','A fee'],a:1,why:'Para (v); ATAs were also asked to give nil cancellation charges.',c:'S13'},
{q:'The October 2023 DoPT O.M. says booking LTC air tickets on the three ATAs’ websites is itself:',o:['A fee-bearing service','Proof that the ticket was of the cheapest fare','Optional','Only valid for Level 14+'],a:1,why:'ATAs display the cheapest fare and fares up to 10% higher.',c:'S13'},
""", 1)
open(p, 'w').write(s)

# ---- meta.js facts / log
p = 'meta.js'
s = open(p).read()
s = s.replace("['Para 3.6.3: TTA for temporary staff under 3 years'",
              "['DoPT LTC-air O.M.s 29.08.2022 and Oct 2023 (21-day, 30-day advance, 24-hour cancellation, 10% band)',OFFC+' (secondary-hosted copy)','S13'],\n['LTC air Special Dispensation extended to 25.09.2028',OFFC+' (secondary-hosted copy)','DoPT O.M. 09.09.2026'],\n['Para 3.6.3: TTA for temporary staff under 3 years'")
s = s.replace("const LOG=[\n", "const LOG=[\n['26 Nov 2026','Staff News check: read the new DoPT O.M. of 09.09.2026 (LTC air Special Dispensation to 25.09.2028) with its enclosures (29.08.2022, Oct 2023); added S12–S14. Staff News is a secondary host — its own articles are not used as authority.'],\n")
s = s.replace("'DoPT LTC FAQ (01.07.2025), DoPT O.M. 29.08.2022, Joining Time Rules consolidation, G.S.R. 229(E) — hosts unreachable; need files from you.'",
              "'DoPT LTC FAQ (01.07.2025), Joining Time Rules consolidation, G.S.R. 229(E) — hosts unreachable; need files from you. (DoPT O.M. 29.08.2022 is now covered via an enclosure.)'")
open(p, 'w').write(s)
