#!/usr/bin/env python3
"""Build Batch 3 text, PDF and selected-voice script. No media generation or B1 edits.

Install subtitle-requirements.txt plus reportlab==5.1.0, then run this file.
Generate the nine JSON-listed speech clips with selected voice-01/voice-00;
then run build_batch3_video.py. Intermediate audio stays in ignored video-work/.
"""
import csv
from html import escape
import json
from pathlib import Path

from batch3_content import DATES, INTRO, ROWS, SOURCES, NOTES, GRID
from batch3_roman import romanize, spoken

ROOT = Path(__file__).resolve().parent
GROUPS = [(0, 4), (4, 8), (8, 12), (12, 16), (16, 20), (20, 24), (24, 28), (28, 32)]
TITLES = ['Important dates: law and practical blocks', 'Rules 4(e) and 5: acceptance, finality and change authority',
          'Rule 5: HoD employee, one-change ceiling and normal-residence test',
          'Rule 5 GID (1): all four criteria in legal order',
          'Rule 5 GID (1): sequence, property, permanence and expired transition',
          'Rule 7 GID (4) declaration routes; Rule 6 family scope',
          'Rule 6: advance declaration, pre-start approval and post-start exception',
          'Rules 5-6: competent relaxation, limits and family destinations',
          'FAQs 19-20, source discrepancy and worked approval checklist']


def dump(name, value):
    (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def content():
    cards = [dict(zip(('ref', 'title', 'spoken_ref_roman', 'rule', 'explanation_roman',
                       'example_roman', 'trap', 'source'), row), id=f'B3-{i:02}')
             for i, row in enumerate(ROWS, 1)]
    scripts = [dict(file='b3-01.mp3', voice='voice-01', title=TITLES[0], units=[],
                    text=spoken(INTRO), roman_text=INTRO)]
    for number, (start, end) in enumerate(GROUPS, 2):
        units = [dict(card_id=c['id'], spoken_ref=spoken(c['spoken_ref_roman']),
                      explanation=spoken(c['explanation_roman']), example=spoken(c['example_roman']))
                 for c in cards[start:end]]
        text = ' '.join(' '.join((u['spoken_ref'], u['explanation'], 'Example, ' + u['example'])) for u in units)
        scripts.append(dict(file=f'b3-{number:02}.mp3', voice='voice-00', title=TITLES[number - 1],
                            units=units, text=text, roman_text=romanize(text)))
    if [u['card_id'] for s in scripts for u in s['units']] != [c['id'] for c in cards]:
        raise ValueError('Every authored clause must be included exactly once in the narration')
    if any(len(s['text']) > 1500 for s in scripts):
        raise ValueError('Speech service character budget exceeded')
    for s in scripts:
        if romanize(s['text']) != s['roman_text']:
            raise ValueError('Speech/caption round-trip differs')
    dump('batch-03.json', dict(title='CCS LTC Batch 3: Rules 5-6, hometown and destination declarations',
         reviewed_on='2026-10-27', master_chapters=[9], sources=SOURCES,
         cards=cards, dates=DATES, status='Authored and source-reviewed; see media reports for build QA'))
    dump('batch-03-narration.json', scripts)
    return cards, scripts


def documents(cards):
    title = 'CCS LTC — Batch 3: Hometown & All-India Destination'
    intro = '\n\n'.join(NOTES)
    md = f'# {title}\n\nReviewed: 27 October 2026. Selected voices: teacher voice-00, questioner voice-01.\n\n'
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
    md += '\n\n## Series status\n\nBatches 1 and 2 delivered unchanged. Batch 3 covers the cards above. Remaining topic batches and their unreviewed GIDs remain pending. See `gid-coverage-register.csv`; see `BATCH-03-README.md` for build and QA details.\n'
    (ROOT / 'batch-03.md').write_text(md)
    css = ('body{font:18px/1.65 system-ui,sans-serif;background:#0c1424;color:#eaf0fa;margin:auto;max-width:1050px;padding:32px}'
           'h1,h2{line-height:1.2}h1{font-size:42px}h2{color:#7bd9ff}a{color:#81e8c0}small{color:#ffd980}'
           'section{background:#142139;border:1px solid #334762;border-radius:16px;margin:24px 0;padding:26px;break-inside:avoid}'
           '.ref{color:#ffda70;font-weight:700}td,th{border:1px solid #40516b;padding:10px;text-align:left}table{border-collapse:collapse;width:100%}'
           '@media print{body{color:black;background:white;padding:0}section{color:black;background:white;border-color:#aaa}h2,a,.ref{color:#163955}}')
    table = '<table><thead><tr>' + ''.join('<th>' + escape(v) + '</th>' for v in ('Question', 'Who acts?', 'Conditions', 'Reference')) + '</tr></thead><tbody>'
    table += ''.join('<tr>' + ''.join('<td>' + escape(v) + '</td>' for v in row) + '</tr>' for row in GRID) + '</tbody></table>'
    html = ('<!doctype html><html lang="en-IN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>' + escape(title) + '</title><style>' + css + '</style><main><h1>' + escape(title) + '</h1>'
            '<p>Reviewed 27 October 2026 · 32 exact-reference cards · Roman city Hinglish</p>'
            '<p><a href="batch-03-video.mp4">Video</a> · <a href="batch-03-hinglish.mp3">Audio</a> · <a href="batch-03.pdf">PDF</a> · <a href="batch-03-video.srt">Subtitles</a></p>'
            '<h2>Important dates first</h2><ul>' + ''.join('<li><b>' + escape(d) + '</b>: ' + escape(t) + '</li>' for d, t in DATES)
            + '</ul><h2>Scope, currentness and corrections</h2>' + ''.join('<p>' + escape(n) + '</p>' for n in NOTES)
            + '<h2>Approval and authority grid</h2>' + table + ''.join(sections)
            + '<h2>Sources and evidence limits</h2>' + ''.join('<p><b>' + k + ': ' + escape(s['title']) + '</b><br><a href="'
              + escape(s['url'], quote=True) + '">' + escape(s['url']) + '</a><br>' + escape(s['use']) + '</p>' for k, s in SOURCES.items())
            + '<p>Remaining LTC topic batches and their GIDs are pending. See the coverage register.</p></main></html>')
    (ROOT / 'batch-03.html').write_text(html)
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
        canvas.drawString(42, 24, 'CCS LTC | Batch 3 | reviewed 27 October 2026 | education, not sanction')
        canvas.drawRightString(555, 24, str(doc.page))
    SimpleDocTemplate(str(ROOT / 'batch-03.pdf'), pagesize=A4, rightMargin=42, leftMargin=42,
                      topMargin=42, bottomMargin=42, title=title, author='LTC learning series').build(story, onFirstPage=footer, onLaterPages=footer)


def register():
    """Record actual B3 media coverage without overwriting older partial pointers."""
    path = ROOT / 'gid-coverage-register.csv'
    with path.open(newline='') as f:
        reader = csv.DictReader(f)
        fields, rows = reader.fieldnames, list(reader)
    covered = {'5.1': 'B3-07 through B3-16', '5.1.i': 'B3-09', '5.1.ii': 'B3-10',
               '5.1.iii': 'B3-11;B3-15', '5.1.iv': 'B3-12', '5.1.note': 'B3-13;B3-14;B3-15',
               '7.4': 'B3-17;B3-18;B3-19'}
    changed = []
    for row in rows:
        ident = row['id']
        if ident in covered:
            row = {**row, 'coverage_status': 'covered-in-batch-3', 'video_card': covered[ident],
                   'current_status': 'mixed-operative-reviewed-expired-transition-excluded' if ident == '5.1' else 'operative-text-reviewed',
                   'review_note': 'Batch 3 exact reference, city-Hinglish explanation and immediate example. All operative limbs taught; 1958 transition excluded as expired. Own-CO communication distinguished from Rule 5 change authorisation.'}
        elif ident == '5.1.transition':
            row = {**row, 'video_card': 'B3-16 (historical explanation only)',
                   'review_note': '31.10.1958 window and 1958-59 block expired; explained to prevent revival, NOT a present concession. Current/coverage exclusion statuses deliberately preserved.'}
        elif ident in ('M-2025-FAQ', 'M-2025-GUIDE'):
            pointer = 'B3-29;B3-30 (FAQ 19-20 only)' if ident == 'M-2025-FAQ' else 'B3-01 through B3-32 (Rules 5-6 subset; Rule 6 discrepancy disclosed)'
            # Idempotent append: never erase Batch 2 evidence or imply whole-instrument completion.
            previous = row['video_card'].split('; B3-')[0]
            row = {**row, 'video_card': previous + '; ' + pointer,
                   'review_note': 'Cumulative partial coverage: Batch 2 family subset and Batch 3 hometown/destination subset. Whole instrument remains incomplete; Rule 6 full text cross-checked and 2025 summary timing discrepancy disclosed.'}
        changed.append(row)
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
