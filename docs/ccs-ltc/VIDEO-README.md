# Batch 1 video — clause-reference edition

**[Download the MP4 video](https://github.com/khanashraf6742-boop/ECC/raw/refs/heads/arena/393900f9-ecc/docs/ccs-ltc/batch-01-video.mp4)**

**[View the video file on GitHub](https://github.com/khanashraf6742-boop/ECC/blob/arena/393900f9-ecc/docs/ccs-ltc/batch-01-video.mp4)**

Duration: approximately 9 minutes 34 seconds. Resolution: 1920 × 1080. Size: 10.0 MiB. H.264 video, AAC stereo audio, browser-friendly faststart MP4.

## Included

- The approved clause-reference script, newly synthesised using the same selected male teacher and female questioner voices.
- City Hinglish audio: everyday Hindi + English; rule/clause references spoken before explanations and hypothetical examples.
- All 30 written cards mapped in order, with readable on-screen references, short points, examples and cautions.
- Ten embedded chapter markers. Slides change at actual narration-chapter boundaries; they are not word-synchronised captions.
- The original standalone MP3 remains unchanged. The video uses new takes of the same script, so the total duration is slightly different.

## Chapter index

| Start | Chapter | Written cards |
|---|---|---|
| 00:00 | 1. Batch 1 | The clause-reference edition | Introduction |
| 00:18 | 2. Scheme name, start date & the entry gate | B1-01, B1-02, B1-03 |
| 01:07 | 3. Who is included? Four legal categories | B1-04, B1-05, B1-06, B1-07 |
| 02:09 | 4. Who is excluded? Clauses (a) to (c) | B1-08, B1-09, B1-10 |
| 02:51 | 5. Who is excluded? Clauses (d) to (g) | B1-11, B1-12, B1-13, B1-14 |
| 03:59 | 6. Rule 2(1) | Service, certificate & hometown | B1-15, B1-16, B1-17, B1-18 |
| 05:12 | 7. Four-year tenure, extension & continuity | B1-19, B1-20, B1-21 |
| 06:22 | 8. Re-employment conditions & Rule 3 scope | B1-22, B1-23, B1-24, B1-25 |
| 07:36 | 9. Separate family travel & applicability notes | B1-26, B1-27, B1-28 |
| 08:46 | 10. Source hierarchy & the final checklist | B1-29, B1-30 |

## Scope and limitations

This is the narrated summary companion to the detailed Batch 1 PDF and Markdown guide, not a full legal reading or completion of the entire LTC series. Rule 2(1) conditions are not assigned invented clause letters. Guideline notes and FAQ cross-references remain separate from the rules. Exact Gazette publication date, detailed Railway pass conditions and exhaustive later-order checks remain open as described in `REVIEW-NOTES.md`. All application examples are hypotheticals, not claimed real decided cases.

## Build and checks

See `build_video.py`, `video-requirements.txt`, `video-summaries.json`, `narration.json` and `video-build-report.json`. The build needs the separately generated selected-voice clips in ignored `video-work/audio/`; the script does not silently substitute a different TTS service. Rebuilding without those clips requires a new selected-voice synthesis. The report records actual chapter durations and the script hash.

Every chapter slide was layout-checked and rendered at a body-text floor of 26 px. Representative slides were visually inspected. The MP4 passed a full audio/video decode check, actual chapter-table validation and non-silent audio check. Test coverage checks the 30-card sequence and faststart atom order; no claim of a complete manual listening/transcription audit is made.

Atkinson Hyperlegible fonts: Google Fonts repository (`google/fonts`, `ofl/atkinsonhyperlegible`), distributed under the included SIL Open Font License in `video-fonts/OFL.txt`.
