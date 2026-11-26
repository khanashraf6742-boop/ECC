import re


def edit(path, fn):
    s = open(path).read()
    t = fn(s)
    open(path, 'w').write(t)


def drop_lines(s, pred):
    return '\n'.join(l for l in s.split('\n') if not pred(l)) + ('\n' if s.endswith('\n') else '')


# ---------------- official.js
def f(s):
    s = drop_lines(s, lambda l: any(k in l for k in [
        "(LTC air Special Dispensation extended", "(LTC air booking) — enclosure", "(LTC air modifications) — enclosure",
        "54 TA/DA/LTC FAQs", "16.07.2026 (LTC air)"]))
    s = s.replace("; adds para 3–4 (date of submission), para 6 (LTC excluded), para 7 — supplement S7.", "; adds para 3–4 (date of submission) and para 7 — supplement S7.")
    s = s.replace("Rules 224, 290, 291, 292, 295", "Rules 224, 290, 291, 295")
    s = re.sub(r"Rule 290 wording and Rule 292 LTC periods — errata E9, E13\.", "Rule 290 wording — errata E13.", s)
    s = s.replace("'DoPT LTC FAQ 01.07.2025 and the DoPT Joining Time Rules consolidation (documents.doptcirculars.nic.in)", "'The DoPT Joining Time Rules consolidation (documents.doptcirculars.nic.in)")
    s = re.sub(r" \(DoPT O\.M\. 29\.08\.2022 was later read as an enclosure — see S13\.\)", "", s)
    s = s.replace("(domestic incl. LTC, and international)", "(domestic and international)")
    # E9: keep only the TTA reason
    a = s.index("['E9',")
    b = s.index("\n", a)
    s = s[:a] + "['E9','TTA para 3.6.3 is stated without its reason (ch13-003).','DoPT O.M. 24.11.2022 para 3.6.3 (NESTS reproduction) adds that temporary Central Government employees with under 3 years’ regular continuous service are “not entitled for joining time pay under Joining Time Rules”.','Add the reason; the interaction with Rule 4(4) stays [uncertain] (G.S.R. 229(E) not retrieved).']," + s[b:]
    return s


edit('official.js', f)


# ---------------- official2.js
def g(s):
    s = re.sub(r"\n'ch10-008':'LTC air Special Dispensation[^\n]*", "", s)
    s = re.sub(r" The DoPT LTC-air O\.M\. of 29\.08\.2022 \(read from an enclosure\)[^']*?S13\.", "", s)
    s = s.replace("S7 — O.M. 13.03.2018: date of submission, LTC exclusion, supersession", "S7 — O.M. 13.03.2018: date of submission and supersession")
    s = re.sub(r"<li><b>Para 6:</b> not applicable to LTC claims \(separate DoPT rules\)\. <b>Para 7:</b> effective from date of issue\.</li>", "<li><b>Para 7:</b> effective from date of issue.</li>", s)
    # remove S12 and S13 blocks
    a = s.index("{id:'off-s12'")
    b = s.index("{id:'off-s14'")
    s = s[:a] + s[b:]
    s = s.replace("(domestic incl. LTC, and international)", "(domestic and international)")
    s = s.replace("At least 21 days encouraged (tour and LTC);", "At least 21 days encouraged;")
    s = drop_lines(s, lambda l: l.startswith("['LTC','Due next day"))
    s = s.replace(" LTC is outside this O.M.", "")
    s = drop_lines(s, lambda l: any(k in l for k in ["LTC air Special Dispensation Scheme (NER", "DoPT LTC-air O.M. of 29.08.2022, cancelling", "October 2023 DoPT O.M. says booking LTC",
                                                       "['LTC air Special Dispensation Scheme — validity", "['LTC air: how many ATAs", "['O.M. 13.03.2018 — LTC?"]))
    s = s.replace("(domestic incl. LTC, and international)", "(domestic and international)")
    return s


edit('official2.js', g)


# ---------------- meta.js
def h(s):
    s = drop_lines(s, lambda l: any(k in l for k in ["['LTC air: 21-day", "['DoPT LTC-air O.M.s", "['LTC air Special Dispensation extended", "['LTC claim periods", "['LTC periods"]))
    s = re.sub(r"\['26 Nov 2026','Staff News check:[^\n]*", "['26 Nov 2026','Staff News checked: no TA-rule order newer than 12.09.2022 found; LTC items are out of scope for this guide and were left out. DoPT O.M. 24.11.2022 para 3.6.3 text confirmed.'],", s)
    s = re.sub(r"'DoPT LTC FAQ \(01\.07\.2025\), Joining Time Rules consolidation, G\.S\.R\. 229\(E\) — hosts unreachable; need files from you\.[^']*'", "'DoPT Joining Time Rules consolidation and G.S.R. 229(E) — hosts unreachable; need files from you.'", s)
    s = s.replace("['Para 3.6.3: TTA for temporary staff under 3 years'", "['Para 3.6.3: TTA for temporary staff under 3 years'")
    return s


edit('meta.js', h)


# ---------------- extra.js
def i(s):
    s = drop_lines(s, lambda l: "TA claim for LTC take to fall due" in l or l.startswith("['LTC periods'"))
    s = s.replace("o:['LTC claims','Retired servants", "o:['Advances','Retired servants")
    s = s.replace("['Air for Levels 6–8','Not allowed','Economy air on tour; not on LTC (CCS (LTC) Rule 12 position)','ch02-004, ch10-008']", "['Air for Levels 6–8','Not allowed','Economy air on tour (Table A, Levels 6 to 11)','ch02-004']")
    return s


edit('extra.js', i)


# ---------------- tables.js: drop TA-vs-LTC table
def j(s):
    a = s.index("{seg:'ch10',title:'TA on tour/transfer vs LTC")
    b = s.index("{seg:'ch07',title:'Who bears the cost")
    return s[:a] + s[b:]


edit('tables.js', j)


# ---------------- svgs.js
def k(s):
    s = s.replace("['Step 1  Official duty or personal LTC?','Official duty / transfer / retirement / training / special family case → Step 2. Personal LTC → Step 3. Defence / CAPF / separately governed → identify the service-specific authority.']",
                  "['Step 1  Is this civilian official TA?','Official duty / transfer / retirement / training / special family case → Step 2. Defence / CAPF / separately governed → identify the service-specific authority.']")
    s = re.sub(r"\n\s*\['Step 3  If LTC: mode and advance status'[^\n]*", "", s)
    s = s.replace("['Separate the four clocks'", "['Step 3  Separate the four clocks'")
    return s


edit('svgs.js', k)

# ---------------- aids
edit('aids/ch06.js', lambda s: s.replace("; no LTC for pensioners.", ".").replace("; no LTC.", "."))
edit('aids/ch07.js', lambda s: s.replace(" LTC = tour entitlement with 3 exceptions (different air entitlement for L6–8, no DA, transport mode rule).", ""))
edit('aids/ch11.js', lambda s: s.replace(" LTC: separate home towns; child claimed by one spouse per block; 10-day leave encashment each (career max 60 days).", ""))


def m(s):
    s = re.sub(r"\n'ch10-008':'LTC vs TA[^\n]*", "", s)
    s = s.replace(" LTC-air O.M. 29.08.2022: 21-day booking = encouragement; LTC-advance request ≥30 days for air-entitled. 16.07.2026 DGT-hosted circular: DoPT officers/officials, LTC air only.", "")
    s = drop_lines(s, lambda l: "Pay Levels 6 to 8 on LTC" in l or l.startswith("{f:'LTC vs TA on DA?'"))
    return s


edit('aids/ch10.js', m)
