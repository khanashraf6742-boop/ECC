#!/usr/bin/env python3
"""Build a standalone study reader and Markdown companion. Standard library only."""
import base64
import csv
import html
import json
from pathlib import Path


def esc(value):
    return html.escape(str(value), quote=True)


def source_link(source):
    return f'<a href="{esc(source["url"])}" target="_blank" rel="noopener noreferrer">[{source["citation"]}] {esc(source["label"])}</a>'


def audio_reference_rows(narration):
    """Map each written card to its explicitly spoken anchor, without inventing timing."""
    return [dict(card_id=unit['card_id'], legal_ref=unit['legal_ref'],
                 audio_chapter=chapter, spoken_ref=unit['spoken_ref'])
            for chapter, segment in enumerate(narration, 1)
            for unit in segment['units']]


def render_card(card, sources, audio_refs):
    source = sources[card['source']]
    audio_ref = audio_refs[card['id']]
    spoken = (f'<p class="spoken-anchor"><strong>Spoken reference · audio chapter {audio_ref["audio_chapter"]}:</strong> '
              f'{esc(audio_ref["spoken_ref"])}</p>')
    extra = ' Also compare S2 for Rules 1–3 and S3 for the FAQ cross-references.'
    return f'''<article class="lesson" id="{esc(card['id'])}" tabindex="-1">
      <div class="eyebrow">{esc(card['id'])} <span>•</span> {esc(card['ref'])}</div>
      <h2>{esc(card['title'])}</h2>
      {spoken}
      <div class="provision"><span class="label">THE PROVISION · CLOSE RESTATEMENT</span><p>{esc(card['rule'])}</p></div>
      <div class="explanation"><h3>Simple explanation <small>Plain-language Hinglish</small></h3><p>{esc(card['explanation'])}</p></div>
      <div class="example"><h3>Apply it <small>Realistic hypothetical · not an actual case</small></h3><p>{esc(card['example'])}</p></div>
      <div class="trap"><strong>WATCH THE DISTINCTION</strong><p>{esc(card['trap'])}</p></div>
      <details class="authority"><summary>Authority &amp; verification · {esc(card['status'])}</summary><p>{source_link(source)}</p><p>{esc(card['ref'])}.{extra} Status describes text checked against the listed source, not proof of no later change.</p></details>
    </article>'''


def render_sources(sources):
    return '\n'.join(f'''<article class="source"><span class="eyebrow">{esc(s['id'])} · {esc(s['kind'])}</span>
    <h2>{source_link(s)}</h2><p><strong>Read / checked:</strong> {esc(s['checked'])}</p>
    <p class="caution"><strong>Limits:</strong> {esc(s['limits'])}</p></article>''' for s in sources)


def render_roadmap(batches):
    return '\n'.join(f'''<article class="roadmap-row"><span class="batch-no">{b['number']:02}</span><div>
    <h2>{esc(b['title'])}</h2><p>Uploaded chapters {', '.join(map(str, b['chapters']))}</p>
    <p class="{'checked' if b['number'] == 1 else 'caution'}">{esc(b['status'])}</p></div></article>''' for b in batches)


def markdown(data, narration):
    out = [f'# {data["title"]} — Detailed companion', '', data['subtitle'], '',
           f'**Review date:** {data["review_date"]}. **Language:** English legal anchors + Roman Hinglish explanation.', '',
           '**Scope:** Rules 1–3 and associated applicability notes. This is Batch 1, not completion of the entire master. All examples are invented hypotheticals, not real decided cases. Each explanation is immediately followed by its application example. Provisions are close restatements, not verbatim quotations.', '',
           '**Evidence limit:** Core text was compared with official-hosted DoPT documents. The original Gazette date, detailed Railway pass conditions and exhaustive later-amendment checks remain open. This educational guide is not a final claim-sanction opinion. A separate CCS Travelling Allowance attachment was not supplied.', '',
           '**Key correction:** Rule 2(1)’s two-/four-year period is reckoned from joining the Central Government post, not as additional years remaining after the proposed journey. One completed continuous year and appropriate certification are separate requirements.', '',
           '**Audio:** `batch-01-hinglish.mp3` has been regenerated in conversational city Hinglish: everyday Hindi + English, English dates/numbers and no formal Hindi phrasing. Every mapped card now starts with its spoken legal reference, followed by an explanation and example. It is a condensed two-voice companion, not a word-for-word reading of the written guide. Rule 2(1) topic labels are not invented lettered clauses; supplementary notes and the teaching checklist are labelled separately. The standalone HTML embeds it; transcript below.', '']
    sources = {s['id']: s for s in data['sources']}
    audio_refs = {row['card_id']: row for row in audio_reference_rows(narration)}
    for card in data['cards']:
        s = sources[card['source']]
        audio_ref = audio_refs[card['id']]
        out.extend([f'## {card["id"]} · {card["title"]}', '', f'**Anchor:** {card["ref"]}', '',
                    f'**Spoken reference — audio chapter {audio_ref["audio_chapter"]}:** {audio_ref["spoken_ref"]}', '',
                    '**Provision — close restatement:** ' + card['rule'], '',
                    '**Explanation:** ' + card['explanation'], '',
                    '**Application example:** ' + card['example'], '',
                    '**Trap / limitation:** ' + card['trap'], '',
                    f'**Authority:** [{s["citation"]}]({s["url"]}) · {s["label"]} · {card["ref"]}. Supporting comparison: S2 for Rules 1–3; S3 for FAQ references.', '',
                    f'**Status:** {card["status"]}. This is not an exhaustive no-later-change certification.', ''])
    out += ['## Active recall — with reasoned answers', '']
    for i, q in enumerate(data['quiz'], 1):
        out += [f'### {i}. {q["q"]}', q['a'], '']
    out += ['## Complete batch plan', '', 'Appendices 1–28 are reconciled in Batch 16 and linked back to their substantive topic batches. All later batches remain pending.', '']
    for b in data['batches']:
        out += [f'- **Batch {b["number"]}: {b["title"]}.** Uploaded chapters {", ".join(map(str,b["chapters"]))}. {b["status"]}.']
    out += ['', '## Source register', '']
    for s in data['sources']:
        out += [f'### {s["id"]} · {s["label"]}', f'[{s["citation"]}]({s["url"]})', '', f'**Type:** {s["kind"]}.', f'**Checked:** {s["checked"]}', f'**Limits:** {s["limits"]}', '']
    out += ['## Revised city Hinglish narration transcript', '', 'Selected voices: masculine teacher voice-00; feminine questioner voice-01; hi-IN. No word-level timing is asserted.', '']
    for i, segment in enumerate(narration, 1):
        out += [f'### Audio chapter {i} · {segment["voice"]}', segment['text'], '']
    return '\n'.join(out).rstrip() + '\n'


def build(root, output):
    data = json.loads((root / 'batch-01.json').read_text())
    narration = json.loads((root / 'narration.json').read_text())
    sources = {s['id']: s for s in data['sources']}
    reference_rows = audio_reference_rows(narration)
    audio_refs = {row['card_id']: row for row in reference_rows}
    if [row['card_id'] for row in reference_rows] != [card['id'] for card in data['cards']]:
        raise ValueError('Every card must have exactly one spoken anchor, in written-card order')
    for card in data['cards']:
        if audio_refs[card['id']]['legal_ref'] != card['ref']:
            raise ValueError(f'Written/spoken legal-reference mismatch: {card["id"]}')
    replacements = {
        '@@CARDS@@': '\n'.join(render_card(c, sources, audio_refs) for c in data['cards']),
        '@@SOURCES@@': render_sources(data['sources']),
        '@@ROADMAP@@': render_roadmap(data['batches']),
        '@@QUIZ@@': '\n'.join(f'<details class="question"><summary>{i}. {esc(q["q"])}</summary><p>{esc(q["a"])}</p></details>' for i, q in enumerate(data['quiz'], 1)),
        '@@JUMP@@': '\n'.join(f'<option value="{i}">{esc(c["id"])} · {esc(c["title"])}</option>' for i, c in enumerate(data['cards'])),
        '@@TRANSCRIPT@@': '\n'.join(f'<h3>Audio chapter {i} · {esc(s["voice"])}</h3><p lang="hi">{esc(s["text"])}</p>' for i, s in enumerate(narration, 1)),
        '@@AUDIO@@': base64.b64encode((root / 'batch-01-hinglish.mp3').read_bytes()).decode(),
    }
    template = (root / 'studio-template.html').read_text()
    for token, value in replacements.items():
        template = template.replace(token, value)
    output.mkdir(parents=True, exist_ok=True)
    (output / 'batch-01.html').write_text(template)
    (output / 'batch-01.md').write_text(markdown(data, narration))
    with (output / 'spoken-reference-map.csv').open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=('card_id', 'legal_ref', 'audio_chapter', 'spoken_ref'))
        writer.writeheader()
        writer.writerows(reference_rows)


if __name__ == '__main__':
    base = Path(__file__).resolve().parent
    build(base, base)
    print('Built batch-01.html and batch-01.md')
