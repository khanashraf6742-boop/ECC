# Batch 1 subtitle and audio check

## What is supplied

- The approximately **19-minute, 3-second** TA-focused lecture has **312 audio-aligned cues** across 21 chapters and 42 illustrated teaching screens.
- Roman-script Hinglish is burned into the MP4. `Captions-roman.vtt` is a separate transliteration of the speech-synthesis input. It is not a human-certified verbatim transcript.
- `Captions-en.vtt` is an English **translation**, not a verbatim transcript. The companion HTML offers it as an optional track positioned near the top to avoid the burned-in captions; other players may position it differently.
- The selected city-Hinglish voice is used throughout. The new chapter explains the DA-linked first increase and the specified-region transfer-effects exception. LTC comparisons remain in the written guide's separate appendix.

## Automated checking

The multilingual Whisper small model (int8) aligned the synthesis input against the actual narration clips. A separate automatic recognition pass, using a generic Hinglish prompt rather than the lesson text, checked each audio block. The unedited block recognition is in `notes/asr-review.json`; alignment and word timings are in `notes/caption-alignment.json`. The latter is bound to the current script and audio by SHA-256 hashes. English translations are bound to the source-cue segmentation.

All **21 clips** also have a whole-clip automatic recognition pass in `notes/whole-audio-review.json`. Among **2,306 partial exact-word matches**, the median difference between the two automatically estimated word starts is 0.02 seconds and the 99th percentile is 0.37 seconds. The 7.60-second maximum comes from a repeated-word pairing in the hotel clip. The food example's automatic recognition identifies both ₹300 amounts and the ₹600 total. The new clip's recognition identifies the 60%, 25%, ₹62.50, one-third, 6,000 kg and 2,000 kg figures. A cue boundary was adjusted so the spoken phrase “two thousand” stays together.

These numbers are **not a word-error rate, a complete timing audit, or a guarantee**. The exact-word comparison omits unmatched words and can pair repeated words incorrectly. Recognition can mishear, omit or translate speech. Recognition and forced alignment use the same model; neither is a human check. Reproduce the partial comparison with `python3 check_alignment.py`. The local model file had SHA-256 `ca732cb1379efc49417d028465f543d83a39de2c61f3027678de103dc404ce73`.

## Human verification is still needed

**No person has listened through and human-verified the complete recording or its captions.** We cannot certify the wording or timing as verbatim on the basis of automatic methods. `Narration-hi.txt` preserves the exact text supplied to the speech synthesizer; the voice may pronounce it differently or omit/change words. Transliteration and translation can also be wrong.

To perform a real check, open **`Caption-Review.html`** alongside the lecture. A reviewer can play each cue, edit its Roman wording and timing, add notes, and explicitly mark it only after listening. The page saves progress locally when browser storage is available and exports a review JSON bound to the current MP4 and VTT hashes. Export the JSON as a backup and return it for the corrections to be incorporated into a newly rendered video. The exported VTT is a **draft**: it does not alter the burned-in captions or the separate English translation. A completed review is a reviewer's assertion, not an automated certification.

The detailed, source-linked written explanation and the outstanding legal-coverage ledger are in `Batch-01-Guide.md` and `Batch-01-Guide.html`.
