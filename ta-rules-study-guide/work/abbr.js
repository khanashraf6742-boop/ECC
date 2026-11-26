// Abbreviations list: only entries whose abbreviation AND expansion both occur in the source are kept.
const fs=require('fs');const {strip}=require('./classify');
const text=strip(fs.readFileSync(__dirname+'/source.html','utf8').replace(/<style[\s\S]*?<\/style>/g,'')).replace(/\s+/g,' ');
const C=[
['TA','Travelling Allowance'],['DA','Daily Allowance'],['DA','Dearness Allowance'],['CTG','Composite Transfer Grant'],['TTA','Transfer Travelling Allowance'],
['HQ','headquarters'],['DoE','Department of Expenditure'],['MoF','Ministry of Finance'],['DoPT','Department of Personnel'],['O.M.','Office Memorandum'],
['CPC','Pay Commission'],['FR','Fundamental Rules'],['SR','Supplementary Rules'],['GFR','General Financial Rules'],['GIO','Government of India'],
['LTC','Leave Travel Concession'],['ATA','Authorized Travel Agent'],['RMA','Road Mileage Allowance'],['NER','North-Eastern Region'],['A&N','Andaman & Nicobar'],
['DDO','Drawing and Disbursing Officer'],['CCS','Central Civil Services'],['HRA','House Rent Allowance'],['NPS','National Pension System'],
['PCDA','PCDA'],['CAPF','Central Armed Police Forces'],['PSU','PSU'],['LDCE','LDCE'],['UA','Urban Agglomeration'],['SCL','Special Casual Leave'],
['RH','Restricted Holiday'],['PML','Pay Matrix Level'],['DR','Dearness Relief'],['FA','Financial Advisor'],['HoD','Head of Department'],
['JCM','Joint Consultative Machinery'],['RPwD','RPwD'],['DFPR','DFPR'],['CEA','Children Education Allowance'],['BLCL','Balmer Lawrie'],
['ATT','Ashok Travels'],['SCI','Shipping Corporation of India'],['GPF','GPF'],['MTS','Multi-Tasking Staff'],['UPSC','UPSC'],['SSC','SSC'],
['IRCTC','Indian Railways Catering and Tourism Corporation'],['ITDC','ITDC'],['PNR','PNR'],['EL','Earned Leave'],['HPL','HPL'],['CCL','CCL'],
['GST','Goods and Services Tax'],['NOC','NOC'],['PRAN','PRAN'],['PRA','PRA'],['AITTSL','AITTSL'],['NESTS','NESTS'],['DGT','DGT'],['ISTM','ISTM'],
['PTC','PTC'],['P&T','P&T'],['AO','AO'],['SO','Section Officer'],['LDC','Lower Division Clerk'],['UDC','Upper Division Clerk'],['MCQ','MCQ'],['PYQ','PYQ'],
['GP','Grade Pay'],['PB','PB'],['TPTA','TPTA'],['NPS','NPS'],['CGA','Controller General of Accounts'],['TRG','TRG'],['GSR','G.S.R.'],['CBI','CBI'],
['FAQ','FAQ'],['w.e.f.','w.e.f.'],['DoP','DoP'],['VPS','x']];
const out=[];const seen=new Set();
for(const [a,e] of C){if(e==='x')continue;const k=a+'|'+e;if(seen.has(k))continue;seen.add(k);
  const hasE=new RegExp(e.replace(/[.*+?^${}()|[\]\\]/g,'\\$&').replace(/ /g,'\\s+'),'i').test(text);
  const hasA=new RegExp('(^|[^A-Za-z])'+a.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'([^A-Za-z]|$)').test(text);
  if(hasE&&hasA&&a!==e)out.push([a,e]);}
fs.writeFileSync(__dirname+'/abbr.json',JSON.stringify(out,null,1));
console.log(out.length,'kept of',C.length);console.log(out.map(x=>x.join('=')).join('; '));
