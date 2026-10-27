# CCS Travelling Allowance — batch-wise study series

A learning series for Central Government civilian employees, based on the supplied TA guide and checked against selected Government orders. **Only Batch 1 is available.** This is not yet a comprehensive or certified consolidation of every applicable rule and amendment. Examples are hypothetical; check the applicable orders, sanctions and departmental instructions before making an actual claim.

## Batch 1 — available now

- [Open the illustrated course and detailed guide](batch-01/Batch-01-Guide.html)
- [Download the 15:35 city-Hinglish lecture](batch-01/Batch-01-Lecture.mp4)
- [Read the guide in Markdown](batch-01/Batch-01-Guide.md)
- [Download the audio](batch-01/Batch-01-Audio.mp3) · [Read the synthesis input](batch-01/Narration-hi.txt)
- [Download English subtitles](batch-01/Captions-en.vtt) · [Download Roman-Hinglish subtitles](batch-01/Captions-roman.vtt)

The lecture uses the selected voice in everyday city Hinglish and has 36 example-bearing screens. The companion contains 50 detailed teaching units, source links, practical examples, corrections to the attachment, a worked case and a coverage ledger. Topics include foundations, domestic travel, booking, claim deadlines and selected current official FAQs, Government decisions and later DoE/DoPT orders. The video is shorter than the guide; many rules and questions remain for later batches.

**Subtitle check:** The MP4 has an English translation burned in; it is not a verbatim transcript. The optional Roman-Hinglish file transliterates the saved speech-synthesis input. Both are automatically aligned to the audio, with a separate automatic recognition check, but **neither timing nor wording has been human-verified**. Recognition, translation and timing can still be wrong. See [Caption-Check.md](batch-01/Caption-Check.md) for the method and limits.

## Planned roadmap

| Batch | Subject | Status |
|---|---|---|
| 01 | Foundations, domestic entitlements, booking, claims and selected official updates | Available; further amendment audit remains |
| 02 | International, sea/river and road entitlements | Planned; source audit pending |
| 03 | Tour Daily Allowance, documentation and DA-linked revisions | Planned; source audit pending |
| 04 | Transfer, family, personal effects and special regions | Planned; source audit pending |
| 05 | Retirement, death, re-employment and settlement journeys | Planned; source audit pending |
| 06 | Training, long halts, disability and other special cases | Planned; source audit pending |
| 07 | Technical resignation, joining time and transfer-TA liability | Planned; source audit pending |
| 08 | Practice, case studies and final clause-by-clause concordance | Planned; not built |

The roadmap can change as the primary-source audit progresses. The eventual goal is to cover all applicable rules, sub-rules, provisos, exceptions and explanations with practical examples, and identify obsolete, superseded or missing material. That goal **has not yet been achieved**. Batch 1 cites sources researched on 27 October 2026; later orders may affect an actual case.

## Run locally

From `batch-01`, run `python3 serve_course.py` and open `http://localhost:4173/`. The server supports video seeking. The HTML and MP4 can also be opened directly, although browser restrictions on local caption files may vary. The optional renderer (`build_batch_01.py`) and guide generator (`build_guide.py`) document their Python dependencies in their headers; they reuse the included selected-voice clips and cached alignment rather than generating new speech. The renderer rejects stale audio, narration, timing or translation-cue data. `align_captions.py` documents how to redo the automated check using a local model and updated timing plan; model weights are not included. Run `python3 -m unittest -v test_course` in `batch-01` for offline content, subtitle, link and video-seeking checks. Font licences are in `batch-01/licenses/`.
