# CCS Travelling Allowance — batch-wise study series

A learning series for Central Government civilian employees, based on the supplied TA guide and checked against selected Government orders. **Batches 1 and 2 are available.** This is not yet a comprehensive or certified consolidation of every applicable rule and amendment. Examples are hypothetical; check the applicable orders, sanctions and departmental instructions before making an actual claim.

## Batch 1 — revised TA-focused edition

- [Open the illustrated course and detailed guide](batch-01/Batch-01-Guide.html)
- [Download the approximately 19-minute city-Hinglish lecture](batch-01/Batch-01-Lecture.mp4)
- [Read the guide in Markdown](batch-01/Batch-01-Guide.md)
- [Download the audio](batch-01/Batch-01-Audio.mp3) · [Read the synthesis input](batch-01/Narration-hi.txt)
- [Download Roman-Hinglish subtitles](batch-01/Captions-roman.vtt) · [Download the English translation](batch-01/Captions-en.vtt)
- [Open the cue-by-cue human review player](batch-01/Caption-Review.html)

The lecture uses the selected voice and contains 42 illustrated, example-bearing teaching screens. Its primary focus is official Travelling Allowance: tour entitlements, air booking, Daily Allowance, hotel/GST, food timing, city travel, road mileage and claims, plus transfer and retirement introductions. The companion has 84 sourced, example-bearing units, corrections, worked cases and a coverage ledger. Selected DoPT LTC FAQs and decisions remain in a clearly separate reference appendix rather than dominating the lecture. Many rules and questions remain for later batches.

**Rates:** Specified 2017 amounts rose by a first 25% when Dearness Allowance reached 50% from 1 January 2024; the published calculations are corroborated by a 2024 Posts implementation order. Dearness Allowance was 60% from 1 January 2026 under the latest DoE order listed when checked on 27 October 2026; that is not a second 50-point trigger. These are not an independently certified consolidation of all 2026 rates. Check applicability, rounding and subsequent orders. The official 2018 hotel-GST order was retrieved directly; check any later amendments and current tax rules.

**Subtitle check:** The MP4 has automatically aligned Roman-Hinglish transliteration of the speech-synthesis input burned in. The optional English track is a translation, not a verbatim transcript. Separate automatic recognition passes checked all clips, but **neither timing nor wording has been human-verified**. Recognition, translation and timing can still be wrong. The review player lets a person listen to every cue and export review notes; it does not change the burned-in video automatically. See [Caption-Check.md](batch-01/Caption-Check.md) for the method and limitations.

## Batch 2 — international, sea and road

- [Open the illustrated course and source-linked guide](batch-02/Batch-02-Guide.html)
- [Download the approximately 7-minute city-Hinglish lecture](batch-02/Batch-02-Lecture.mp4)
- [Read the detailed guide and coverage ledger](batch-02/Batch-02-Guide.md)
- [Download the audio](batch-02/Batch-02-Audio.mp3) · [Read the narration script](batch-02/Narration-hi.txt)
- [Download Roman-Hinglish captions](batch-02/Captions-roman.vtt) · [Download the English translation](batch-02/Captions-en.vtt)
- [Open the cue-by-cue human review player](batch-02/Caption-Review.html)

Batch 2 uses the selected voice and 20 illustrated, example-bearing screens. Its 57-unit guide covers international air class and booking, selected foreign-visit approvals and sponsorship, MEA foreign daily allowance and hotel conditions, sea/river classes, prescribed and fallback road rates, rail-route distinctions, and related special cases. Its coverage ledger identifies source, audio-review and remaining legal-audit gaps.

**Foreign-rate warning:** The 2023 MEA foreign-tour order is the latest relevant one located, not proof that no later instruction exists. Its official-scan extraction and unofficial copies conflict on the Level 2–9 percentage; do not calculate that row without a legible authoritative order and accounts guidance. The 2023 country list must be checked for later amendments and adoption. Both the video and captions use automated timing and recognition: **no complete human-verbatim audio review has been performed**. See [the caption check](batch-02/Caption-Check.md) and review player.

## Planned roadmap

| Batch | Subject | Status |
|---|---|---|
| 01 | Official tour, Daily Allowance, road mileage, booking and claims; transfer overview | Revised edition available; further audit remains |
| 02 | International, sea/river and remaining road entitlements | Batch available; Level 2–9 foreign rate and further source/human review remain open |
| 03 | Remaining Daily Allowance exceptions, documentation and revisions | Planned; source audit pending |
| 04 | Transfer, family, personal effects and special regions | Introduction in Batch 1; full source audit pending |
| 05 | Retirement, death, re-employment and settlement journeys | Retirement CTG and selected re-employment branches introduced; full audit pending |
| 06 | Training, long halts, disability and other special cases | Planned; source audit pending |
| 07 | Technical resignation, joining time and transfer-TA liability | One specific case introduced; full audit pending |
| 08 | Practice, case studies and final clause-by-clause concordance | Selected 2017 concordance supplied; full audit and final concordance pending |

The roadmap can change as the primary-source audit progresses. The eventual goal is to cover all applicable rules, sub-rules, provisos, exceptions and explanations with practical examples, and identify obsolete, superseded or missing material. That goal **has not yet been achieved**. Batches 1 and 2 cite sources researched on 27 October 2026; later orders may affect an actual case.

## Run locally

From `batch-01`, run `python3 serve_course.py` and open `http://localhost:4173/`. The server supports video seeking. The HTML and MP4 can also be opened directly, although browser restrictions on local caption files may vary. The optional renderer (`build_batch_01.py`) and guide generator (`build_guide.py`) document their Python dependencies in their headers; they reuse the included selected-voice clips and cached alignment rather than generating new speech. Run `python3 build_review.py` after a render to bind the human-review page to the new MP4 and Roman VTT. The renderer rejects stale audio, narration, timing or translation-cue data. `align_captions.py` documents how to redo the automated check using a local model and updated timing plan; model weights are not included. Run `python3 -m unittest -v test_course` in `batch-01` for offline content, subtitle, link and video-seeking checks. Font licences are in `batch-01/licenses/`.


For Batch 2, from `batch-02` run `python3 serve_course.py 4175` and open `http://localhost:4175/`. Its range-capable server serves the series directory, so cross-batch links work. Rebuild the HTML with `build_guide.py`, and the media from the included narration and cached alignment with `build_batch_02.py --build`. Re-run `build_review.py` after changing the video or Roman VTT. The chapter 04 clip assembly is documented by `assemble_section_04.py`; regenerating audio requires fresh alignment. Automated checks do not replace a human caption review. Fonts are licensed in `batch-02/licenses/`; the model weights are not included.
