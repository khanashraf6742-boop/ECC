# Batch 1 subtitle and audio check

## What is supplied

- The approximately **18-minute, 11-second** TA-focused lecture has **297 audio-aligned cues** across 20 chapters and 40 illustrated teaching screens.
- Roman-script Hinglish is burned into the MP4. `Captions-roman.vtt` is a separate transliteration of the exact synthesis input. It is not a human-certified verbatim transcript.
- `Captions-en.vtt` is an English **translation**, not a verbatim transcript. The companion HTML offers it as an optional track positioned near the top to avoid the burned-in captions; other players may position it differently.
- The user-selected city-Hinglish voice is used throughout. LTC comparisons remain in the written guide's separate appendix, not the main lecture.

## How timing and audio were checked

The multilingual Whisper small model (int8) aligned the synthesis input against the actual narration clips. A separate automatic recognition pass, using a generic Hinglish prompt rather than the lesson text, checked each audio block. The unedited block recognition is in `notes/asr-review.json`; alignment and word timings are in `notes/caption-alignment.json`. The latter is bound to the current script and audio by SHA-256 hashes. The English translations are additionally bound to their exact source-cue segmentation.

The eight new or replaced TA-focused clips also have a separate whole-clip automatic recognition pass in `notes/whole-audio-review.json`. The food example was re-recorded to say each ₹300 amount separately; the final automatic pass recognises both ₹300 amounts and the ₹600 total. For all eight new clips, an exact-word automatic comparison found **888 matched anchors**, with a median start-time difference of 0.03 seconds and a 99th percentile of 0.40 seconds. The maximum was 7.60 seconds: the matching algorithm paired a repeated “rupees” with the wrong occurrence when the recognizer rendered another as “Rs”. The method and per-clip output are reproducible with `python3 check_alignment.py`.

These are partial automated matches, not an error rate across all words, not independent human verification, and not a guarantee of accurate figures or captions. Both recognition and forced alignment use the same model. The local model file used had SHA-256 `ca732cb1379efc49417d028465f543d83a39de2c61f3027678de103dc404ce73`.

## Important limitation

**No one has listened through and human-verified the complete recording or its captions.** Automated recognition can mishear names, figures, Hindi or English; forced alignment can confidently match words even when they were not spoken. Translation and transliteration can also contain mistakes. Timing and wording may therefore still be wrong. For a genuinely human-verified verbatim transcript, a reviewer must listen to the entire recording and check each cue. `Narration-hi.txt` preserves the exact text supplied to the speech synthesizer; the detailed, source-linked written explanation is in the companion guide.
