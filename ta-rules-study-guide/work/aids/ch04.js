module.exports={
quick:{
'ch04-004':'Where neither the State nor a neighbouring State Directorate of Transport has prescribed a rate: own car/taxi ₹30/km; auto-rickshaw/own scooter ₹15/km; on foot ₹15/km (25%-enhanced rates). A state-specific RMA rate (e.g. PCDA state-wise, for defence) governs instead.',
'ch04-005':'Dead-km rule (inherited FR/SR practice, not restated in the 2017 O.M. main text): no mileage for the 1st km by own car/hired taxi — 10 km × ₹30 → 9 × 30 = ₹270. Metered auto/public bus: actual fare, no deduction. Verify against the Ministry’s TA manual.',
'ch04-006':'State-wise RMA is a defence-accounts ILLUSTRATION (PCDA(O) Pune Circular 1/2024 dated 25.01.2024), not part of the civilian 2017 O.M. [uncertain — see source lines 1213–1227: the prose cites ₹15–₹30/km (Delhi ₹27.50, Karnataka ₹28.75 …) but the sample table lists ₹12–₹24 (Delhi 22, Karnataka 23 …); the source does not reconcile them.]',
'ch04-007':'Level 6, 40 km own car, no state rate → 40 × ₹30 = ₹1,200 (as the source’s worked example states it, without deducting the dead km); always check for a state rate first.',
'ch04-008':'Priority order: State DoT rate > neighbouring-state rate > default ₹30/₹15. Dead km not payable for own car/taxi.'},
hooks:{'ch04-005':'“Ten km, nine paid” — drop the dead kilometre before multiplying.'},
mcqs:[
{q:'Default mileage rate for own car/taxi where no state rate is prescribed (as per the guide’s current 25%-enhanced rates)?',o:['₹15/km','₹24/km','₹30/km','₹62.50/km'],a:2,why:'“₹30 per km (own car/taxi) and ₹15 per km (auto/own scooter etc.)”.',c:'ch04-004 (L1188–1201)'},
{q:'Which takes priority?',o:['Default ₹30/₹15 over state rate','State Directorate of Transport rate over neighbouring-state rate over default','Neighbouring-state rate over own-state rate','All are alternatives'],a:1,why:'Fact-Sheet: “State DoT rate > neighbouring-state rate > default ₹30/₹15”.',c:'ch04-008 (L1237–1246)'},
{q:'Applying the dead-kilometre rule, a 10 km own-car journey at ₹30/km yields:',o:['₹300','₹270','₹150','₹285'],a:1,why:'(10 − 1) × ₹30 = ₹270 per the micro-note.',c:'ch04-005 (L1202–1212)'},
{q:'The dead-km deduction applies to which journeys?',o:['Own car and hired taxi','Metered auto-rickshaw','Public bus','All road journeys'],a:0,why:'“This rule applies to own car and hired taxi journeys… auto-rickshaw (metered fare) or public bus, the actual fare paid is reimbursed without this deduction.”',c:'ch04-005'}],
cards:[
{f:'Default own car/taxi mileage (no state rate)?',b:'₹30 per km.',c:'ch04-004'},
{f:'Default auto-rickshaw / own scooter mileage?',b:'₹15 per km (on foot also ₹15/km).',c:'ch04-004'},
{f:'What overrides the ₹30/₹15 default?',b:'A rate prescribed by the Directorate of Transport of the State (or neighbouring State).',c:'ch04-004'},
{f:'Dead kilometre?',b:'No mileage for the first km of own-car/hired-taxi journeys; calculation begins from the 2nd km (inherited FR/SR practice).',c:'ch04-005'}]};
