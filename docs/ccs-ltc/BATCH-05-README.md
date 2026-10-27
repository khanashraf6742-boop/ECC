# CCS LTC Batch 5 — types, blocks, carry-over and fresh recruits

**Complete multimedia release · reviewed 27 October 2026 · 13:46 · 1920×1080**

## Downloads

- **[Watch/download the actual MP4 video](batch-05-video.mp4)**
- [PDF companion — 24 pages](batch-05.pdf)
- [Selected-voice MP3](batch-05-hinglish.mp3)
- [Roman-Hinglish SRT](batch-05-video.srt) · [VTT](batch-05-video.vtt)
- [Written lessons, tables and sources](batch-05.md) · [HTML reader](batch-05.html)
- [Source/correction audit](batch-05-source-review.md) · [Measured QA evidence](batch-05-qa.json)

## Scope and format

Master chapters **16–18**: Rules **8(a), 8(b) and proviso, 8(c), 9, 10 and proviso, 11**; FAQ **13–20 / 64–70** and **all five tables with explanatory notes**.

All **55 teaching cards** follow **exact spoken reference → everyday city-Hinglish explanation → immediate hypothetical example**. Written English restatements are fuller and expressly not verbatim quotations. All five tables are printed completely, not only summarised. Each has narrated coverage, with the three fresh-recruit calendars explained year by year.

- Selected **voice-00 male teacher / voice-01 female questioner**, unchanged, no reaudition or substituted narrator; no background music.
- Important legal issue dates and practical blocks/deadlines at the start; issue dates are not misrepresented as all-new effective dates.
- **9 embedded chapters**, 55 audio-timed teaching pages plus two opening pages.
- **215 Roman-Hinglish caption cues**, burned into a dedicated 144px bottom band; matching SRT/VTT/ASS sidecars; no Devanagari captions/slides.
- H.264/AAC fast-start MP4, 10 fps for slide teaching; full decode passed; audio stream unchanged by subtitle burning.

## Important corrections included

- Normal HQ-different scheme: **two Home Town OR one Home Town plus one All India**. All India replaces one available Home Town occasion; it is neither compulsory nor a third free trip.
- **Conditional All-India carry:** second-sub-block Home Town must itself be unused/carried where Home Town entitled. Completing a Home Town trip first is not the condition. Normal HQ=Home Town has no nonexistent Home Town prerequisite.
- Outward commencement controls the charged block, including grace; ordinary return/claim conditions still apply. Grace is automatic, normal sanction is not waived.
- Current block **2026–29**; Home Town sub-blocks **2026–27 / 2028–29**. Ordinary previous eligible carry outward deadline **31 December 2026**, not an unconditional All-India right.
- Fresh pattern **HT–HT–HT–AI–HT–HT–HT–AI** after the one-year gate, no annual carry. Initial-service clock does not reset on Government job change.
- Normal-scheme election excludes fresh LTCs in **that four-year block**, not an invented permanent career ban.
- **Table 4 unused-eighth exception:** following 2024–25 sub-block gives HT **or** AI if eighth AI was forgone/not availed. Source typo “2024–45” disclosed and normalized.
- 31 December first-eligibility-day case; same-HQ fresh recruits' fourth/eighth-only rights; Table 3 NIL year; Table 5 eighth in **2033**, normal **2034–37**, assuming unchanged rules.
- Rule 10 GID (1) June 2005 extension is **expired audit history**, never a current concession. Current applicable older instruction subjects are traced to official current guidance, with original-scan retrieval limits disclosed.

## Chapter navigation

Start | Topic | Cards
--- | --- | ---
00:00 | Important legal dates, practical blocks and deadlines | Two date-first pages
00:54 | Rule 8: frequency, normal choices and annual option | B5-01–B5-07
02:21 | Annual trade-off; Rule 9 separate groups and outward dates | B5-08–B5-14
03:40 | Rule 11 destinations; Rule 10 conditional carry and ledgers | B5-15–B5-21
05:13 | FAQ 13–16: automatic grace, blocks, HQ and Tables 1–2 | B5-22–B5-28
07:01 | FAQ 16–20, expired GID and the fresh-recruit pattern | B5-29–B5-35
08:43 | FAQ 65–68: service clocks, election, annual lapse and transition exception | B5-36–B5-42
10:16 | FAQ 68–70 and the complete Table 3 calendar | B5-43–B5-49
12:03 | Tables 4–5: every year, footnotes and future-rule qualification | B5-50–B5-55

## QA and limitations

- **74 tests passed**, including earlier-batch regressions, source/script contracts, every card's layout, PDF text bounds, exact caption/transcript word preservation, actual audio digest, script hashes, fast-start atoms, failure guardrails and idempotent cumulative register rebuilding.
- **96.51% statement / 94.93% combined line-and-branch coverage** across the new text/video builders, Roman mapper and QA evidence helper. This includes running the actual media pipeline; source data are not a legal-coverage metric.
- **12 actual final-video frames visually sampled**: both openings, normal two-HT choice, conditional carry, automatic grace, same-HQ table, NCR, unused-eighth exception and fresh calendars. Main text and caption bands remain separate.
- PDF **pages 1, 5, 6, 7 and 16** visually sampled; all pages' text bounds checked automatically. All 55 card IDs and all five tables found.
- **72 earlier delivery/build/test files** byte-identical to baseline `7774ac7500f0433304215a0f90af04515fbf33db`.
- Cumulative register **122 overlapping records**, not 122 independent OMs. All earlier pointers retained; three scoped modern-instruction groups added. Parent FAQ/consolidation remain partial; later topic/GID batches remain pending.

Caption timing uses chapter-local acoustic MFCC/DTW against Hindi eSpeak NG reference speech. That reference is **not** part of the delivered narrator audio. The 20ms feature grid is **not a certified 20ms accuracy guarantee**. Technical checks and sampled visual review do not constitute a full manual word-by-word listening audit or legal perfection. Tiny-model ASR diagnostics hallucinated repetitive dates and are **inconclusive**, not proof of every spoken word; automatic alignment is not a substitute for that distinction.

Older standalone 2008/2014/2015 originals were not independently retrieved; current official 2025 reproductions/citations support these subjects. The government-hosted DoT file in a 2026 upload folder is a **2025 forwarding circular**, not a 2026 rule amendment. See the source audit for the exact evidence boundary.

## Build and preservation

Use Python 3.11 with `batch5-requirements.txt` in a virtual environment. Run `build_batch5.py` to prepare the documents and nine-clip `batch-05-narration.json`. Generate the listed text in selected voices into ignored `video-work/batch5/audio/`. One initial benign clip request was declined by the speech service; its plain educational wording was revised and successfully generated in the same voice before this build. No declined/absent clip or substitute narrator was used.

Run `build_batch5_video.py`: normalization, fresh acoustic captions, card timing, 1080p encoding and full-decode/audio/chapter checks. Use `--render-only` ONLY for layout changes with unchanged script hash and existing scratch master/plan; changed speech requires fresh alignment. Run `review_batch5.py` after tests for sample extraction and QA evidence. It retains a prior visual-review record only if the final artifact hashes are identical.

Run `python -m unittest discover -s docs/ccs-ltc -p 'test_*.py' -v` from the repository root. Coverage combines the actual video build, test execution and QA helper. Intermediate audio, model diagnostics, review frames and clean video remain ignored. Raw service clips are not versioned; bit-identical synthesis reproduction is not promised. Batch 1–4 builders and deliverables are not regenerated.

Educational hypothetical examples, not individual claim sanction. Verify later orders before an actual claim; future tables assume unchanged rules.
