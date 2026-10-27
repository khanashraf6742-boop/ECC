#!/usr/bin/env python3
"""Build Batch 4 text, PDF and selected-voice script. No media generation or B1 edits.

Install subtitle-requirements.txt plus reportlab==5.1.0, then run this file.
Generate the ten JSON-listed speech clips with selected voice-01/voice-00;
then run build_batch4_video.py. Intermediate audio stays in ignored video-work/.
"""
import csv
from html import escape
import json
from pathlib import Path

from batch4_content import DATES, INTRO, ROWS, SOURCES, NOTES, GRID
from batch4_roman import romanize, spoken

ROOT = Path(__file__).resolve().parent
GROUPS = [(0, 9), (9, 17), (17, 25), (25, 33), (33, 42), (42, 51), (51, 60), (60, 68), (68, 77)]
TITLES = ['Important dates, service gate and current blocks',
          'Rule 7: service, leave, resignation and technical-resignation gate',
          'Technical-resignation conditions; suspension self versus family',
          'Route ceiling, class, evidence, records and foreign hometown',
          'Tour/transfer combinations and Missions abroad',
          'Missions, Nepal Aid, AIS and non-top PSU options',
          'PSU options and top posts; study leave and training-HQ caution',
          'Training in India/abroad; escort conditions one to four',
          'Escort condition five; posted-staff annual and Emergency Passage options',
          'Fresh-recruit comparison, cancellation, deputation advance and booking charges']


def dump(name, value):
    (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def content():
    cards = [dict(zip(('ref', 'title', 'spoken_ref_roman', 'rule', 'explanation_roman',
                       'example_roman', 'trap', 'source'), row), id=f'B4-{i:02}')
             for i, row in enumerate(ROWS, 1)]
    scripts = [dict(file='b4-01.mp3', voice='voice-01', title=TITLES[0], units=[],
                    text=spoken(INTRO), roman_text=INTRO)]
    for number, (start, end) in enumerate(GROUPS, 2):
        units = [dict(card_id=c['id'], spoken_ref=spoken(c['spoken_ref_roman']),
                      explanation=spoken(c['explanation_roman']), example=spoken(c['example_roman']))
                 for c in cards[start:end]]
        text = ' '.join(' '.join((u['spoken_ref'], u['explanation'], 'Example, ' + u['example'])) for u in units)
        scripts.append(dict(file=f'b4-{number:02}.mp3', voice='voice-00', title=TITLES[number - 1],
                            units=units, text=text, roman_text=romanize(text)))
    if [u['card_id'] for s in scripts for u in s['units']] != [c['id'] for c in cards]:
        raise ValueError('Every authored clause must be included exactly once in the narration')
    if any(len(s['text']) > 1500 for s in scripts):
        raise ValueError('Speech service character budget exceeded')
    for s in scripts:
        if romanize(s['text']) != s['roman_text']:
            raise ValueError('Speech/caption round-trip differs')
    dump('batch-04.json', dict(title='CCS LTC Batch 4: Rule 7, leave and special service situations',
         reviewed_on='2026-10-27', master_chapters=[10, 11, 12, 13, 14, 15], sources=SOURCES,
         cards=cards, dates=DATES, status='Authored and source-reviewed; see media reports for build QA'))
    dump('batch-04-narration.json', scripts)
    return cards, scripts


def documents(cards):
    title = 'CCS LTC — Batch 4: Admissibility, Leave & Special Situations'
    intro = '\n\n'.join(NOTES)
    md = f'# {title}\n\nReviewed: 27 October 2026. Selected voices: teacher voice-00, questioner voice-01.\n\n'
    if not (ROOT / 'batch-04-video-report.json').exists():
        md += '**Written companion release; video/audio not yet released.** A speech omission was detected during acoustic QA. See `BATCH-04-README.md`.\n\n'
    md += '## Important dates first\n\n' + '\n'.join(f'- **{d}:** {t}' for d, t in DATES)
    md += '\n\n## Scope, currentness and corrections\n\n' + intro
    md += '\n\n## Approval and authority grid\n\nQuestion | Who acts? | Conditions | Reference\n--- | --- | --- | ---\n'
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
    md += '\n\n## Series status\n\nBatches 1-3 delivered unchanged. Batch 4 covers the cards above. Remaining topic batches and their unreviewed GIDs remain pending. See `gid-coverage-register.csv`; see `BATCH-04-README.md` for build and QA details.\n'
    (ROOT / 'batch-04.md').write_text(md)
    css = ('body{font:18px/1.65 system-ui,sans-serif;background:#0c1424;color:#eaf0fa;margin:auto;max-width:1050px;padding:32px}'
           'h1,h2{line-height:1.2}h1{font-size:42px}h2{color:#7bd9ff}a{color:#81e8c0}small{color:#ffd980}'
           'section{background:#142139;border:1px solid #334762;border-radius:16px;margin:24px 0;padding:26px;break-inside:avoid}'
           '.ref{color:#ffda70;font-weight:700}td,th{border:1px solid #40516b;padding:10px;text-align:left}table{border-collapse:collapse;width:100%}'
           '@media print{body{color:black;background:white;padding:0}section{color:black;background:white;border-color:#aaa}h2,a,.ref{color:#163955}}')
    table = '<table><thead><tr>' + ''.join('<th>' + escape(v) + '</th>' for v in ('Question', 'Who acts?', 'Conditions', 'Reference')) + '</tr></thead><tbody>'
    table += ''.join('<tr>' + ''.join('<td>' + escape(v) + '</td>' for v in row) + '</tr>' for row in GRID) + '</tbody></table>'
    html = ('<!doctype html><html lang="en-IN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>' + escape(title) + '</title><style>' + css + '</style><main><h1>' + escape(title) + '</h1>'
            '<p>Reviewed 27 October 2026 · 77 exact-reference cards · Roman city Hinglish</p>'
            '<p><a href="batch-04-video.mp4">Video</a> · <a href="batch-04-hinglish.mp3">Audio</a> · <a href="batch-04.pdf">PDF</a> · <a href="batch-04-video.srt">Subtitles</a></p>'
            '<h2>Important dates first</h2><ul>' + ''.join('<li><b>' + escape(d) + '</b>: ' + escape(t) + '</li>' for d, t in DATES)
            + '</ul><h2>Scope, currentness and corrections</h2>' + ''.join('<p>' + escape(n) + '</p>' for n in NOTES)
            + '<h2>Approval and authority grid</h2>' + table + ''.join(sections)
            + '<h2>Sources and evidence limits</h2>' + ''.join('<p><b>' + k + ': ' + escape(s['title']) + '</b><br><a href="'
              + escape(s['url'], quote=True) + '">' + escape(s['url']) + '</a><br>' + escape(s['use']) + '</p>' for k, s in SOURCES.items())
            + '<p>Remaining LTC topic batches and their GIDs are pending. See the coverage register.</p></main></html>')
    (ROOT / 'batch-04.html').write_text(html)
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
    if not (ROOT / 'batch-04-video-report.json').exists():
        story.insert(2, Paragraph('<b>Written companion release:</b> video/audio held for a detected speech omission; see BATCH-04-README.md.', styles['BodyText']))
    for date, text in DATES:
        story.append(Paragraph('<b>' + escape(date) + '</b> — ' + escape(text), styles['BodyText']))
    story += [PageBreak(), Paragraph('Scope, currentness and corrections', styles['Heading1'])]
    for note in NOTES:
        story += [Paragraph(escape(note), styles['BodyText']), Spacer(1, 7)]
    story += [PageBreak(), Paragraph('Approval and authority grid', styles['Heading1'])]
    table = [[Paragraph(escape(str(t)), styles['BodyText']) for t in row] for row in
             [('Question', 'Who acts?', 'Conditions', 'Reference')] + GRID]
    grid = Table(table, colWidths=[95, 145, 165, 105], repeatRows=1)
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
        canvas.drawString(42, 24, 'CCS LTC | Batch 4 | reviewed 27 October 2026 | education, not sanction')
        canvas.drawRightString(555, 24, str(doc.page))
    SimpleDocTemplate(str(ROOT / 'batch-04.pdf'), pagesize=A4, rightMargin=42, leftMargin=42,
                      topMargin=42, bottomMargin=42, title=title, author='LTC learning series').build(story, onFirstPage=footer, onLaterPages=footer)


def register():
    """Cumulative actual coverage, retaining every earlier teaching pointer."""
    path = ROOT / 'gid-coverage-register.csv'
    with path.open(newline='') as f:
        reader = csv.DictReader(f)
        fields, rows = reader.fieldnames, list(reader)
    covered = {
        '7.1': 'B4-04;B4-18 through B4-23', '7.1.route': 'B4-18', '7.1.class': 'B4-19', '7.1.notice': 'B4-20;B4-21', '7.1.record': 'B4-22;B4-23', '7.1.vacation': 'B4-04', '7.2': 'B4-08 through B4-15',
        '7.3': 'B4-24;B4-25', '7.3.abroad': 'B4-24', '7.7': 'B4-26 through B4-31',
        '7.7.i': 'B4-26;B4-27', '7.7.ii.a': 'B4-28;B4-30', '7.7.ii.b': 'B4-29;B4-30',
        '7.8': 'B4-32 through B4-35', '7.8.i': 'B4-32', '7.8.ii.a': 'B4-33', '7.8.ii.b': 'B4-34', '7.8.iii': 'B4-35',
        '7.10': 'B4-36;B4-37', '7.11': 'B4-38 through B4-40', '7.11.blocks': 'B4-38', '7.11.cost': 'B4-39', '7.11.unused': 'B4-40',
        '7.12': 'B4-41 through B4-43', '7.14': 'B4-44', '7.16': 'B4-45 through B4-47',
        '7.19': 'B4-57 through B4-61', '7.19.i': 'B4-57', '7.19.ii': 'B4-58', '7.19.iii': 'B4-59', '7.19.iv': 'B4-60', '7.19.v': 'B4-61',
        '7.20': 'B4-51 through B4-56', '7.20.i': 'B4-51', '7.20.ii': 'B4-52 through B4-54', '7.20.iii': 'B4-55;B4-56'}
    repeated = {'7.18': 'B4-68 (operative option comparison)', '7.15': 'B4-16;B4-17', '7.17': 'B4-48 through B4-50', '7.17.a': 'B4-48', '7.17.b.i': 'B4-49', '7.17.b.ii': 'B4-50',
                '15.1': 'B4-72 through B4-74', '15.1.a': 'B4-72', '15.1.b': 'B4-73', '15.1.c': 'B4-74',
                'M-2025-FAQ': 'B4-03;B4-05;B4-06;B4-16;B4-17;B4-70;B4-75;B4-77 (selected FAQs only)',
                'M-2025-GUIDE': 'B4-01 through B4-77 (admissibility subset; training discrepancy disclosed)'}
    result = []
    for row in rows:
        ident = row['id']
        pointer = covered.get(ident, repeated.get(ident))
        if pointer:
            previous = '' if row['video_card'].startswith('B4-') else row['video_card'].split('; B4-')[0]
            status = 'covered-in-batch-4' if ident in covered or ident.startswith('15.1') else row['coverage_status']
            row = {**row, 'coverage_status': status,
                   'current_status': 'operative-reviewed-training-source-tension-disclosed' if ident.startswith('7.20') else row['current_status'],
                   'video_card': (previous + '; ' if previous else '') + pointer,
                   'review_note': 'Cumulative reference-first explanation + example; older pointers retained. Training HQ wording tension, source-host limits, technical-resignation exception and later family rules explicitly reconciled. Modern parent instruments remain partial.'}
            if status == 'covered-in-batch-4' and not ident.startswith('7.20'):
                row = {**row, 'current_status': 'operative-subject-reviewed-with-current-consolidation'}
        result.append(row)
    additions = [
        ('M-2022-TECH', 'Technical resignation: qualifying route, pre-service application conditions and LTC preservation', 'DOPT-1669266628362;28020/1/2010-Estt.(C)', '2022-11-24;2016-08-17', 'B4-09 through B4-15', 'T22'),
        ('M-2018-POSTED', 'Posted-staff normal/annual election and emergency passage; restricted family and effective date', '31011/12/2015-Estt.(A-IV)', '2018-04-24;2020-02-28', 'B4-62 through B4-67', 'P18'),
        ('M-2007-COMBINE', 'All-India LTC extension to tour/transfer combinations; historical transition', '31011/3/2006-Estt.(A)', '2007-02-07', 'B4-31', 'C07'),
        ('M-2018-CCL', 'CCL as qualifying leave; no extra LTC occasion', '13018/6/2013-Estt(L)', '2018-04-03', 'B4-03;B4-07', 'F25')]
    for ident, topic, authority, date, pointer, source in additions:
        replacement = dict(id=ident, record_type='modern-instruction', topic=topic, authority=authority, issue_date=date,
            planned_batch='4', current_status='operative-subject-reviewed-source-limits-disclosed', coverage_status='covered-in-batch-4',
            video_card=pointer, source=SOURCES[source]['url'], review_note='Subject-specific coverage only, not entire parent instrument. Non-government original-document reproductions C07/P18/P20 explicitly distinguished from government-hosted current corroboration.')
        result = [row for row in result if row['id'] != ident] + [replacement]
    with path.open('w', newline='') as f:
        writer = csv.DictWriter(f, fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(result)


def main():
    cards, scripts = content()
    documents(cards)
    # Register updated after successful media QA only; this script prepares content, not proof of coverage.
    print('Prepared', len(cards), 'cards;', len(scripts), 'clips:', [len(s['text']) for s in scripts])


if __name__ == '__main__':
    main()
