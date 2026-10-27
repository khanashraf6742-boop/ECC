# CCS LTC — Batch 2: family, dependency and definitions

**Review date: 27 October 2026.** Master-guide chapters **4–8**. This is a new Batch 2 delivery; the previously delivered Batch 1 media and written editions are unchanged.

## GitHub downloads

- [1080p video — approximately 13 minutes 20 seconds](https://github.com/khanashraf6742-boop/ECC/raw/refs/heads/arena/393900f9-ecc/docs/ccs-ltc/batch-02-video.mp4)
- [City-Hinglish audio, MP3](https://github.com/khanashraf6742-boop/ECC/raw/refs/heads/arena/393900f9-ecc/docs/ccs-ltc/batch-02-hinglish.mp3)
- [Written companion, PDF](https://github.com/khanashraf6742-boop/ECC/raw/refs/heads/arena/393900f9-ecc/docs/ccs-ltc/batch-02.pdf)
- [Roman-Hinglish subtitles, SRT](https://github.com/khanashraf6742-boop/ECC/raw/refs/heads/arena/393900f9-ecc/docs/ccs-ltc/batch-02-video.srt)
- [Written companion, Markdown](batch-02.md)
- [Downloadable offline HTML reader](https://github.com/khanashraf6742-boop/ECC/raw/refs/heads/arena/393900f9-ecc/docs/ccs-ltc/batch-02.html) — download, then open locally; GitHub's source viewer does not execute HTML.
- [Series GID coverage register](gid-coverage-register.csv)

The final delivery message also links an immutable Git commit. Branch links above follow later revisions.

## Teaching format

**46 individually anchored cards:** exact reference → everyday city-Hinglish explanation → immediate hypothetical example. Every card is narrated, not merely present in the PDF. The full written companion adds precise English restatements, a comparative eligibility grid, cross-references, cautions and evidence limits. Restatements are not mislabelled verbatim legal quotations.

- Same selected **voice-00 teacher / voice-01 questioner**. No voice substitution, no background music, no alignment-reference voice in the soundtrack.
- Important legal dates first, then practical regular blocks and the conditional carryover deadline.
- **1920×1080 H.264/AAC MP4**, ten embedded chapters, two dates pages and 46 individually timed teaching pages.
- **243 Roman-script Hinglish captions**, burned into a dedicated 144px band. Matching SRT, VTT and ASS sidecars; no Devanagari in display captions or slides.
- Roman Hinglish is transliteration, not a translation into formal English. Numbers, years, dates and legal terms remain English.

## Clause and GID scope

- Rule 4(a), (b), (c), (e), (f), and **all four limbs of 4(d)**.
- **All three** child-number exceptions in Explanation 1; second-childbirth multiple-birth qualifier; Explanation 2's specific second-wife exception; current Explanation 3 / historical Explanation 4 crosswalk.
- Parents, stepmother and stepfather; spouse exemption; whole dependency/income test, equality at the ceiling and explicitly hypothetical DR arithmetic.
- Rule 4 **GIDs (1), (2)(i), (2)(ii), (2)(vi), (3), (4)**, reconciled with the 2017 family-to-HQ-and-back instruction. Starred/deleted historical clauses are not invented.
- Family **FAQs 1–12 and 74–75**, including private-sector spouse, separate travel, mixed HT/All India options, suspension, under-5 and 5-to-under-12 child fares.
- Rule 7 **GID (5)'s independent-leg principle and all SIX illustrations**: two outward-only cases, four return-only cases. The first illustration is at the end of chapter 8; the other five continue in chapter 9.
- Government-spouse **GID (18)**: the operative 1990 option and self/children duplication conditions, not the superseded pre-decision common-hometown paragraph.
- Study leave **GID (17)(a), (b)(i), (b)(ii)** and an expressly limited overseas-training **GID (20)(iii)** family/anchor comparison. Full training administration remains for Batch 4.

Full Rule 5 hometown acceptance/change, blocks/fresh recruits, fare/booking, claims/advance settlement, encashment and other specialist topics remain in their planned batches. Short reminders here are not full coverage of those topics.

## Important corrections and evidence boundary

Read the opening notes and linked sources in [the companion](batch-02.md):

1. Parents/step-parents and pension-linked dependency are **not newly introduced in 2025**; the family changes originate in the 23 September 2008 instruction. Current substance is confirmed by official 2025 sources. A secondary reproduction corroborates the 2008 origin; the standalone primary 2008 PDF and its effective-date paragraph were not retrieved/authenticated here.
2. The multiple-birth exception is tied to the **second childbirth**.
3. Government spouses residing together have the independent-choice option under the **8 May 1990** decision, not a new 2025 relaxation.
4. A valid All India option may use **hometown** as destination. The 2017 family-to-HQ relief is not a zero HQ-to-HQ reimbursement cap and not unrestricted reimbursement of every other away-family trip.
5. **50% DR is only an arithmetic assumption**, not a claim about the current notified DR rate. Old Rs.1500/Rs.3500 dependency ceilings are not current teaching.
6. In 2026 the regular block is **2026–29**, not the 2025 source document's then-current 2022–25 block. Carryover requires available unused entitlement and Rule 10's applicable HT-second-sub-block condition.
7. The reported September 2026 Special Dispensation extension is **not authenticated in this batch**. A valid current permission is required before using a special air segment.

Relevant governing orders prevail over compilation imprecision. This educational review is not a legal accuracy guarantee or a departmental sanction. No verified later family amendment was identified in the review; that is not a guarantee that no later instrument exists.

## Chapters

| Start | Chapter | Cards |
|---|---|---|
| 00:00 | Important legal dates and practical blocks | Dates opening |
| 00:44 | Rule 4: the five key terms | B2-01–B2-05 |
| 01:52 | Spouse, children and all three numerical exceptions | B2-06–B2-11 |
| 03:24 | Wives, daughters, parents and dependency | B2-12–B2-16 |
| 04:50 | Income arithmetic, siblings, exclusions and marriage | B2-17–B2-21 |
| 06:14 | Operative Rule 4 Task Force clauses and away family | B2-22–B2-26 |
| 07:43 | HT/All India counting, separate travel and private spouse | B2-27–B2-31 |
| 09:00 | Government spouses, suspension and independent-leg facts | B2-32–B2-36 |
| 10:25 | Single-leg illustrations continued: five remaining cases | B2-37–B2-41 |
| 11:52 | Child fares and family during study/training | B2-42–B2-46 |

Times are rounded down to whole seconds. Exact embedded chapter/page boundaries are in `batch-02-video-report.json`.

## Rebuild and QA

```sh
python -m venv .venv
.venv/bin/python -m pip install -r docs/ccs-ltc/batch2-requirements.txt
.venv/bin/python docs/ccs-ltc/build_batch2.py
# Generate the ten clips named in batch-02-narration.json with the selected voices.
# Put them in ignored docs/ccs-ltc/video-work/batch2/audio/.
.venv/bin/python docs/ccs-ltc/build_batch2_video.py
.venv/bin/python -m unittest discover -s docs/ccs-ltc -p 'test_*.py' -v
```

`build_batch2.py` authors only Batch 2 text/script. `build_batch2_video.py` normalizes the actual selected-voice clips, measures their PCM durations, aligns phrase and card boundaries acoustically, renders a new clean video, then burns Roman captions. It never burns over the previously captioned Batch 1 or substitutes eSpeak for selected-voice narration. The final MP4 is replaced only after a successful full decode and AAC-preservation check; the GID register updates after media validation.

`--render-only` can reuse the matching acoustic report and ignored normalized master for layout corrections. A changed script hash is rejected. A fresh checkout needs regenerated clips: intermediates are intentionally not committed.

**Checks:** 33 acceptance/regression tests, including original Batch 1 tests; all 48 layouts rendered with clipping guards; caption word-for-word transcript fidelity and no Devanagari; ten actual embedded MP4 chapters; faststart; unchanged AAC bitstream during the caption pass; full audio/video decode. Rebuild/test execution is statement-coverage measured for the four new content/build modules, with an 80% minimum. Final results are recorded in `batch-02-qa.json`.

Six representative actual MP4 frames were visually inspected: legal dates, practical dates, dependency arithmetic, the 2017 HQ journey, under-5 air travel, and the overseas-training comparison. PDF extraction/layout checks and sample pages are also recorded in QA. These checks are **not a full manual listening audit or certified word-level timing**. The acoustic analysis uses a 20ms grid; this is not a verified 20ms accuracy claim. Caption timings are automatic phrase-level MFCC/DTW alignment.

Fonts: the existing Atkinson Hyperlegible files and SIL Open Font License in `video-fonts/` are reused. Large scratch WAVs, clips and raster frames remain ignored.

## Full-series status

The shared register now has **115 records**: 40 historical parent annotations, 62 separately tracked clauses, and 13 modern instruction groups. These are overlapping parent/child records, **not 115 independent orders**. Batch 2 marks 23 relevant records covered and four records partially covered; it does **not** mark the full FAQ, full consolidation or full training GID complete. Other applicable GIDs remain pending for their topic batches. Further applicable instructions found later must still be added.

Batch 1's written roadmap is a retained historical release snapshot; this README and the current coverage register record Batch 2's completion.
