#!/usr/bin/env python3
"""Isolated Batch 5 source/document/script builder. Run before selected-voice synthesis."""
import csv
from html import escape
import json
from pathlib import Path
from batch5_content import DATES, INTRO, ROWS, SOURCES, NOTES
from batch5_tables import TABLES
from batch5_roman import spoken, romanize

ROOT = Path(__file__).resolve().parent
# Explicit boundaries, verified against the speech API character ceiling below.
GROUPS = [(0,7),(7,14),(14,21),(21,28),(28,35),(35,42),(42,49),(49,55)]
TITLES = ['Important legal dates, practical blocks and deadlines',
 'Rule 8: frequency, normal choices and annual option',
 'Annual trade-off; Rule 9 separate groups and outward dates',
 'Rule 11 destinations; Rule 10 conditional carry and ledgers',
 'FAQ 13–16: automatic grace, blocks, HQ and Tables 1–2',
 'FAQ 16–20, expired GID and the fresh-recruit pattern',
 'FAQ 65–68: service clocks, election, annual lapse and transition exception',
 'FAQ 68–70 and the complete Table 3 calendar',
 'Tables 4–5: every year, footnotes and future-rule qualification']


def dump(name,value):
    (ROOT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def content():
    keys=('ref','title','spoken_ref_roman','rule','explanation_roman','example_roman','trap','source')
    cards=[dict(zip(keys,row),id=f'B5-{i:02}') for i,row in enumerate(ROWS,1)]
    scripts=[dict(file='b5-01.mp3',voice='voice-01',title=TITLES[0],units=[],text=spoken(INTRO),roman_text=INTRO)]
    for number,(start,end) in enumerate(GROUPS,2):
        units=[dict(card_id=c['id'],spoken_ref=spoken(c['spoken_ref_roman']),explanation=spoken(c['explanation_roman']),example=spoken(c['example_roman'])) for c in cards[start:end]]
        text=' '.join(' '.join((u['spoken_ref'],u['explanation'],'Example, '+u['example'])) for u in units)
        scripts.append(dict(file=f'b5-{number:02}.mp3',voice='voice-00',title=TITLES[number-1],units=units,text=text,roman_text=romanize(text)))
    if [u['card_id'] for s in scripts for u in s['units']] != [c['id'] for c in cards]:
        raise ValueError('Every clause must occur exactly once in speech')
    if any(len(s['text'])>1500 for s in scripts):
        raise ValueError('Speech budget exceeded: '+str([len(s['text']) for s in scripts]))
    if any(romanize(s['text']) != s['roman_text'] for s in scripts):
        raise ValueError('Speech/caption round-trip differs')
    dump('batch-05.json',dict(title='CCS LTC Batch 5: Types, blocks, carry-over, destinations and fresh recruits',reviewed_on='2026-10-27',master_chapters=[16,17,18],cards=cards,dates=DATES,sources=SOURCES,tables=TABLES,status='Source-reviewed educational restatements; see media/QA reports for measured validation'))
    dump('batch-05-narration.json',scripts)
    return cards,scripts


def documents(cards):
    title='CCS LTC — Batch 5: Types, Blocks, Carry-over & Fresh Recruits'
    md=f'# {title}\n\nReviewed 27 October 2026 · {len(cards)} exact-reference cards · voice-00 teacher / voice-01 questioner.\n\n'
    md+='[Video](batch-05-video.mp4) · [Audio](batch-05-hinglish.mp3) · [PDF](batch-05.pdf) · [Roman subtitles](batch-05-video.srt)\n\n## Important dates first\n\n'
    md+='\n'.join(f'- **{d}:** {t}' for d,t in DATES)+'\n\n## Scope, corrections and evidence limits\n\n'+'\n\n'.join(NOTES)
    html=['<!doctype html><html lang="en-IN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+escape(title)+'</title><style>body{font:18px/1.6 system-ui;background:#0c1424;color:#eaf0fa;max-width:1100px;margin:auto;padding:32px}h1,h2{line-height:1.2}h2,a{color:#7bd9ff}section{padding:24px;margin:24px 0;border:1px solid #40516b;border-radius:14px;background:#142139}table{border-collapse:collapse;width:100%}td,th{border:1px solid #40516b;padding:10px;text-align:left;vertical-align:top}.ref{color:#ffda70}@media print{body,section{color:black;background:white}h2,a,.ref{color:#163955}}</style><main><h1>'+escape(title)+'</h1><p>'+str(len(cards))+' exact-reference cards · Reviewed 27 October 2026</p><p><a href="batch-05-video.mp4">Video</a> · <a href="batch-05-hinglish.mp3">Audio</a> · <a href="batch-05.pdf">PDF</a> · <a href="batch-05-video.srt">Roman subtitles</a></p><h2>Important dates first</h2><ul>']
    html += ['<li><b>'+escape(d)+'</b>: '+escape(t)+'</li>' for d,t in DATES]
    html += ['</ul><h2>Scope, corrections and evidence limits</h2>']+['<p>'+escape(n)+'</p>' for n in NOTES]
    md+='\n\n## All five official FAQ tables — normalized restatements\n\n'
    html+=['<h2>All five official FAQ tables — normalized restatements</h2>']
    for t in TABLES:
        heading=f'Table {t["number"]}: {t["title"]}'
        md+='\n### '+heading+'\n\n'+' | '.join(t['headers'])+'\n'+' | '.join(['---']*len(t['headers']))+'\n'
        md+='\n'.join(' | '.join(r) for r in t['rows'])+'\n\n'+'\n\n'.join(t['notes'])+'\n'
        html+=['<h3>'+escape(heading)+'</h3><table><thead><tr>'+''.join('<th>'+escape(x)+'</th>' for x in t['headers'])+'</tr></thead><tbody>']
        html+=['<tr>'+''.join('<td>'+escape(x)+'</td>' for x in r)+'</tr>' for r in t['rows']]
        html+=['</tbody></table>']+['<p>'+escape(n)+'</p>' for n in t['notes']]
    for c in cards:
        md+=f'\n## {c["id"]} — {c["title"]}\n\n**Exact reference:** {c["ref"]}\n\n'
        html+=['<section id="'+c['id']+'"><h2>'+c['id']+' — '+escape(c['title'])+'</h2><p class="ref">'+escape(c['ref'])+'</p>']
        for label,key in [('Rule / current restatement (not verbatim)','rule'),('Simple city Hinglish','explanation_roman'),('Immediate hypothetical example','example_roman'),('Watch out','trap')]:
            md+=f'**{label}:** {c[key]}\n\n'
            html+=['<p><b>'+escape(label)+':</b> '+escape(c[key])+'</p>']
        md+='**Evidence:** '+'; '.join(f'[{s}]({SOURCES[s]["url"]})' for s in c['source'].split(';'))+'\n'
        html+=['<p>Evidence: '+'; '.join('<a href="'+escape(SOURCES[s]['url'],quote=True)+'">'+s+'</a>' for s in c['source'].split(';'))+'</p></section>']
    md+='\n## Sources and provenance\n\n'
    html+=['<h2>Sources and provenance</h2>']
    for k,s in SOURCES.items():
        md+=f'- **{k}: {s["title"]}** — {s["url"]}\n  {s["use"]}\n\n'
        html+=['<p><b>'+k+': '+escape(s['title'])+'</b><br><a href="'+escape(s['url'],quote=True)+'">'+escape(s['url'])+'</a><br>'+escape(s['use'])+'</p>']
    md+='\n## QA and series status\n\nBatches 1–4 are preserved. Other topics and GIDs remain pending; parent consolidations remain partially covered. See `gid-coverage-register.csv` and `BATCH-05-README.md`. Automatic phrase alignment is not certified word-level timing or a full manual listening audit.\n'
    (ROOT/'batch-05.md').write_text(md)
    (ROOT/'batch-05.html').write_text(''.join(html)+ '</main></html>')
    pdf(cards,title)


def pdf(cards,title):
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Table,TableStyle,KeepTogether
    for name,file in [('Atkinson','Regular'),('AtkinsonBold','Bold')]:
        pdfmetrics.registerFont(TTFont(name,str(ROOT/f'video-fonts/AtkinsonHyperlegible-{file}.ttf')))
    pdfmetrics.registerFontFamily('Atkinson',normal='Atkinson',bold='AtkinsonBold',italic='Atkinson',boldItalic='AtkinsonBold')
    styles=getSampleStyleSheet()
    for name in ('BodyText','Normal','Heading1','Heading2','Title'):
        styles[name].fontName='Atkinson'
        styles[name].leading=styles[name].fontSize*1.35
    styles['BodyText'].fontSize=10.5
    styles['BodyText'].leading=14
    def p(text,style='BodyText'):
        return Paragraph(escape(text),styles[style])
    story=[p(title,'Title'),p('Reviewed 27 October 2026. Educational restatements, not an individual sanction.'),Spacer(1,12),p('Important dates first','Heading1')]
    for d,t in DATES:
        story+=[p(d+' — '+t),Spacer(1,7)]
    story+=[PageBreak(),p('Scope, corrections and evidence limits','Heading1')]
    for note in NOTES:
        story+=[p(note),Spacer(1,8)]
    for t in TABLES:
        story+=[PageBreak(),p(f'Table {t["number"]}: {t["title"]}','Heading1')]
        rows=[[p(cell) for cell in row] for row in [t['headers']]+t['rows']]
        table=Table(rows,colWidths=[180,170,160],repeatRows=1)
        table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),.4,colors.grey),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#d9edf8'))]))
        story+=[table,Spacer(1,12)]
        for note in t['notes']:
            story+=[p(note),Spacer(1,7)]
    story+=[PageBreak()]
    for c in cards:
        story+=[KeepTogether([p(c['id']+' — '+c['title'],'Heading2'),p('Exact reference: '+c['ref'])])]
        for label,key in [('Current restatement','rule'),('Simple city Hinglish','explanation_roman'),('Immediate hypothetical example','example_roman'),('Watch out','trap')]:
            story+=[p(label+': '+c[key]),Spacer(1,5)]
        story+=[p('Evidence: '+c['source']),Spacer(1,16)]
    story+=[PageBreak(),p('Sources and provenance','Heading1')]
    for k,s in SOURCES.items():
        story+=[p(k+': '+s['title'],'Heading2'),p(s['url']),p(s['use']),Spacer(1,10)]
    def footer(canvas,doc):
        canvas.setFont('Atkinson',9)
        canvas.drawString(42,24,'CCS LTC | Batch 5 | reviewed 27 October 2026 | education, not sanction')
        canvas.drawRightString(555,24,str(doc.page))
    SimpleDocTemplate(str(ROOT/'batch-05.pdf'),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=42,bottomMargin=42,title=title,author='LTC learning series',invariant=1).build(story,onFirstPage=footer,onLaterPages=footer)


def register():
    """Append B5 teaching pointers idempotently, preserving prior coverage verbatim."""
    path=ROOT/'gid-coverage-register.csv'
    with path.open(newline='') as f:
        reader=csv.DictReader(f)
        fields,rows=reader.fieldnames,list(reader)
    pointers={'10.1':'B5-34 (EXPIRED audit only)','M-2025-FAQ':'B5-23 through B5-33; B5-35 through B5-55 (FAQ 13–20/64–70 and all five tables only)','M-2025-GUIDE':'B5-01 through B5-55 (Rules 8–11 and fresh-recruit subset only)','M-2022-TECH':'B5-36 (initial-clock reminder only)'}
    result=[]
    for r in rows:
        pointer=pointers.get(r['id'])
        if pointer:
            old=r['video_card'].split('; B5-')[0]
            old='' if old.startswith('B5-') else old
            r={**r,'video_card':(old+'; ' if old else '')+pointer}
        result.append(r)
    additions=[('M-2008-FRESH','Fresh-recruit origin: personal two blocks and one-year gate','31011/4/2008-Estt.(A)','2008-09-23','B5-35 through B5-38','G25'),('M-2014-FRESH','Fresh-recruit FAQ/calendar pattern and normal-option mechanics','31011/7/2013-Estt.(A-IV)','2014-09-26','B5-35 through B5-55','F25'),('M-2015-HQNCR','HQ equals Home Town; Delhi versus other-State NCR','31011/4/2007-Estt.(A-IV)','2015-05-18','B5-02;B5-24;B5-33;B5-46','F25')]
    for ident,topic,authority,date,pointer,source in additions:
        new=dict(id=ident,record_type='modern-instruction',topic=topic,authority=authority,issue_date=date,planned_batch='5',current_status='operative-subject-reviewed-via-current-official-reproduction',coverage_status='covered-in-batch-5',video_card=pointer,source=SOURCES[source]['url'],review_note='Current subject verified in official 2025 guidance; standalone older original not independently retrieved. Not full coverage of unrelated provisions of any parent instrument.')
        result=[r for r in result if r['id']!=ident]+[new]
    with path.open('w',newline='') as f:
        writer=csv.DictWriter(f,fields,lineterminator='\n')
        writer.writeheader()
        writer.writerows(result)


def main():
    cards,scripts=content()
    documents(cards)
    print('Prepared',len(cards),'cards; speech characters:',[len(s['text']) for s in scripts])

if __name__=='__main__':
    main()
