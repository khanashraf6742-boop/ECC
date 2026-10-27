# Batch 3 caption and audio check

**Status: automated review only. No person has listened through the entire lecture and checked every word and cue.** Do not describe this as human-verbatim certified or “perfectly synchronized.” Review the [cue-by-cue player](Caption-Review.html) and export the hash-bound record after listening. The player does not automatically correct the MP4's burned-in captions.

## What was checked

- The ten selected-voice clips were decoded and checked with multilingual Whisper small (CTranslate2 int8) in whole-clip and separate block recognition passes. Neither pass was given the lesson text as a transcription prompt; both used the same model, and both are automated. The full-clip pass uses a generic Hinglish prompt. The timing pass **force-aligns the supplied caption text**; that is not independent proof that the speaker actually said it.
- The checked timing was split into 20 slide beats, with 92 non-overlapping Roman-Hinglish cues and matching English translation cues. Every cue's source text, audio hash, clip duration, timeline and translation binding are checked by the builder. The MP4 burns in Roman text; the optional English VTT is a **translation**, not a transcript.
- Comparison with matching Roman-word tokens in the separate whole-clip pass found **687 partial matches, median 0.020 s, p99 0.360 s, maximum 0.520 s**. These numbers cover only exact-ish matching tokens and can mispair repeated words; they are not error rates for all words, all cues or all listeners. Recognition can omit, normalize numbers, translate, hallucinate or miss a wrong spoken word.
- Recognition evidence and timing are in `notes/whole-audio-review.json`, `notes/asr-review.json`, `notes/caption-alignment.json` and `notes/caption-plan.json`. The model `model.bin` SHA-256 was `ca732cb1379efc49417d028465f543d83a39de2c61f3027678de103dc404ce73`; model weights are not included. `check_alignment.py` reproduces the partial-match calculation.

## Known editorial interventions and cautions

1. **Section 04 tax example:** Both recognition passes suggested that the voice rendered the English number words “ninety six” and “eight hundred ninety six” as Hindi number words. The Roman caption uses the ASR-suggested *chhiyaanve* / *aath sau chhiyaanve* rather than claiming the synthesis input is the spoken transcript. The original synthesis input and the caption basis are both recorded in `Narration-hi.txt`. This is still a hypothesis, not a human confirmation. The worked amount itself is ₹96 tax and ₹896 total on a hypothetical ₹800 + 12% example.
2. **Section 06 local-journey list:** Automated recognition flagged the first spoken percentage as potentially **30**, despite a synthesis input of fifteen. Instead of publishing a potentially misleading spoken list, the whole percentage-list sentence was excised from the clip. The complete **provisional** 15/35/50 list remains on the slide and in the guide. The shortened audio is assembled from the preserved `audio/source-06-original.mp3` by `assemble_section_06.py`, then re-recognized and re-aligned. A person has not checked the edit for audible seams or exact wording.
3. The local-journey list itself is **provisional**: government training corroborates it, but the original 2018 letter was not authenticated. The speaker's ₹350 example and the slide require accounts confirmation before use.
4. **Section 09 deadline wording:** “Due” on the day after a journey means **due for payment**, not that a tour claim must be submitted the next day. The slide, English translation and guide add this clarification; the spoken Roman caption retains the shorter wording. Check the applicable 60-day filing period and count with accounts. The CAG circular cited in the guide explains the due-for-payment date.
5. Abbreviations, dates, numbers, proper names and beat transitions deserve particular attention during human review. The legal audit also remains incomplete; see the guide's coverage ledger.

After any change to an audio clip or script, rebuild the alignment and translation bindings, render a fresh video, and run `build_review.py` to bind a new review player to the new video and VTT. A review checkbox records a reviewer's assertion, not a model-generated certification.

## Delivered file identities

The 1920 × 1080 lecture runs approximately **5 minutes 45 seconds**. These SHA-256 values bind this report to the files that were tested:

| File | SHA-256 |
|---|---|
| `Batch-03-Lecture.mp4` | `fae875e5524effc3accb26e57c59ba722a74cb4cfa44e71a5f2092a0d17dc156` |
| `Batch-03-Audio.mp3` | `528f049f46ca5eed178151bc71ea510ac72e59299e246e6b17e10ef2119a2b63` |
| `Captions-roman.vtt` | `10feae3ebb37f0005a17d97615e8cb2d1292fd6436f27614a79c89b6a28d65ee` |
| `Captions-en.vtt` | `2b1321c9e08166d8a7bc8cdb7851d62f67d6366d8ae4a438e1a080653fb21177` |
| `audio/06-local-journeys.mp3` | `0e655956a7e5e23ca9b64e499d3af0ef30ad8cfdb343cce9b90b0c7abec51a34` |
| `audio/source-06-original.mp3` | `191d5e97628b1ed415a49a45aec5fd86f765657f9c4a2ac202b0f442bef5e027` |
