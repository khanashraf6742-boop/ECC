#!/usr/bin/env python3
"""Build Batch 2 text, PDF and selected-voice script. No media generation or B1 edits.

Install subtitle-requirements.txt plus reportlab==5.1.0, then run this file.
Generate the ten JSON-listed speech clips with selected voice-01/voice-00;
then run build_batch2_video.py. Intermediate audio stays in ignored video-work/.
"""
import csv
from html import escape
import json
from pathlib import Path

from batch2_content import DATES, INTRO, ROWS, SOURCES
from batch2_roman import romanize, spoken

ROOT = Path(__file__).resolve().parent
GROUPS = [(0, 5), (5, 11), (11, 16), (16, 21), (21, 26),
          (26, 31), (31, 36), (36, 41), (41, 46)]
TITLES = ['Important dates: law and practical blocks', 'Rule 4: the five key terms',
          'Spouse, children and all three numerical exceptions', 'Wives, daughters, parents and dependency',
          'Income arithmetic, siblings, exclusions and marriage', 'All operative Rule 4 Task Force clauses and away family',
          'Counting HT/AI, separate travel and private spouse', 'Government spouses, suspension and single-leg facts',
          'Single-leg illustrations continued: five remaining cases', 'Child fares and family during study/training']


def dump(name, value):
    (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def content():
    cards = [dict(zip(('ref', 'title', 'spoken_ref_roman', 'rule', 'explanation_roman',
                       'example_roman', 'trap', 'source'), row), id=f'B2-{i:02}')
             for i, row in enumerate(ROWS, 1)]
    scripts = [dict(file='b2-01.mp3', voice='voice-01', title=TITLES[0], units=[],
                    text=spoken(INTRO), roman_text=INTRO)]
    for number, (start, end) in enumerate(GROUPS, 2):
        units = [dict(card_id=c['id'], spoken_ref=spoken(c['spoken_ref_roman']),
                      explanation=spoken(c['explanation_roman']), example=spoken(c['example_roman']))
                 for c in cards[start:end]]
        text = ' '.join(' '.join((u['spoken_ref'], u['explanation'], 'Example, ' + u['example'])) for u in units)
        scripts.append(dict(file=f'b2-{number:02}.mp3', voice='voice-00', title=TITLES[number - 1],
                            units=units, text=text, roman_text=romanize(text)))
    if [u['card_id'] for s in scripts for u in s['units']] != [c['id'] for c in cards]:
        raise ValueError('Every authored clause must be included exactly once in the narration')
    if any(len(s['text']) > 1500 for s in scripts):
        raise ValueError('Speech service character budget exceeded')
    for s in scripts:
        if romanize(s['text']) != s['roman_text']:
            raise ValueError('Speech/caption round-trip differs')
    dump('batch-02.json', dict(title='CCS LTC Batch 2: Rule 4, family and dependency',
         reviewed_on='2026-10-27', master_chapters=[4, 5, 6, 7, 8], sources=SOURCES,
         cards=cards, dates=DATES, status='Authored and source-reviewed; see media reports for build QA'))
    dump('batch-02-narration.json', scripts)
    return cards, scripts


NOTES = [
    'Scope: master chapters 4-8; every Rule 4 limb, the three child-number exceptions, operative Rule 4 GIDs, family FAQs 1-12 and 74-75. Reference first, then city-Hinglish explanation and an immediate hypothetical example. All examples are invented teaching cases, not actual departmental sanctions.',
    'Evidence review: 27 October 2026. The current family position is checked against the official July 2025 FAQ and September 2025 consolidation, with the original numbered GIDs cross-mapped. A publication/upload folder is not an amendment effective date. No verified later family amendment was identified in this review; this is not a guarantee that no later instrument exists.',
    'Critical correction to the uploaded master: parental/step-parent no-co-residence and minimum-pension-linked dependency were already in the 23 September 2008 instruction, not newly created in 2025. Current official sources confirm the substance. The standalone primary 2008 instrument was not retrieved; a secondary full-text reproduction corroborates the origin. Its claimed 1 September 2008 effective date is not certified in this edition.',
    'Second master correction: multiple births qualify for the numerical exception when the SECOND childbirth produces the excess; not every later set of twins. The normal child count is family-wide, not two per wife.',
    'Third master correction: the separate-hometown/independent-claims option for government spouses residing together dates to the 8 May 1990 decision, from block 1990-91 onwards. The old mandatory common-hometown/one-claim paragraph is the pre-decision position, not the operative conclusion.',
    'Fourth master correction: a declared valid All India option can have hometown as its destination. Destination alone does not mechanically decide HT versus All India. The family residence-to-HQ-and-back 2017 instruction cannot be reduced to a zero HQ-to-HQ ceiling, nor extended to unlimited fares for every other destination.',
    'Numbering crosswalk: historical Rule 4 Explanation 4 (sisters\' children) is Explanation 3 in the 2025 consolidation. Historical Explanation 3 (away-family fare cap) is reconciled with Notes 5(i)-(ii), the 2017 HQ-visit instruction and FAQs 74-75. Historical Explanation 5\'s Rs.1500 ceiling is obsolete; no old DR/stipend exclusion is silently carried into current FAQ 2.',
    'Calendar warning: the 2025 sources call 2022-25 current because that was their issue-year context. On 27 October 2026 the regular block is 2026-29. The 2022-25 carryover deadline is conditional: for a person eligible for HT LTC, carrying forward All India requires carryover of HT from the second two-year sub-block. Full Rule 8/9/10 mechanics and fresh-recruit personal blocks follow in the planned block batch.',
    'The assumed 50% DR in B2-17 is arithmetic ONLY, not today\'s notified DR. Always obtain the applicable minimum family pension and DR for the relevant date. A new pay commission\'s announcement does not by itself change the minimum used here.',
    'Training/study-leave cards compare family eligibility and fare anchors. Detailed domestic-training clauses, missions abroad, special-posting concessions, fresh recruits, general fare/ATA rules, claims/advance deadlines, encashment and spouse administration remain in their topic batches. Special Dispensation air segments require a valid applicable permission; this batch does not authenticate the reported September 2026 scheme extension.',
    'Coverage is batchwise, not a claim that all non-obsolete GIDs in the full series are already complete. GID (2) teaches the operative printed clauses (i), (ii), (vi); starred/deleted historical matter is not invented. GID (5) teaches the opening principle and all SIX illustrations. The register distinguishes actual coverage, partial comparisons and remaining work.',
    'The governing OM/order prevails if a consolidation is imprecise. This is educational material; the sanctioning office must verify journey facts, the applicable order, entitled class/route, documentation and available occasion.',
]

GRID = [
    ('Spouse', 'No', 'No', 'Legally married; one-wife rule and express exception'),
    ('Unmarried/step/legally adopted child', 'No', 'Yes', 'Two eldest surviving; Explanation 1 exceptions; no 25-year ceiling'),
    ('Divorced/abandoned/separated/widowed daughter', 'Yes', 'Yes', 'Listed marital status; not an ordinarily married daughter'),
    ('Parents/stepmother/stepfather', 'No', 'Yes', 'Not parents-in-law or grandparents'),
    ('Unmarried minor brother', 'Yes', 'Yes', 'Minor; parents dead or themselves dependent'),
    ('Unmarried/divorced/abandoned/separated/widowed sister', 'Yes', 'Yes', 'No minor-only restriction; parents dead or themselves dependent'),
    ('Children of eligible daughters/sisters', 'Not applicable', 'Not applicable', 'Excluded as such; no inherited eligibility'),
]


def documents(cards):
    title = 'CCS LTC — Batch 2: Family, Dependency & Definitions'
    intro = '\n\n'.join(NOTES)
    md = f'# {title}\n\nReviewed: 27 October 2026. Selected voices: teacher voice-00, questioner voice-01.\n\n'
    md += '## Important dates first\n\n' + '\n'.join(f'- **{d}:** {t}' for d, t in DATES)
    md += '\n\n## Scope, currentness and corrections\n\n' + intro
    md += '\n\n## Comparative eligibility grid\n\nCategory | Co-residence required? | Dependency tested? | Other conditions\n--- | --- | --- | ---\n'
    md += '\n'.join(' | '.join(row) for row in GRID)
    sections = []
    for c in cards:
        sources = '; '.join(f'[{s}]({SOURCES[s]["url"]})' for s in c['source'].split(';'))
        md += (f'\n\n## {c["id"]} — {c["title"]}\n\n**Exact reference:** {c["ref"]}\n\n'
               f'**Rule / current restatement (not a verbatim quotation):** {c["rule"]}\n\n'
               f'**Simple city Hinglish:** {c["explanation_roman"]}\n\n'
               f'**Immediate hypothetical example:** {c["example_roman"]}\n\n'
               f'**Watch out:** {c["trap"]}\n\n**Evidence:** {sources}\n')
        sections.append('<section id="' + c['id'] + '"><small>' + c['id'] + '</small><h2>' + escape(c['title']) + '</h2>'
             + '<p class="ref">' + escape(c['ref']) + '</p>'
             + ''.join('<p><b>' + label + '</b> ' + escape(c[key]) + '</p>' for label, key in
               [('Rule / current restatement:', 'rule'), ('Simple city Hinglish:', 'explanation_roman'),
                ('Immediate hypothetical example:', 'example_roman'), ('Watch out:', 'trap')])
             + '<p>Evidence: ' + '; '.join('<a href="' + escape(SOURCES[s]['url'], quote=True) + '">' + s + '</a>'
                                         for s in c['source'].split(';')) + '</p></section>')
    md += '\n## Sources and evidence limits\n\n' + '\n'.join(f'- **{key}: {s["title"]}** — {s["url"]}\n  {s["use"]}' for key, s in SOURCES.items())
    md += '\n\n## Series status\n\nBatch 1 delivered. Batch 2 covers the cards above. Remaining topic batches and their unreviewed GIDs remain pending. See `gid-coverage-register.csv`; see `BATCH-02-README.md` for build and QA details.\n'
    (ROOT / 'batch-02.md').write_text(md)
    css = ('body{font:18px/1.65 system-ui,sans-serif;background:#0c1424;color:#eaf0fa;margin:auto;max-width:1050px;padding:32px}'
           'h1,h2{line-height:1.2}h1{font-size:42px}h2{color:#7bd9ff}a{color:#81e8c0}small{color:#ffd980}'
           'section{background:#142139;border:1px solid #334762;border-radius:16px;margin:24px 0;padding:26px;break-inside:avoid}'
           '.ref{color:#ffda70;font-weight:700}td,th{border:1px solid #40516b;padding:10px;text-align:left}table{border-collapse:collapse;width:100%}'
           '@media print{body{color:black;background:white;padding:0}section{color:black;background:white;border-color:#aaa}h2,a,.ref{color:#163955}}')
    table = '<table><thead><tr>' + ''.join('<th>' + escape(v) + '</th>' for v in ('Category', 'Co-residence?', 'Dependency?', 'Other conditions')) + '</tr></thead><tbody>'
    table += ''.join('<tr>' + ''.join('<td>' + escape(v) + '</td>' for v in row) + '</tr>' for row in GRID) + '</tbody></table>'
    html = ('<!doctype html><html lang="en-IN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>' + escape(title) + '</title><style>' + css + '</style><main><h1>' + escape(title) + '</h1>'
            '<p>Reviewed 27 October 2026 · 46 exact-reference cards · Roman city Hinglish</p>'
            '<p><a href="batch-02-video.mp4">Video</a> · <a href="batch-02-hinglish.mp3">Audio</a> · <a href="batch-02.pdf">PDF</a> · <a href="batch-02-video.srt">Subtitles</a></p>'
            '<h2>Important dates first</h2><ul>' + ''.join('<li><b>' + escape(d) + '</b>: ' + escape(t) + '</li>' for d, t in DATES)
            + '</ul><h2>Scope, currentness and corrections</h2>' + ''.join('<p>' + escape(n) + '</p>' for n in NOTES)
            + '<h2>Comparative eligibility grid</h2>' + table + ''.join(sections)
            + '<h2>Sources and evidence limits</h2>' + ''.join('<p><b>' + k + ': ' + escape(s['title']) + '</b><br><a href="'
              + escape(s['url'], quote=True) + '">' + escape(s['url']) + '</a><br>' + escape(s['use']) + '</p>' for k, s in SOURCES.items())
            + '<p>Remaining LTC topic batches and their GIDs are pending. See the coverage register.</p></main></html>')
    (ROOT / 'batch-02.html').write_text(html)
    pdf(cards, title)


def pdf(cards, title):
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether
    pdfmetrics.registerFont(TTFont('Atkinson', str(ROOT / 'video-fonts/AtkinsonHyperlegible-Regular.ttf')))
    pdfmetrics.registerFont(TTFont('AtkinsonBold', str(ROOT / 'video-fonts/AtkinsonHyperlegible-Bold.ttf')))
    pdfmetrics.registerFontFamily('Atkinson', normal='Atkinson', bold='AtkinsonBold', italic='Atkinson', boldItalic='AtkinsonBold')
    styles = getSampleStyleSheet()
    for name in ('BodyText', 'Normal', 'Heading1', 'Heading2', 'Title'):
        styles[name].fontName = 'Atkinson'
        styles[name].leading = styles[name].fontSize * 1.35
    styles['BodyText'].fontSize = 10.5
    styles['BodyText'].leading = 14
    story = [Paragraph(escape(title), styles['Title']), Paragraph('Reviewed 27 October 2026. Educational restatements, not an official sanction.', styles['BodyText']), Spacer(1, 12), Paragraph('Important dates first', styles['Heading1'])]
    for date, text in DATES:
        story.append(Paragraph('<b>' + escape(date) + '</b> — ' + escape(text), styles['BodyText']))
    story += [PageBreak(), Paragraph('Scope, currentness and corrections', styles['Heading1'])]
    for note in NOTES:
        story += [Paragraph(escape(note), styles['BodyText']), Spacer(1, 7)]
    story += [PageBreak(), Paragraph('Comparative eligibility grid', styles['Heading1'])]
    table = [[Paragraph(escape(str(t)), styles['BodyText']) for t in row] for row in
             [('Category', 'Reside with?', 'Income test?', 'Other conditions')] + GRID]
    grid = Table(table, colWidths=[135, 75, 75, 225], repeatRows=1)
    grid.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('GRID', (0, 0), (-1, -1), .4, colors.grey), ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d9edf8'))]))
    story += [grid, PageBreak()]
    for c in cards:
        story.append(KeepTogether([Paragraph(c['id'] + ' — ' + escape(c['title']), styles['Heading2']), Paragraph('<b>Exact reference:</b> ' + escape(c['ref']), styles['BodyText'])]))
        for label, key in [('Current restatement', 'rule'), ('Simple city Hinglish', 'explanation_roman'),
                           ('Immediate hypothetical example', 'example_roman'), ('Watch out', 'trap')]:
            story += [Paragraph('<b>' + label + ':</b> ' + escape(c[key]), styles['BodyText']), Spacer(1, 5)]
        story += [Paragraph('Evidence: ' + escape(c['source']), styles['BodyText']), Spacer(1, 16)]
    story += [PageBreak(), Paragraph('Sources and evidence limits', styles['Heading1'])]
    for key, source in SOURCES.items():
        story += [Paragraph(key + ': ' + escape(source['title']), styles['Heading2']),
                  Paragraph('<link href="' + escape(source['url'], quote=True) + '">' + escape(source['url']) + '</link>', styles['BodyText']),
                  Paragraph(escape(source['use']), styles['BodyText'])]
    def footer(canvas, doc):
        canvas.setFont('Atkinson', 9)
        canvas.drawString(42, 24, 'CCS LTC | Batch 2 | reviewed 27 October 2026 | education, not sanction')
        canvas.drawRightString(555, 24, str(doc.page))
    SimpleDocTemplate(str(ROOT / 'batch-02.pdf'), pagesize=A4, rightMargin=42, leftMargin=42,
                      topMargin=42, bottomMargin=42, title=title, author='LTC learning series').build(story, onFirstPage=footer, onLaterPages=footer)


def register():
    path = ROOT / 'gid-coverage-register.csv'
    with path.open(newline='') as f:
        reader = csv.DictReader(f)
        fields, rows = reader.fieldnames, list(reader)
    covered = {'4.1': 'B2-21', '4.2': 'B2-22;B2-23;B2-24', '4.2.i': 'B2-22', '4.2.ii': 'B2-23', '4.2.vi': 'B2-24',
               '4.3': 'B2-01', '4.4': 'B2-25;B2-26;B2-28', '7.5': 'B2-35;B2-36;B2-37;B2-38;B2-39;B2-40;B2-41',
               '7.5.I.i': 'B2-36', '7.5.I.ii': 'B2-37', '7.5.II.i': 'B2-38', '7.5.II.ii': 'B2-39', '7.5.II.iii': 'B2-40;B2-42;B2-43;B2-44', '7.5.II.iv': 'B2-41',
               '7.15': 'B2-34', '7.17': 'B2-45', '7.17.a': 'B2-45', '7.17.b.i': 'B2-45', '7.17.b.ii': 'B2-45', '7.18': 'B2-32;B2-33'}
    partial = {'7.20': 'B2-46', '7.20.iii': 'B2-46', 'M-2025-FAQ': 'B2-06;B2-07;B2-08;B2-13;B2-14;B2-15;B2-16;B2-17;B2-18;B2-19;B2-20;B2-25;B2-26;B2-27;B2-28;B2-29;B2-30;B2-31;B2-34;B2-42;B2-43;B2-44', 'M-2025-GUIDE': 'B2-01 through B2-46 (Rule 4/family portions only)'}
    changed = []
    for row in rows:
        ident = row['id']
        if ident in covered:
            note = 'Batch 2 exact-reference explanation + example. Reviewed against current July/September 2025 family instructions; detailed future topic treatment is not removed.'
            if ident == '4.2': note += ' Operative printed (i), (ii), (vi) covered; starred/deleted matter not reconstructed.'
            if ident == '4.4': note += ' Ordinary cap retained; 2017 family-to-HQ exception explicitly reconciled.'
            if ident == '7.18': note += ' 1990 operative option distinguished from superseded pre-decision common-hometown paragraph.'
            row = {**row, 'current_status': 'operative-text-reviewed-with-later-family-instructions', 'coverage_status': 'covered-in-batch-2', 'video_card': covered[ident], 'review_note': note}
        elif ident in partial:
            row = {**row, 'coverage_status': 'partially-covered-in-batch-2', 'video_card': partial[ident], 'review_note': 'Only family/anchor comparison or family subset taught; full parent topic still pending. Do not mark the complete instrument covered.'}
        changed.append(row)
    additions = [
        ('M-2008-FAMILY', 'Parents/step-parents, dependency and preserved relation conditions', '31011/4/2008-Estt.(A)', '2008-09-23', 'B2-13;B2-15;B2-16;B2-17', 'G25'),
        ('M-2017-FAMILY', 'Family residence to headquarters and back; full entitled fare', '31011/5/2015-Estt.(A-IV)', '2017-10-31', 'B2-25;B2-26;B2-27;B2-28', 'G25'),
        ('M-2016-2018-CHILD', '5-to-under-12 rail fare and under-5 rail/ordinary air restrictions', '31011/3/2016-Estt.(A-IV)', '2016-04-29;2018-05-16', 'B2-40;B2-42;B2-43;B2-44', 'F25'),
    ]
    for ident, topic, authority, date, ids, source in additions:
        replacement = dict(id=ident, record_type='modern-instruction', topic=topic, authority=authority,
            issue_date=date, planned_batch='2', current_status='operative-family-subject-reviewed', coverage_status='covered-in-batch-2',
            video_card=ids, source=SOURCES[source]['url'], review_note='Subject-specific family/child provisions, not every subject in the parent OM. Current substance checked against official 2025 sources.' + (' 2008 origin corroborated by secondary reproduction; standalone original primary not retrieved.' if ident == 'M-2008-FAMILY' else ''))
        changed = [row for row in changed if row['id'] != ident] + [replacement]
    with path.open('w', newline='') as f:
        writer = csv.DictWriter(f, fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(changed)


def main():
    cards, scripts = content()
    documents(cards)
    # Register updated after successful media QA only; this script prepares content, not proof of coverage.
    print('Prepared', len(cards), 'cards;', len(scripts), 'clips:', [len(s['text']) for s in scripts])


if __name__ == '__main__':
    main()
