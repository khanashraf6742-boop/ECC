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
['frsr-71', ['sr-71','sr-72','sr-73'], 'SR 71–73 — local journeys and the 8 km rule',
 'SR 71: DA may not be drawn for a day on which the Government servant does not reach a point outside a radius of eight kilometres from the duty point (and return from a similar point); “radius of eight kilometres” means eight kilometres by the shortest practicable route. SR 71(2): TA for a local journey is admissible if the temporary place of duty is beyond 8 km from the normal place of duty, whether the journey starts from residence or office. After the 7th CPC, DA on tour has three components (hotel, travel within the city, food) and for a local journey beyond 8 km the prescribed components may be admissible. Practice: journeys beyond 8 km inside the urban agglomeration/municipality of headquarters are normally by bus, local train or own conveyance, as for the journey to the duty point. G.I.O.(4): DA on local journeys up to 180 days (one secondary training document). SR 72–73 extracts: a railway journey combined with steamer/road travel to a place at least eight kilometres from the railhead earns mileage for that leg with the time deducted from absence; evidence in a court within eight kilometres of headquarters earns no TA, and the court’s actual-expense payment may be accepted if no permanent TA is drawn.',
 SEC+' · '+UNRES+' for the at-or-below-8-km case', 'Works Accounts FR-SR PDF; Staff News 2018; MCR HRDI; Lawyers Club India'],
['frsr-107', ['sr-107'], 'SR 107 — TA on re-appointment',
 'When a pensioner, or a servant thrown out of employment by reduction of establishment or abolition of the post, is re-appointed, the sanctioning authority may (outside Rule 105-A cases) allow TA for so much of the journey to join the new post as falls within India. The study-guide source cites SR 107 for steamer entitlements — a conflict not resolved here.',
 SEC, 'Works Accounts FR-SR PDF; Teachmint'],
['frsr-110-116', ['sr-110','sr-111','sr-112','sr-113','sr-114','sr-115','sr-116'], 'SR 110–116 — general TA conditions',
 'A secondary summary of “SR-116” lists: travel in the public interest; shortest and cheapest route; tickets/receipts mandatory; TA advance allowed; unspent balance returned. SRs 110–115 were not separately verified. The official 13.07.2017 O.M. itself cites SR 114 (general conditions on transfer TA) and SR 116 (conveyance on transfer).',
 SEC, 'CSD Rates'],
['frsr-147', ['sr-147'], 'SR 147 — as described in the compilation',
 'The compilation (from a secondary summary) calls SR 147 “Transfer TA” (public interest, family fare, goods up to entitled weight, family may travel separately within 6 months, retirement journeys). The official 13.07.2017 O.M. (para 4) cites SR 147 for the general conditions of TA on RETIREMENT and SR 114 for transfer — use the official role.',
 SEC+' · differs from the official O.M.', 'CSD Rates'],
['frsr-148', ['sr-148'], 'SR 148', 'No primary text and no reliable secondary summary was available. The guide’s source describes SR 148 as the family TA on death-in-service; the 21.12.2016 O.M. (read) extends the one-year limit with FA approval.', GAP, '—'],
['frsr-164', ['sr-164'], 'SR 164 / 164-A — TA on training',
 'SR 164: for a Government servant or student not already in service selected for a course of training, the competent authority may fix the scale of (a) TA for the original journey to and the last journey from the place of training, and halts there; (b) for similar journeys on holidays and vacations in a school/college/institution; (c) for journeys during the course — provided the scale does not exceed that of Government servants of similar status on duty at the place of training. SR 164-A: a military officer in civil employ attending a military course draws mileage and DA at military rates. The training-TA position is held as unresolved.',
 SEC+' · '+UNRES, 'Works Accounts FR-SR PDF'],
['frsr-172', ['sr-172'], 'SR 172', 'No primary text and no reliable secondary summary was available.', GAP, '—'],
['frsr-206', ['sr-206'], 'SR 206', 'No primary text and no reliable secondary summary was available. The guide’s source cites SR 206 for foreign-service TA.', GAP, '—']];
const NOTES = [
 'Status: every row is a SECONDARY summary from the compilation you supplied; the compilation itself says it must be verified against primary FR/SR Part II text. It is not exam-quotable as verbatim rule text.',
 'Still unresolved in the compilation: training TA (SR 164), the at-or-below-8-km case (SR 71), the 2005 Advances Compendium, Rule 4(4) as substituted in 2015, foreign-travel DA (MEA), Defence and Railways TA, the family and city-class lists, permanent/fixed TA categories, and any DoE TA order after 12.09.2022.'];
const DISCREP = [
 ['SR 147 and SR 116 roles','The compilation (CSD Rates summary) calls SR 147 transfer TA and SR 116 general TA. The official O.M. of 13.07.2017 cites SR 114 for transfer, SR 116 for conveyance on transfer, and SR 147 for retirement.','Official O.M. prevails; the compilation’s labels are not relied on.'],
 ['SR 58 / SR 107 steamer entitlement','The study-guide source cites SR 58 and SR 107 for steamer travel. The compilation records SR 58 as “Deleted” (or an unrelated police text) and SR 107 as TA on re-appointment. The official O.M. para 2C gives steamer classes without citing an SR.','Unresolved — do not quote an SR number for steamer entitlements.'],
 ['The “180 days” figure','The compilation records a “G.I.O.(4)” 180-day limit on DA for local journeys in one secondary training document. The 13.07.2017 O.M. contains no 180-day DA limit (E2).','The figure, if it exists, comes from FR/SR commentary, not the O.M.; keep it unverified.']];
const MCQ = [
{q:'SR 30 (secondary summary): for mileage allowance a journey is held to be by:',o:['The route actually used in every case','The shortest of two or more practicable routes, or the cheapest of equally short routes','The cheapest route only','The fastest route'],a:1,w:'With the railway-route proviso.',c:'FR/SR summary (secondary)'},
{q:'SR 71 (secondary summary): the “radius of eight kilometres” is measured:',o:['In a straight line','By the shortest practicable route by ordinary modes of travel','From the residence only','By railway distance only'],a:1,w:'SR 71 Note as summarised.',c:'FR/SR summary (secondary)'},
{q:'SR 164 (secondary summary): the training TA scale may not exceed that of:',o:['Level 14 officers','Government servants of similar status on duty at the place of training','Probationers','Retiring employees'],a:1,w:'Proviso to SR 164.',c:'FR/SR summary (secondary)'},
{q:'Per the official 13.07.2017 O.M., SR 147 is cited for the general conditions of TA on:',o:['Transfer','Retirement','Tour','Training'],a:1,w:'Para 4; para 3 cites SR 114 for transfer.',c:'O.M. 13.07.2017; E16'}];
const CARDS = [
['SR 31 in one line?','A competent authority may, for recorded special reasons, allow mileage on a route other than the shortest/cheapest if actually used.','FR/SR summary (secondary)'],
['SR 71 local-journey test?','TA for a local journey if the temporary duty place is beyond 8 km from the normal place of duty; “radius” = 8 km by the shortest practicable route.','FR/SR summary (secondary)'],
['Which SRs does the official O.M. 13.07.2017 cite?','SR 114 (transfer conditions), SR 116 (conveyance on transfer), SR 147 (retirement).','O.M. 13.07.2017 paras 3–4']];
module.exports = {ROWS, NOTES, DISCREP, MCQ, CARDS, SEC, GAP, CONFL, UNRES};
