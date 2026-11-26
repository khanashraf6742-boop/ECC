module.exports={
quick:{
'ch05-004':'CTG = 80% of last month’s basic pay for eligible transfer ≥20 km; <20 km/same city: one-third of normal CTG only if actual change of residence, else nil; A&N/Lakshadweep: 100%; both spouses (second after 60 days, within 6 months): full to earlier, 50% to later. CTG on retirement: O.M. 06.01.2022.',
'ch05-005':'STATUS OPEN: no verified “180-day” tour/transfer switch. Classify using the actual order and SR 114 conditions (O.M. 13.07.2017 preserves SR 114); fare, CTG, personal effects and conveyance each keep their own conditions. Training (SR 164) is separate.',
'ch05-006':'Same Urban Agglomeration: no residence change → no TA (CTG nil); with residence change → one-third CTG (1/3 × 80% = 26.67% of last basic) + actual local transport of personal effects. “Station” = Census-defined UA (Delhi UA example).',
'ch05-007':'SR 116 GIOs: road mileage scaled by family — one (self or self + 1), two (exactly 2 family members), three (more than 2); taxes (service tax, GST, cess) on personal-effects transport reimbursable up to entitlement; conveyance possession need not be in public interest; Posts: choice posting after full tenure ≠ transfer on own request.',
'ch05-008':'Personal effects by road: ₹62.50/km (L6+), ₹31.25/km (L5), ₹18.75/km (L4 & below); by train: 6,000 kg (L6+; double container L12+, single L6–11), 3,000 kg (L5), 1,500 kg (≤L4). Conveyance: L6+ 1 car or 1 motor cycle/scooter; L5 & below 1 motorcycle/scooter/moped/bicycle.',
'ch05-009':'On transfer, TA entitlement is based on the pay of the lower of the two posts/grades. Special provisions for NE Region, A&N, Lakshadweep, Ladakh: O.M. 16.06.2022.',
'ch05-010':'Fact-sheet: CTG 80% / 1⅓ / 100% rules, 100/50 spouse split, retirement CTG O.M. 06.01.2022, effects road rates ₹62.50/31.25/18.75, same-UA CTG nil or 1/3.'},
hooks:{'ch05-004':'“Below 20 km: residence change matters; the islands have a separate 100% rate.” (source fix-phrase)','ch05-009':'“Paid like the junior of your two posts — never the senior.” (source hook)'},
mcqs:[
{q:'CTG for an eligible transfer between stations 20 km or more apart (general case)?',o:['50% of basic','80% of last month’s basic pay','100% of last month’s basic pay','Nil'],a:1,why:'“payable at 80% of the last month's basic pay”.',c:'ch05-004 (L1270–1284)'},
{q:'Transfer of 15 km with NO actual change of residence — CTG?',o:['80%','One-third of normal CTG','Nil','100%'],a:2,why:'Below 20 km/same city: one-third only if an actual change of residence is involved; otherwise nil.',c:'ch05-004'},
{q:'CTG on transfer to/from Andaman & Nicobar or Lakshadweep?',o:['80%','100% of last month’s basic pay','One-third','Nil'],a:1,why:'“enhanced rate of 100% of last month's basic pay”.',c:'ch05-004'},
{q:'Is a duration-only “180 days” rule verified to classify Tour vs Transfer?',o:['Yes — under 180 days tour, over 180 transfer','No — apply the order and current SR 114 conditions; duration alone is not verified','Yes, but only for training','Yes, under O.M. 16.06.2022'],a:1,why:'Primary-source boundary: a duration-only “180-day switch” is not established.',c:'ch05-005 (L1285–1304)'},
{q:'Personal-effects road rate for Level 5 (current 25%-enhanced)?',o:['₹62.50/km','₹31.25/km','₹18.75/km','₹30/km'],a:1,why:'₹62.50 (L6+), ₹31.25 (L5), ₹18.75 (L4 & below).',c:'ch05-008 (L1350–1363)'}],
cards:[
{f:'CTG general rate?',b:'80% of last month’s basic pay (eligible transfer, stations ≥20 km apart).',c:'ch05-004'},
{f:'CTG below 20 km / same city?',b:'One-third of normal CTG only if actual change of residence; otherwise nil.',c:'ch05-004'},
{f:'Spouse transfer CTG split?',b:'Both Central Govt servants, same station to same station within 6 months, second after 60 days: full CTG to earlier-transferred spouse; 50% to the later.',c:'ch05-004'},
{f:'Which pay governs TA on transfer?',b:'Pay of the lower of the two posts/grades (old vs new).',c:'ch05-009'},
{f:'Road mileages on transfer by road (SR 116 GIO 5)?',b:'One (self / self+1); two (exactly two family members); three (more than two).',c:'ch05-007'},
{f:'Effects by train — weight entitlements?',b:'6,000 kg (L6+); 3,000 kg (L5); 1,500 kg (L4 & below).',c:'ch05-008'}]};
