# CCS Travelling Allowance — batch-wise study series

A learning series for Central Government civilian employees, based on the supplied TA guide and checked against selected Government orders. **Only Batch 1 is available.** This is not yet a comprehensive or certified consolidation of every applicable rule and amendment. Examples are hypothetical; check the applicable orders, sanctions and departmental instructions before making an actual claim.

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

## Planned roadmap

| Batch | Subject | Status |
|---|---|---|
| 01 | Official tour, Daily Allowance, road mileage, booking and claims; transfer overview | Revised edition available; further audit remains |
| 02 | International, sea/river and remaining road entitlements | Selected 2017 classes and 2023 foreign-tour material introduced; full audit pending |
| 03 | Remaining Daily Allowance exceptions, documentation and revisions | Planned; source audit pending |
| 04 | Transfer, family, personal effects and special regions | Introduction in Batch 1; full source audit pending |
| 05 | Retirement, death, re-employment and settlement journeys | Retirement CTG and selected re-employment branches introduced; full audit pending |
| 06 | Training, long halts, disability and other special cases | Planned; source audit pending |
| 07 | Technical resignation, joining time and transfer-TA liability | One specific case introduced; full audit pending |
| 08 | Practice, case studies and final clause-by-clause concordance | Selected 2017 concordance supplied; full audit and final concordance pending |

The roadmap can change as the primary-source audit progresses. The eventual goal is to cover all applicable rules, sub-rules, provisos, exceptions and explanations with practical examples, and identify obsolete, superseded or missing material. That goal **has not yet been achieved**. Batch 1 cites sources researched on 27 October 2026; later orders may affect an actual case.

## Run locally

From `batch-01`, run `python3 serve_course.py` and open `http://localhost:4173/`. The server supports video seeking. The HTML and MP4 can also be opened directly, although browser restrictions on local caption files may vary. The optional renderer (`build_batch_01.py`) and guide generator (`build_guide.py`) document their Python dependencies in their headers; they reuse the included selected-voice clips and cached alignment rather than generating new speech. Run `python3 build_review.py` after a render to bind the human-review page to the new MP4 and Roman VTT. The renderer rejects stale audio, narration, timing or translation-cue data. `align_captions.py` documents how to redo the automated check using a local model and updated timing plan; model weights are not included. Run `python3 -m unittest -v test_course` in `batch-01` for offline content, subtitle, link and video-seeking checks. Font licences are in `batch-01/licenses/`.
