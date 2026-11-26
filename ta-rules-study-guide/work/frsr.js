// FR/SR Part II — SECONDARY summaries, from the compilation supplied by the user (“FR_SR_Part_II_TA_Rules_with_Sources.html”).
// Nothing here is primary rule text. Where it conflicts with the official O.M.s or the guide's source, the conflict is stated.
const SEC = 'Secondary summary', GAP = 'Gap — no text', CONFL = 'Conflicting summaries', UNRES = 'Unresolved';
// [rowId, SRs it covers (for the xref index), title, summary, status, drawn from (names only)]
const ROWS = [
['frsr-30-31', ['sr-30','sr-31'], 'SR 30 / 31 — route for mileage allowance',
 'SR 30: a journey is held to be by the shortest of two or more practicable routes, or the cheapest where equally short; where alternative railway routes differ little in time and cost, mileage is calculated on the route actually used. SR 31: a competent authority may, for recorded special reasons, allow mileage on a route other than the shortest or cheapest, if the journey is actually performed by it.',
 SEC, 'Works Accounts FR-SR PDF; Teachmint SR 1–195'],
['frsr-46', ['sr-46'], 'SR 46 — TA on tour (road mileage)',
 'Listed as “TA on Tour”. For road journeys, mileage allowance at prescribed rates per kilometre, distinguishing ordinary public conveyance, autorickshaw and own car/scooter/motorcycle, and places where no specific rates are prescribed. Rates and conditions not verified.',
 SEC, 'Finance Administration index; Teachmint'],
['frsr-51', ['sr-51'], 'SR 51 — taxes/GST, travelling charges, DA on boarding/lodging',
 'Indexed as covering reimbursement of taxes/GST, reimbursement of travelling charges and admissibility of DA where boarding and lodging are provided; DA to an official on tour who returns to headquarters daily (except Sundays/holidays) is admissible as per the conditions for actual stay on tour or temporary transfer.',
 SEC, 'Finance Administration index; Teachmint'],
['frsr-58', ['sr-58'], 'SR 58',
 'Summaries conflict: one compilation records “S.R. 58: Deleted”; another reproduces an older text about Civil Police below Sub-Inspector rank in fatigue parties. The study-guide source cites SR 58 and SR 107 for steamer entitlements — not confirmed here.',
 CONFL, 'Works Accounts FR-SR PDF; Indian Kanoon'],
['frsr-61', ['sr-61'], 'SR 61 — when a Government servant is on tour',
 'On tour when absent on duty from headquarters, within or (with proper sanction) beyond the sphere of duty. The secondary text is truncated after the hill-station reference.',
 SEC, 'Works Accounts FR-SR PDF'],
['frsr-71', ['sr-71-sec'], 'SR 71(2), clarifications and SR 72–73 extracts (not in the reproduced text)',
 'SR 71(2): TA for a local journey is admissible if the temporary place of duty is beyond 8 km from the normal place of duty, whether the journey starts from residence or office. After the 7th CPC, DA on tour has three components (hotel, travel within the city, food) and for a local journey beyond 8 km the prescribed components may be admissible. Practice: journeys beyond 8 km inside the urban agglomeration/municipality of headquarters are normally by bus, local train or own conveyance, as for the journey to the duty point. G.I.O.(4): DA on local journeys up to 180 days (one secondary training document). SR 72–73 extracts: a railway journey combined with steamer/road travel to a place at least eight kilometres from the railhead earns mileage for that leg with the time deducted from absence; evidence in a court within eight kilometres of headquarters earns no TA, and the court’s actual-expense payment may be accepted if no permanent TA is drawn.',
 SEC+' · '+UNRES+' for the at-or-below-8-km case', 'Staff News 2018; MCR HRDI; Lawyers Club India; Works Accounts FR-SR PDF'],
['frsr-107', ['sr-107'], 'SR 107 — TA on re-appointment',
 'When a pensioner, or a servant thrown out of employment by reduction of establishment or abolition of the post, is re-appointed, the sanctioning authority may (outside Rule 105-A cases) allow TA for so much of the journey to join the new post as falls within India. The study-guide source cites SR 107 for steamer entitlements — a conflict not resolved here.',
 SEC, 'Works Accounts FR-SR PDF; Teachmint'],
['frsr-110-116', ['sr-110','sr-111','sr-112','sr-113','sr-114','sr-115','sr-116'], 'SR 110–116 — general TA conditions',
 'The reproduced text of SR 114 and SR 116 is given below; a secondary summary of “SR-116” also lists: travel in the public interest; shortest and cheapest route; tickets/receipts mandatory; TA advance allowed; unspent balance returned. SRs 110–115 were not separately verified. The official 13.07.2017 O.M. itself cites SR 114 (general conditions on transfer TA) and SR 116 (conveyance on transfer).',
 SEC, 'CSD Rates'],
['frsr-172', ['sr-172'], 'SR 172', 'No primary text and no reliable secondary summary was available.', GAP, '—'],
['frsr-206', ['sr-206'], 'SR 206', 'No primary text and no reliable secondary summary was available. The guide’s source cites SR 206 for foreign-service TA.', GAP, '—']];
const NOTES = [
 'Status: every row is a SECONDARY summary from the compilation you supplied; the compilation itself says it must be verified against primary FR/SR Part II text. It is not exam-quotable as verbatim rule text.',
 'Still unresolved in the compilation: training TA (SR 164), the at-or-below-8-km case (SR 71), the 2005 Advances Compendium, Rule 4(4) as substituted in 2015, foreign-travel DA (MEA), Defence and Railways TA, the family and city-class lists, permanent/fixed TA categories, and any DoE TA order after 12.09.2022.'];
const DISCREP = [
 ['SR 147 and SR 116 roles (secondary summary)','The compilation (CSD Rates summary) calls SR 147 transfer TA and SR 116 general TA. The official O.M. of 13.07.2017 cites SR 114 for transfer, SR 116 for conveyance on transfer, and SR 147 for retirement.','The reproduced SR text confirms SR 114 = transfer (public convenience), SR 116 = transfer entitlements, SR 147 = discretion for journeys of the kind in Rule 146 (retirement). The “SR 147 = Transfer TA” label is wrong.'],
 ['SR 58 / SR 107 steamer entitlement','The study-guide source cites SR 58 and SR 107 for steamer travel. The compilation records SR 58 as “Deleted” (or an unrelated police text) and SR 107 as TA on re-appointment. The official O.M. para 2C gives steamer classes without citing an SR.','Unresolved — do not quote an SR number for steamer entitlements.'],
 ['The “180 days” figure','The compilation records a “G.I.O.(4)” 180-day limit on DA for local journeys in one secondary training document. The 13.07.2017 O.M. contains no 180-day DA limit (E2).','The reproduced text states that SR 73 is not printed and that Government orders give full DA for the first 180 days of a continuous halt and nil thereafter — so the figure comes from a GIO under SR 73, not the O.M. The GIO text itself was not seen.'],
 ['SR 164 clause (c)','The earlier secondary summary lists clause (c) — journeys during the course of training; the reproduced text lists only (a) and (b) plus the proviso.','[uncertain] — check the official text; the guide’s source treats training TA as unresolved anyway.']
];
const MCQ = [
{q:'SR 114 (reproduced text): a transfer at the Government servant’s own request is treated as a transfer for the public convenience:',o:['Always','Unless the authority, for recorded special reasons, otherwise directs it to be treated so — i.e. normally not','Only for Level 9+','Only within 20 km'],a:1,w:'SR 114: own-request transfer is not a transfer for public convenience unless the sanctioning authority, for special reasons recorded, otherwise directs.',c:'SR 114 (reproduced text)'},
{q:'SR 116(b)(iii) (reproduced text): a family member who follows within ___ of the transfer, or precedes by not more than one month, is treated as accompanying.',o:['One month','Three months','Six months','One year'],a:2,w:'Time limits extendable by the competent authority in special circumstances.',c:'SR 116(b)(iii)'},
{q:'SR 148 (reproduced text) provides that:',o:['The family gets TA at a fixed scale','A competent authority may grant the family of a servant who dies in service such TA as it deems fit','Only a 75% advance is allowed','No TA is ever admissible'],a:1,w:'One-sentence rule; the GIOs below it carry the detail.',c:'SR 148'},

{q:'SR 30 (secondary summary): for mileage allowance a journey is held to be by:',o:['The route actually used in every case','The shortest of two or more practicable routes, or the cheapest of equally short routes','The cheapest route only','The fastest route'],a:1,w:'With the railway-route proviso.',c:'FR/SR summary (secondary)'},
{q:'SR 71 (secondary summary): the “radius of eight kilometres” is measured:',o:['In a straight line','By the shortest practicable route by ordinary modes of travel','From the residence only','By railway distance only'],a:1,w:'SR 71 Note as summarised.',c:'FR/SR summary (secondary)'},
{q:'SR 164 (secondary summary): the training TA scale may not exceed that of:',o:['Level 14 officers','Government servants of similar status on duty at the place of training','Probationers','Retiring employees'],a:1,w:'Proviso to SR 164.',c:'FR/SR summary (secondary)'},
{q:'Per the official 13.07.2017 O.M., SR 147 is cited for the general conditions of TA on:',o:['Transfer','Retirement','Tour','Training'],a:1,w:'Para 4; para 3 cites SR 114 for transfer.',c:'O.M. 13.07.2017; E16'}];
const CARDS = [
['SR 114 in one line?','No TA on transfer unless it is for the public convenience and pay is drawn during the journey; own-request transfer does not qualify unless recorded special reasons direct otherwise.','SR 114'],
['SR 147 in one line?','A competent authority may, for recorded special reasons, allow TA for a journey of the kind in Rule 146 (retirement-type journeys).','SR 147'],

['SR 31 in one line?','A competent authority may, for recorded special reasons, allow mileage on a route other than the shortest/cheapest if actually used.','FR/SR summary (secondary)'],
['SR 71 local-journey test?','TA for a local journey if the temporary duty place is beyond 8 km from the normal place of duty; “radius” = 8 km by the shortest practicable route.','FR/SR summary (secondary)'],
['Which SRs does the official O.M. 13.07.2017 cite?','SR 114 (transfer conditions), SR 116 (conveyance on transfer), SR 147 (retirement).','O.M. 13.07.2017 paras 3–4']];
const TEXTMAP = {'sr-71':'frsrt-71','sr-72':'frsrt-72','sr-73':'frsrt-73','sr-114':'frsrt-114','sr-116':'frsrt-116','sr-147':'frsrt-147','sr-148':'frsrt-148','sr-164':'frsrt-164'};
module.exports = {TEXTMAP, ROWS, NOTES, DISCREP, MCQ, CARDS, SEC, GAP, CONFL, UNRES};
