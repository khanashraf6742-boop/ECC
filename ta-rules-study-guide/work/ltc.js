// TA vs LTC — comparison of COMMON areas only (the guide does not cover LTC as a topic).
// Official = read in the official PDF (DoPT O.M.s via a staffnews.in-hosted copy; GFR; DoE O.M.s). Source only = the study-guide source's own statement.
const OFF = 'Official', SRC = 'Source only', CONF = 'Conflict', HOLD = 'Not retrieved';
const ROWS = [
['Who issues the orders','Department of Expenditure (O.M. 19030/1/2017-E.IV and amendments)','DoPT (CCS (LTC) Rules, 1988 and DoPT O.M.s). DoE O.M. 13.03.2018 para 6 says its claim-time orders do not apply to LTC',OFF],
['Air-ticket channel','Only the three ATAs: BLCL, Ashok Travels & Tours, IRCTC (DoE O.M.s 31.12.2021, 16.06.2022)','Same three ATAs (DoPT O.M. 29.08.2022, issued after DoE’s 16.06.2022 O.M., “which is also applicable” to LTC air journeys)',OFF],
['Fare rule','Cheapest fare in the entitled class, preferably non-stop, in the desired 3-hour slot; 10% price band','Same slots and band; October 2023: the ATAs show the cheapest and up-to-10%-dearer fares, and booking on their sites is itself proof of the cheapest fare',OFF],
['Lead time','21 days ahead encouraged; booking under 72 hours before tour travel needs a self-declared justification','21 days ahead encouraged; no 72-hour item appears in the LTC O.M.',OFF],
['Cancellation','Under 24 hours before travel: self-declared justification','Under 24 hours: justification; ATAs to give nil cancellation charges and until then charges are reimbursed where beyond the employee’s control',OFF],
['Tickets per leg','One; at most two alternates with justification','One ticket per leg; more than one not allowed',OFF],
['Unauthorised booking','Relaxation by the FA or a Head of Department not below Joint Secretary','Same authorities',OFF],
['Mileage points','None generated on Government-account travel (O.M. 16.06.2022 para 14)','None generated (DoPT O.M. 29.08.2022 para ix)',OFF],
['Private airlines','Allowed, tickets only via the three ATAs (DoE O.M. 16.02.2022)','The same DoE clarification expressly covers LTC (“domestic (including LTC)”)',OFF],
['Proof after the journey','Annexure-1 self-declaration within 72 hours; boarding pass, or the self-declaration allowed by O.M. 23.06.2020','Keep the ATA web-page print-out for settlement; no Annexure-1 in the DoPT O.M.',OFF],
['Advance','Tour advance rules not established in the sources (2005 Compendium currency unverified)','Air-entitled employees apply at least 30 days before the journey with the ATA print-out; non-entitled employees who fly outside the Special Dispensation apply on rail/bus fare',OFF+' (LTC) / '+HOLD+' (TA)'],
['Claim period','60 days from the day the claim becomes due (GFR 290; O.M. 13.03.2018); retirement 180 days (O.M. 15.06.2021)','GFR 292: 30 days if an advance was drawn, 60 days if not (due the day after the return journey). The study-guide source says 1 month / 3 months under CCS (LTC) Rules 14/15',CONF+' for the no-advance case; DoPT text not retrieved'],
['Daily Allowance','Hotel, local travel and food by Pay Level (O.M. para 2E)','None of any kind',SRC],
['Air for Levels 6–8','Economy air (Table A, Levels 6 to 11)','Normal LTC entitlement is not air (CCS (LTC) Rule 12 as stated in the source); Special Dispensation to NER, J&K, Ladakh and A&N allows air until 25.09.2028 (DoPT O.M. 09.09.2026)',OFF+' (dispensation) / '+SRC+' (Rule 12)'],
['Road vehicle','Mileage for own car/taxi (para 2D)','Government or PSU-operated vehicles only, with stated exceptions',SRC],
['Tour packages','Not applicable','Private operators’ tour packages not allowed',SRC],
['Dependent family','Family as in SR 2(8); dependency ₹9,000 + DR','Same dependency income test is used',SRC],
['Misuse check','—','Ministries to randomly verify submitted air tickets with the airlines (DoPT O.M.s 09.09.2026 and October 2023)',OFF]];
const SVG = {id:'svg-ta-ltc',title:'TA or LTC? — which order set applies',cite:'DoE O.M. 13.07.2017; DoE O.M. 13.03.2018 para 6; DoPT O.M. 29.08.2022',steps:[
['1  What is the journey for?','Official duty, transfer, retirement or training → CCS TA rules (DoE). Leave travel concession → CCS (LTC) Rules and DoPT orders.'],
['2  Is it an air ticket on Government account?','Yes, for either → buy only through the three ATAs; same slots, 10% band, 21-day encouragement, 24-hour cancellation rule, relaxation by FA / HoD ≥ Joint Secretary.'],
['3  Daily Allowance and vehicles','TA: DA by Pay Level and mileage. LTC: no DA; Government/PSU vehicles with exceptions (source).'],
['4  Claim clock','TA: 60 days (retirement 180). LTC: GFR 292 gives 30 / 60 days; the guide’s source says 1 / 3 months — unresolved. DoE’s 13.03.2018 clock does not apply to LTC.']]};
const MCQ = [
{q:'Which department’s O.M. 13.03.2018 clock (60 days) does NOT apply to LTC claims?',o:['DoPT','Department of Expenditure — its para 6 excludes LTC','CAG','UPSC'],a:1,w:'O.M. 13.03.2018 para 6: not applicable to LTC claims, which are governed by DoPT’s separate rules.',c:'O.M. 13.03.2018 para 6'},
{q:'How many authorised travel agents apply to air tickets for both tour and LTC?',o:['One','Two','Three','Any registered agent'],a:2,w:'BLCL, Ashok Travels & Tours and IRCTC (DoE 16.06.2022; DoPT 29.08.2022).',c:'TA vs LTC table'},
{q:'Mileage points on Government-account air travel are:',o:['Kept by the employee','Not generated','Used for upgrades','Shared with the agent'],a:1,w:'DoE 16.06.2022 para 14; DoPT 29.08.2022 para ix.',c:'TA vs LTC table'},
{q:'Daily Allowance on LTC (as stated in the study-guide source) is:',o:['Same as tour','Half','None of any kind','Only for Level 14+'],a:2,w:'Source Chapter 10 contrast.',c:'ch10-008'},
{q:'GFR Rule 292 sets LTC claim submission, where no advance was drawn, at:',o:['30 days from the due date','60 days from the due date','3 months from the return journey','One year'],a:1,w:'GFR text; the source’s “3 months” differs — flagged as a conflict.',c:'GFR 292'},
{q:'Until when has the LTC air Special Dispensation (NER, J&K, Ladakh, A&N) been extended?',o:['25.09.2026','25.09.2027','25.09.2028','31.03.2030'],a:2,w:'DoPT O.M. 09.09.2026.',c:'DoPT O.M. 09.09.2026'},
{q:'Booking an air ticket on an ATA’s website for LTC is, per the October 2023 DoPT O.M.:',o:['Optional','Itself proof that the ticket was the cheapest fare','Barred','Only for Level 14+'],a:1,w:'ATAs display the cheapest fare and fares up to 10% more.',c:'DoPT O.M. October 2023'},
{q:'Air for Pay Levels 6–8: tour vs LTC (normal rule)?',o:['Both allowed','Tour allowed; LTC not (dispensation aside)','LTC allowed; tour not','Neither'],a:1,w:'Table A for tour; CCS (LTC) Rule 12 as stated in the source for LTC.',c:'ch10-008'}];
const CARDS = [
['Common air regime of TA and LTC?','Three ATAs, cheapest fare in a 3-hour slot (10% band), 21-day encouragement, 24-hour cancellation justification, FA / HoD ≥ Joint Secretary relaxation, no mileage points.','DoE 16.06.2022; DoPT 29.08.2022'],
['What differs after the journey?','TA: Annexure-1 within 72 hours, boarding pass. LTC: keep the ATA web-page print-out.','DoE 16.06.2022; DoPT 29.08.2022'],
['LTC claim period — official text?','GFR 292: 30 days (advance drawn) / 60 days (not drawn); the guide’s source says 1 / 3 months — unresolved.','GFR 292'],
['Does O.M. 13.03.2018 cover LTC?','No — para 6 leaves LTC to DoPT’s rules.','O.M. 13.03.2018'],
['LTC air Special Dispensation?','NER, J&K, Ladakh, A&N; extended to 25.09.2028.','DoPT O.M. 09.09.2026']];
module.exports = {ROWS, SVG, MCQ, CARDS};
