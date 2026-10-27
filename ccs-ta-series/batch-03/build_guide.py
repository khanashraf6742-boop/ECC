#!/usr/bin/env python3
"""Render the accessible local HTML companion from Batch-03-Guide.md.

Requires the small Python Markdown package: python3 -m pip install markdown.
The result has no network dependencies except optional links to government
sources. Keep the lecture, audio, narration script and captions next to the HTML file.
"""
from pathlib import Path
import json
import markdown

ROOT = Path(__file__).resolve().parent
source = (ROOT / 'Batch-03-Guide.md').read_text(encoding='utf-8')
body = markdown.markdown(source, extensions=['tables', 'toc', 'sane_lists'])
lesson = json.loads((ROOT / 'notes' / 'lesson-data.json').read_text(encoding='utf-8'))
beats = sum(len(section['beats']) for section in lesson['sections'])
page = r'''<!doctype html>
<html lang="en-IN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="dark light">
  <title>CCS Travelling Allowance — Batch 03</title>
  <style>
    :root { color-scheme: dark; --ink:#edf4ff; --muted:#b7c8dc; --bg:#070d1b;
      --panel:#101b30; --line:#2a3a58; --teal:#45e0bd; --gold:#ffd56a; --violet:#c493ff; }
    * { box-sizing: border-box; }
    html { scroll-behavior:smooth; }
    body { margin:0; background:var(--bg); color:var(--ink); font:17px/1.7 system-ui,-apple-system,Segoe UI,sans-serif; }
    a { color:#7edbff; text-underline-offset:3px; }
    a:hover { color:#b1edff; }
    a:focus-visible, video:focus-visible { outline:3px solid var(--gold); outline-offset:4px; }
    .skip { position:absolute; left:-10000px; }
    .skip:focus { left:1rem; top:1rem; z-index:5; background:#fff; color:#111; padding:.6rem; }
    header { border-bottom:1px solid var(--line); background:linear-gradient(90deg,#0a1428 0%,rgba(10,20,40,.97) 47%,rgba(10,20,40,.28) 100%), url('assets/claim-illustration.png') right center / cover no-repeat #0a1428; }
    .shell { width:min(1120px, calc(100% - 36px)); margin:0 auto; }
    .topline { display:flex; flex-wrap:wrap; gap:1rem; align-items:center; justify-content:space-between;
      padding:1rem 0; font-size:.78rem; letter-spacing:.11em; font-weight:700; text-transform:uppercase; color:var(--muted); }
    .badge { color:var(--violet); border:1px solid #9256c9; border-radius:999px; padding:.25rem .7rem; }
    .hero { padding:2.2rem 0 2.8rem; max-width:690px; }
    .hero h1 { font-size:clamp(2.1rem,5vw,3.8rem); line-height:1.08; letter-spacing:-.04em; margin:.6rem 0 1rem; }
    .hero p { color:var(--muted); max-width:70ch; margin:0; }
    .chips { display:flex; flex-wrap:wrap; gap:.65rem; margin-top:1.3rem; }
    .chip { border:1px solid var(--line); background:#101e32; color:#d5e9fa; border-radius:8px; padding:.35rem .65rem; font-size:.83rem; }
    main { padding:2rem 0 4rem; }
    .player, article { background:var(--panel); border:1px solid var(--line); border-radius:18px; }
    .player { overflow:hidden; margin-bottom:1.5rem; }
    .player-heading { padding:1.15rem 1.5rem .4rem; display:flex; flex-wrap:wrap; gap:1rem; justify-content:space-between; align-items:center; }
    .player-heading h2 { margin:0; font-size:1.15rem; }
    .player-heading span { color:var(--teal); font-size:.8rem; font-weight:700; }
    video { display:block; background:#000; width:100%; aspect-ratio:16/9; }
    @media (min-width:768px) { video::cue { font-size:75%; } }
    .player p { color:var(--muted); font-size:.89rem; margin:0; padding:1rem 1.5rem 1.25rem; }
    article { padding:clamp(1.2rem,4vw,3rem); }
    article h1, article h2, article h3 { color:#f8fbff; line-height:1.25; scroll-margin-top:1rem; }
    article h1 { font-size:2rem; margin:0 0 .6rem; }
    article h2 { font-size:1.55rem; margin:2.7rem 0 1rem; padding-bottom:.55rem; border-bottom:1px solid var(--line); }
    article h3 { font-size:1.15rem; margin:2rem 0 .6rem; color:#e5d3ff; }
    article { overflow-wrap:anywhere; }
    article p { margin:.7rem 0; } article strong { color:#fff; }
    article p:has(strong:first-child) { padding:.25rem 0; }
    article h3 + p strong:first-child { color:var(--teal); }
    article table { width:100%; border-collapse:collapse; display:block; overflow-x:auto; margin:1.2rem 0 1.6rem; }
    article th, article td { border:1px solid #344767; padding:.7rem .8rem; text-align:left; vertical-align:top; }
    article th { background:#172942; color:var(--teal); }
    article tr:nth-child(even) td { background:#122037; }
    article hr { border:0; height:1px; background:var(--line); margin:2.3rem 0; }
    article li { margin:.35rem 0; }
    footer { border-top:1px solid var(--line); padding:1.5rem 0 3rem; color:var(--muted); font-size:.88rem; }
    @media (prefers-reduced-motion:reduce) { html { scroll-behavior:auto; } }
    @media print { :root { color-scheme:light; } body { color:#111; background:#fff; }
      header,.player,footer { display:none; } main { padding:0; } article { color:#111; border:0; padding:0; background:#fff; }
      article h1,article h2,article h3,article strong,article h3 + p strong:first-child { color:#111; }
      article a { color:#134e7b; } article tr:nth-child(even) td,article th { background:#eee; color:#111; }
    }
  </style>
</head>
<body>
<a href="#guide" class="skip">Skip to the companion guide</a>
<header><div class="shell">
  <div class="topline"><span class="badge">Batch 03 / Study series</span><span>Central Government civilian context</span><span>Research: 27 Oct 2026</span></div>
  <div class="hero"><span style="color:var(--teal);font-weight:700;letter-spacing:.1em;font-size:.8rem">TRAVEL. RULES. REAL-LIFE APPLICATION.</span>
    <h1>Daily Allowance,<br>claims &amp; exceptions.</h1>
    <p>Domestic DA exceptions, documentation, deadlines and revision checks — explained in city Hinglish with practical examples and links to official sources.</p>
    <div class="chips"><span class="chip">__BEATS__ illustrated teaching beats</span><span class="chip">Source-linked guide</span><span class="chip">City-Hinglish narration</span><span class="chip">2018 local-journey letter: verify</span></div>
  </div>
</div></header>
<main class="shell">
  <section class="player" aria-labelledby="watch-title">
    <div class="player-heading"><h2 id="watch-title">Watch the Batch 3 lecture</h2><span>CITY HINGLISH · AUDIO-ALIGNED CAPTIONS</span></div>
    <video controls preload="metadata" aria-label="Batch 3 narrated Travelling Allowance lecture">
      <source src="Batch-03-Lecture.mp4" type="video/mp4">
      <track src="Captions-en.vtt" kind="subtitles" srclang="en" label="English translation (automatic, optional)">
      Your browser cannot play this video. <a href="Batch-03-Lecture.mp4">Download the MP4</a> or read the detailed guide below.
    </video>
    <p><strong>Subtitle check:</strong> The video has burned-in Roman-Hinglish, transliterated from the caption-alignment text. The optional English translation appears near the top to avoid the burned-in captions; placement may vary by player. Both tracks are automatically audio-aligned, and a separate automatic recognition pass checked the recording. Neither wording nor timing has been human-verified as verbatim. <a href="Caption-Check.md">How the check was done</a> · <a href="Caption-Review.html">Human cue-by-cue review</a> · <a href="Narration-hi.txt">Read narration script</a> · <a href="Captions-en.vtt">English subtitles</a> · <a href="Captions-roman.vtt">Roman-Hinglish subtitles</a> · <a href="Batch-03-Audio.mp3">Download audio</a> · <a href="Batch-03-Lecture.mp4">Download video</a></p>
  </section>
  <article id="guide" tabindex="-1">__BODY__</article>
</main>
<footer><div class="shell">Batch 03 is an educational resource, not a sanction. Check the latest applicable orders and your controlling/accounts authority before making a claim.</div></footer>
</body>
</html>'''
(ROOT / 'Batch-03-Guide.html').write_text(page.replace('__BEATS__', str(beats)).replace('__BODY__', body), encoding='utf-8')
print('Created Batch-03-Guide.html')
