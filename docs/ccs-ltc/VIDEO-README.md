# Batch 1 video — dates, GIDs and Roman-Hinglish captions

**[Download the updated MP4](https://github.com/khanashraf6742-boop/ECC/raw/refs/heads/arena/393900f9-ecc/docs/ccs-ltc/batch-01-video.mp4)** · [GitHub file page](https://github.com/khanashraf6742-boop/ECC/blob/arena/393900f9-ecc/docs/ccs-ltc/batch-01-video.mp4)

**15:46 · 1920 × 1080 · approximately 19.5 MiB · H.264 / AAC stereo · faststart MP4**

## Changes in this edition

- **Important dates at the start:** five narrated chapters covering key historical/legal dates, reference OMs, current regular blocks, conditional carry-forward, outward-journey counting, booking guidance and claim deadlines.
- **Roman-script city-Hinglish subtitles throughout:** 281 acoustically aligned phrase cues. No Devanagari in the caption files or burned-in captions. This is transliteration, not a change to formal English or a new legal translation.
- **Exact GID authorities added:** Rule 7 GIDs (9) and (6), behind the autonomous-deputation and industrial/work-charged notes in Batch 1, with full authority/date, explanation and immediate hypothetical example.
- **Original ten core chapters retained:** their original AAC packet sequence is preserved; six new selected-teacher-voice opening chapters precede them. The old questioner introduction is still the start of the core lesson at 06:11.
- **Full-series GID checklist:** 112 register entries: 40 historical parent annotations, 62 clause records and 10 modern instruction groups. Remaining topic-batch teaching/currentness checks are **pending**, not presented as complete.

## Downloads and companion notes

- [Roman-Hinglish SRT](https://github.com/khanashraf6742-boop/ECC/raw/refs/heads/arena/393900f9-ecc/docs/ccs-ltc/batch-01-video.srt)
- [Roman-Hinglish WebVTT](https://github.com/khanashraf6742-boop/ECC/raw/refs/heads/arena/393900f9-ecc/docs/ccs-ltc/batch-01-video.vtt)
- [Dates, sources, explanations and examples](DATES-AND-GIDS.md)
- [Full-series GID coverage register](gid-coverage-register.csv)

Captions are part of the picture: no CC button is required. Sidecar SRT/VTT files are supplied for reuse; enabling an external caption file while watching this already-captioned video can display duplicate text. Captions target this **945.74-second video**, not the unchanged standalone MP3.

## Chapter index

| Start | Chapter | Cards |
|---|---|---|
| 00:00 | 1. Important dates — Origins and legal cut-offs | D1-01, D1-02, D1-03 |
| 00:58 | 2. Important dates — Entitlement and air booking | D1-04, D1-05, D1-06 |
| 01:59 | 3. Important dates — Recent references and live evidence holds | D1-07, D1-08, D1-09 |
| 02:58 | 4. Important dates — Blocks, carry-forward and outward journey | D1-10, D1-11, D1-12 |
| 04:06 | 5. Important dates — Booking guidance and claim deadlines | D1-13, D1-14, D1-15 |
| 05:11 | 6. GIDs — Exact authorities behind Batch 1 applicability notes | G1-01, G1-02 |
| 06:11 | 7. Batch 1 — The clause-reference edition | Core introduction |
| 06:30 | 8. Scheme name, start date & the entry gate | B1-01, B1-02, B1-03 |
| 07:18 | 9. Who is included? Four legal categories | B1-04, B1-05, B1-06, B1-07 |
| 08:21 | 10. Who is excluded? Clauses (a) to (c) | B1-08, B1-09, B1-10 |
| 09:03 | 11. Who is excluded? Clauses (d) to (g) | B1-11, B1-12, B1-13, B1-14 |
| 10:10 | 12. Rule 2(1) — Service, certificate & hometown | B1-15, B1-16, B1-17, B1-18 |
| 11:24 | 13. Four-year tenure, extension & continuity | B1-19, B1-20, B1-21 |
| 12:34 | 14. Re-employment conditions & Rule 3 scope | B1-22, B1-23, B1-24, B1-25 |
| 13:48 | 15. Separate family travel & applicability notes | B1-26, B1-27, B1-28 |
| 14:58 | 16. Source hierarchy & the final checklist | B1-29, B1-30 |

## Scope and evidence limits

This is still Batch 1, not a completed video of the entire LTC rulebook. The user selected coverage of all applicable non-obsolete GIDs **across the series, batch by batch**. See the coverage register and planned batches in `DATES-AND-GIDS.md`. The opening previews later topics; a short date reminder is not full coverage of that topic or OM.

The 1988 Gazette publication day remains unauthenticated here. A reported 2026–2028 regional-air extension still needs a signed official instrument. Detailed Railway pass-surrender mechanics and later-order reconciliation remain pending. Old instructions are not discarded just for being old; expired one-time windows are not taught as current benefits. All examples are hypotheticals.

The original PDF, HTML reader and standalone MP3 remain the previous editions. `DATES-AND-GIDS.md` is the new opening companion. `narration.json` preserves the original ten-part script; `video-prefix.json` holds the six additions; `video-narration.json` is the full current video script.

## Build and validation

Install `subtitle-requirements.txt` in a virtual environment. Full update build:

```sh
python docs/ccs-ltc/extend_video.py
python docs/ccs-ltc/build_subtitles.py
python -m unittest discover -s docs/ccs-ltc -p 'test_*.py'
```

`extend_video.py` needs the six selected-voice MP3s named by `video-prefix.json` under ignored `video-work/audio/`. It never silently substitutes another speech service. It reads the clean pre-caption video and timing report from Git commit `f7badf15704c978b447c1ae5708d13f9bea47313`. A shallow checkout may first need `git fetch origin f7badf15704c978b447c1ae5708d13f9bea47313`. It renders new slides, measures actual audio durations, concatenates without changing the original AAC packet sequence, and writes sixteen chapter markers. No existing captioned frame is used as the base.

`build_subtitles.py` uses eSpeak NG reference speech only for acoustic alignment; reference speech is not in the delivered soundtrack. Chapter-local MFCC/dynamic-time-warping alignment uses 20 ms feature frames. That is processing granularity, **not a claim of 20 ms timing accuracy**. These are automatic phrase timings, not a certified word-level or complete manual listening audit.

`roman_subtitles.py` applies a reviewed word map only to caption display text. Unknown Hindi words fail rather than being silently guessed or left in Devanagari. Original spoken text remains alongside Roman caption text in the timing report. All English legal terms, dates, years, numbers and punctuation remain unchanged.

`--align-only` creates subtitle files; `--render-only` renders already-approved timings. Input must be clean and the chapter report/script must match. The builder rejects double-captioning of an already-captioned video. Full audio/video decoding and an unchanged AAC hash during the caption pass are checked before replacing the output.

All slides fit above a dedicated 144 px caption band, without covering references/examples. Roman captions use Atkinson Hyperlegible at ASS size 40, at most two lines. Base slide text is layout-checked; representative opening, carry-forward, GID and core frames were inspected. Twenty-two tests pass, covering transcript/transliteration fidelity, absence of Devanagari captions, source/sequence preservation, reading load, formats, chapter bounds, faststart, AAC hash and repeat-render protection. These checks do not certify exhaustive legal verification.

Atkinson Hyperlegible is distributed under `video-fonts/OFL.txt` (Google Fonts: `ofl/atkinsonhyperlegible`). The unused Noto Sans Devanagari font/license is retained for reproducibility of the previous edition, but the current captions use the Latin font.
