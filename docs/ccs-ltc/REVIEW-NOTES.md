# CCS LTC rebuild — review notes and continuation contract

Review date: **27 October 2026**. This is a batch-wise educational rebuild, not a sanction opinion or a certificate that no later order exists.

## What was supplied and what was reviewed

- `build_pension_rules_batch2_simple_english_video_1.md`: a 1,645-line Python compiler inside Markdown; 29 scenes and 125 cards. Reviewed its scene schema, short/full/narration separation, teacher/student roles, progressive reveal, density guard, reference-sheet export, caption construction, audio generation and ffmpeg pipeline. Its legal claims were **not independently re-certified**. The code was parsed, not executed as an untrusted attachment.
- `Screenshot 2026-10-24 022051.png`: dark navy/purple interface, cyan/amber/teal/purple topic cards, gold active outline/trap strip, progress and media controls. These visual conventions informed the new responsive reader. Its constitutional-law content is unrelated to LTC and was not reused as law.
- `LTC_Master_Guide_FINAL (6).html`: structural inventory covers **14 topic books, 80 numbered chapters and 28 appendices**. Batch 1 substantive review concentrated on Rules 1–3, the associated applicability notes, and the repeated Rule 2 material in chapter 76. The rest is inventoried for subsequent clause-level review, **not declared fully read, verified or complete**.
- No separate CCS Travelling Allowance file was attached. The LTC master contains TA comparisons, but those are not a substitute for that missing reference. Supply the TA file before its requested detailed comparison is represented as completed.

## Chosen format

A **dual-layer, source-led study studio**: a readable complete companion plus one-card focus mode, rather than 4–5 dense text columns squeezed into a video slide. Every teaching card contains:

1. A stable batch/card ID and precise legal reference.
2. A close restatement of the provision, clearly not a verbatim quotation.
3. Roman-script Indian Hinglish explanation, retaining English legal terms.
4. An immediately following practical **hypothetical**, not a purported real decided case.
5. A trap, limitation or exception.
6. The source and verification status.

The final standalone HTML embeds the selected-voice audio. The audio is a **condensed companion**, not a word-for-word reading of the complete written file. It does not provide word-synchronised captions or an MP4. The full narration transcript is included. No browser speech-synthesis fallback silently substitutes a different voice.

Voice selection this session: `voice-00`, masculine teacher; `voice-01`, feminine questioner; language `hi-IN`, Indian Hindi with English code-switching. These IDs identify this session's registrations, not portable public voice names.

## Corrections and holds found so far

| Item | Uploaded guide / risk | Treatment in this rebuild |
|---|---|---|
| Rule 2(1): 2/4-year duration | Multiple passages call this additional future/remaining service after eligibility | Corrected: the period is expressly **reckoned from joining the Central Government post**. The one completed year and certification remain separate conditions. See Batch 1 cards B1-18/B1-19. |
| Contract staff | An analogy suggests only permanent/regular staff receive LTC | Removed. Direct contract appointments are expressly included, subject to applicable conditions. Outsourced/vendor status must not be assumed equivalent. |
| Autonomous deputation | The master infers the Rule 2 certificate solely from temporary-Government-servant treatment | Inference not taught as express law. The official note provides the treatment during deputation; actual category, service conditions and deputation terms require examination. |
| Gazette commencement day | The attachment asserts 21 May 1988 without the original issue being available here | Publication-date trigger checked; exact 1988 publication day and notification identifiers held for original-Gazette authentication. |
| Railway spouse surrender | Chapter 73 says surrender by either one of two Railway spouses suffices; secondary Railway material says both surrender their Privilege Passes | Conflict flagged, not resolved by guessing. General conditional All India window is supported by the official DoPT consolidation; full pass mechanics need original DoPT/Railway instruments and later-change checks. Do not conflate Privilege Passes with all other kinds of passes. |
| Special air dispensation expiry | Uploaded master stops at 25 September 2026 | That old validity period is historical now. A reported 9 September 2026 OM extending through 25 September 2028 was found in secondary results; signed order was **not officially authenticated** in this build. Neither blanket expiry nor confirmed renewal is taught as verified current law. |
| 16 July 2026 Cash Section circular | Potentially presented as a new general statutory amendment | Full official-hosted circular read. It addresses DoPT staff and reiterates earlier planning instructions; distinguish “encouraged/as far as possible” 21-day wording from an automatic forfeiture rule. Detailed treatment remains in the booking batch. |
| Age of an instruction | Risk of discarding an old but still operative instruction | Old does not mean obsolete. Preserve provisions still operative; retire only on a demonstrated amendment, supersession, cancellation, expiry or inapplicable scope. |
| Consolidation label | Risk of calling the 2025 compilation a blanket supersession of every earlier OM | Not assumed. Its paragraph 2 explicitly defers to relevant governing instruments where contradictions/imprecision occur. |

## Evidence policy for every subsequent batch

- Start with the statutory rule and each sub-rule/clause/proviso/explanation/illustration; then layer relevant valid orders and FAQs.
- Primary text first. An official departmental host carrying a DoPT order is useful evidence; preserve the distinction between the forwarding cover date and the enclosed DoPT date.
- Search excerpts and commercial reproductions are **discovery leads**, not silently promoted into officially checked rules.
- Record original issue/effective dates, scope, parent authority, later modification and journey-date applicability. Negative search results do not prove the absence of amendments.
- A consolidation is not a substitute for reading the source of a disputed condition. Statutory authority cannot be casually displaced by an administrative summary.
- Cross-map duplicate explanations so that deduplication does not lose a unique proviso. The 108-row inventory maps every source chapter/appendix to a planned batch.
- Each batch must mark items as checked, corrected, historical/superseded with evidence, pending, or a teaching interpretation. No unqualified “100% no-omission certification”.
- Batch 16 reconciles the gap-closure chapters and appendices. Valid unique items should be inserted into the relevant earlier topic batch too, not left orphaned in an appendix.

## Batch 1 coverage boundary

Drafted: Rule 1(1), 1(2), opening qualification in 1(3), all four clauses 1(3)(i)–(iv), all seven exclusions 1(4)(a)–(g), Rule 2(1)'s category/completed-service/certification/2-year/4-year/joining-date limbs, Rule 2(2), Rule 2(3)'s immediate/no-break condition, continuity consequence, proviso and official illustration; Rule 3; the two applicability notes; paragraph 2 consolidation disclaimer; a limited separate-family-travel cross-reference.

Not claimed complete here: all conditions of the Railway exception; Rule 4 family detail; Rule 7 continuity and FR 17A issues; leave/block/fare/booking/advance/claim rules; original Gazette date; later amendment exhaustiveness. These are explicit future-batch dependencies.

## Sources actually accessed

See the source register inside `batch-01.json`, `batch-01.md` or the HTML Sources tab for direct URLs and evidence limits. All six chunks of the September 2025 guidelines were retrieved and read. Only the indicated portions of the older compilation and July 2025 FAQ were reviewed for Batch 1. Direct DoPT HTML access returned a cookie shell; the circular-view endpoint returned HTTP 500. Those failures are not described as successful direct-site verification.

## Local use

Open `batch-01.html` directly; it is self-contained, including audio, and makes no network calls for scripts, fonts or narration. `batch-01.md` is the full printable text; `batch-01-hinglish.mp3` is the condensed spoken companion. `source-inventory.csv` records the full structural inventory. `narration.json` preserves the spoken script.

Rebuild with `python docs/ccs-ltc/build.py`. Run checks with `python -m unittest discover -s docs/ccs-ltc -p 'test_*.py'`. `build.py` requires only the Python standard library and the already-created audio file. It does not call a TTS service or execute the uploaded pension script.

## Checks performed for this delivery

- Six Python content/build tests pass: all required card fields and examples; clause anchors; complete 80-chapter/28-appendix structural inventory; narration-call limits; joining-date correction and open-date disclosure; generated HTML/Markdown contracts.
- Actual headless Chromium checks pass: reader, filtered and empty search states, single-card navigation, boundary buttons, jump selector, arrow-key navigation, quiz reveal, source and roadmap views, embedded MP3 metadata and playback, no horizontal overflow at 375/768/1440 pixels, complete print visibility, and restoration of open/closed details after printing. No page errors observed.
- Audio metadata: 479.08 seconds, approximately 7 minutes 59 seconds. Synthesised from the two voices selected in this session, concatenated and loudness-normalised. Transcript and script budgets checked; no claim of manual phonetic review of every word.
- `batch-01.pdf` is the browser-print companion, including all 30 teaching cards, source register, quiz answers and roadmap. The audio-panel transcript is available in HTML/Markdown, not included in the PDF.
- Screenshots were inspected for desktop/mobile layout. Automated checks test structure and functionality; they do **not** certify legal completeness or future validity.

## User-requested revision — city Hinglish audio

All eight audio clips have been rewritten and regenerated with the same selected voices. The previous narration has been replaced in the MP3 and embedded standalone HTML. The HTML/Markdown transcript now contains the revised spoken script.

Style: everyday conversational Hindi mixed with English; English legal labels, rule numbers, dates and years. Formal Hindi wording such as “udaharan”, “pravadhan”, “avadhi”, “patrata”, “kijiye” and spelled-out Hindi years has been avoided. For example, narration now uses “Example lo”, “condition check karo”, “joining date se count hoga” and “twenty twenty six”. Legal content, the 30 written teaching cards and their evidence limits remain unchanged. A few spoken explanations were made more explicit rather than translated into formal Hindi.

Revised audio duration: **501.76 seconds (approximately 8 minutes 22 seconds)**. This remains a condensed companion, not a full spoken reading of every written card. The earlier 479.08-second figure above describes the replaced first version, not the current file.

Seven Python content/build checks pass, including the added city-Hinglish vocabulary/script check. The Chromium interaction, embedded-audio playback, responsive-layout and print checks were rerun successfully against the revised file. The PDF has been regenerated; its printed teaching content does not contain the audio transcript. No new current-law verification is claimed for this language-only revision.

## User-requested revision — clause-reference edition

The previous city-Hinglish recording has been replaced with ten newly synthesised clips: one questioner introduction and nine teacher chapters. Current duration: **581.76 seconds (approximately 9 minutes 42 seconds)**. Both earlier duration figures describe superseded recordings.

All **30 cards** have exactly one mapped spoken anchor, followed by an explanation and a hypothetical example. The spoken script now explicitly names Rule 1(1), Rule 1(2), the opening qualification in Rule 1(3), clauses 1(3)(i)–(iv), every exclusion 1(4)(a)–(g), Rule 2(1) and its conditions, Rule 2(2), Rule 2(3), its “provided that” condition/proviso and official illustration, and Rule 3. Roman clause numbers are spoken as “clause Roman one”, etc.; alphabetic clauses are spoken as “clause A”, etc.

Rule 2(1) contains unlettered conditions: labels such as “certification condition” are teaching labels, **not new statutory clause numbers**. Rule 3 has no numbered sub-rules. Rule 4(d), Rules 9/11 and FAQ question 6 remain clearly identified cross-references rather than claimed complete coverage of those provisions. The September 2025 applicability notes, paragraph 2 and the teaching checklist are named separately, not mislabelled as additional clauses of Rules 1–3.

The Rule 1–3 numbering and text, Rule 2(3) condition and illustration, and the supplementary-note locations were rechecked against the official-hosted copies of the 03 September 2025 DoPT guidelines and older Government-hosted rule compilation. This is a numbering/content cross-check, not a fresh certification that no later instrument exists. Existing Gazette-date and detailed Railway-condition holds remain visible in the spoken script.

`spoken-reference-map.csv` provides the 30-row written-card → audio-chapter → spoken-reference index. The same index information appears on each HTML/Markdown card and in the regenerated PDF. Chapter numbers are not word-level synchronisation or precise timestamp claims.

Eight Python tests pass, including a fixed expected-reference list, one-to-one card coverage in order, exact script construction as reference → explanation → example, and checks that Rule 2(1) has not acquired invented clause letters. Generated HTML/Markdown/CSV mappings are checked for consistency. Chromium audio playback, navigation, quiz, search, responsive layouts and complete printing were rerun successfully. These checks do not constitute a guarantee of zero legal or synthesis-pronunciation errors; no manual listening-based transcription audit is claimed.

## Video delivery

`batch-01-video.mp4` adds the requested 1080p video companion. All 30 cards appear as reference/point/hypothetical-example rows across ten audio-timed chapter slides. The same clause-reference script was newly synthesised with the already-selected teacher and questioner voices; the existing standalone MP3 was not changed. Video duration is approximately 9 minutes 34 seconds, versus the earlier MP3's approximately 9 minutes 42 seconds. This is a new take, not a bit-identical reuse of the old MP3.

The video contains short visual summaries, not a word-for-word reading of the full written guide. Slides change at chapter boundaries; no word-synchronised subtitle or active-clause highlighting claim is made. Existing evidence limits remain on screen and in the spoken script. See `VIDEO-README.md` for the chapter index, rebuild prerequisites, font licensing and checks. `video-build-report.json` records actual timings, the narration-script hash and full decode result. Thirteen content/build/video tests pass with the video dependencies installed. AAC stereo audio is present and non-silent; actual MP4 chapter count is ten; faststart metadata precedes media data.


## User-requested revision — synchronized video subtitles

The same `batch-01-video.mp4` now includes **177 burned-in phrase captions**, with separate subtitle files for reuse. The approved `narration.json` text is preserved verbatim apart from whitespace/line breaks. Captions retain everyday Hindi in Devanagari mixed with the original English legal terms, numbers and dates. Separate SRT, VTT and styled ASS files are included. The standalone MP3 remains untouched; captions target the video's original 574.42-second soundtrack.

Timing uses 20 ms MFCC feature frames and dynamic time warping between actual MP4 soundtrack audio and eSpeak NG reference speech, separately within all ten original chapters. Reference speech is for alignment only, not replacement narration. It is automatic phrase-level alignment, not a claim of 20 ms timing accuracy, certified word-level accuracy, or a complete manual listening audit. The original AAC compressed-audio SHA-256 is unchanged. No new law or content verification is implied by this presentation-only update.

The entire slide is fitted into the top 936 px of the 1080p frame; the bottom 144 px is reserved for two-line captions, so none of the slide references, examples or evidence cautions is covered. Noto Sans Devanagari with HarfBuzz shapes Hindi and English. Representative beginning/middle/end frames were inspected. Caption durations range from 0.79 to 5.80 seconds, with at most 84 transcript characters per cue and approximately 22.3 characters/second maximum. Full final video/audio decoding passed, faststart and all ten chapter markers were retained, and eighteen content/build/video/subtitle tests pass. Exact script fidelity and the final AAC stream hash are tested. These checks do not certify legal completeness or perfect synthesis pronunciation.


## User-requested revision — important dates, Roman subtitles, full-series GIDs

User confirmed: (1) GIDs means Government of India's Decisions, (2) all applicable non-obsolete GIDs should be covered across the **full series, batch by batch**, and (3) the opening should include both legal/OM dates and practical blocks/windows/deadlines. Subtitles must be Roman-script Hinglish, without Devanagari.

The revised Batch 1 video is **945.74 seconds (about 15:46)** with sixteen chapters: five narrated date/deadline sections, one exact-applicability-GID section, then the original ten core chapters. Six new teacher clips use the already-selected `voice-00`; the existing questioner/teacher core recording was retained, not resynthesised. The clean pre-caption original was recovered from Git commit f7badf1. Its AAC packet sequence is present unchanged in the extended clean video. Caption rendering copied the extended AAC stream without modification and checked its hash and a full decode. The standalone MP3/PDF/reader are unchanged.

All **281** caption segments are Roman-script city Hinglish. A reviewed deterministic map transliterates Hindi display words while preserving English legal terms/numbers/dates. Unknown Hindi words fail closed. The report preserves both original spoken text and Roman caption text for audit. Subtitles remain phrase-aligned using actual audio/MFCC/DTW; 20 ms frames do not imply 20 ms verified timing accuracy. No complete manual listening audit is claimed. Representative final opening/GID/carry-forward/core frames were inspected; captions are in a separate band and do not cover slide text. Caption duration range: 0.79–6.30 s; maximum 88 Roman characters/cue and approximately 26.5 characters/s. Twenty-two tests pass.

The exact MHA authorities behind the applicability notes were recovered from the Government-hosted compilation: **Rule 7 GID (9), letter 43/6/59-Ests.(A), 24 July 1959**, and **Rule 7 GID (6), OM 6/7/59-Ests.(A), 15 June 1960**. The video identifies their actual Rule 7 GID location as a cross-reference, not invented Rule 1 subclauses. Both are followed by explanations and hypothetical examples. Their substantive treatment is reaffirmed by the 2025 applicability notes.

This turn read all ten returned chunks of the Government-hosted older compilation and all six chunks of the direct DoPT 1 July 2025 FAQ, plus the full 16 July 2026 departmental Cash circular and the returned official MSME enclosure of the 29 August 2022 booking OM. Refresh of the prior CSIR September 2025 consolidation failed; a secondary reproduction's opening chunk was compared and labelled as such. No original Gazette day or signed 2026 special-air renewal was authenticated. Those holds remain audible and visible; reported dates are not promoted into verified facts. Rule 9 outward commencement, Rule 10 conditional carry-forward, normal versus FA-concurrence delayed-claim limits, fresh-recruit annual occasions, and advisory versus mandatory wording are expressly distinguished.

**Full-series work is not complete.** `gid-coverage-register.csv` contains 40 historical parent annotations, 62 child-clause checks and 10 modern instruction groups, with source, date, planned batch, currentness and teaching status. The modern list is not a certified exhaustive later-OM inventory. Expired 2005 grace and 2004 two-year special-air windows are retained for audit but excluded as currently open benefits. Mixed annotations (pay tables, national-carrier restrictions, spouse paragraphs, advance windows/percentages) require clause-level reconciliation, not blanket deletion. The remaining applicable GIDs must be taught in their topic batches with exact reference → simple explanation → immediate example → exception/caution. See `DATES-AND-GIDS.md`; no claim that every non-obsolete GID is already explained in this one video is made.
