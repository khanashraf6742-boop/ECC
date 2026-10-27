# Batch 1 subtitle and audio check

## What is supplied

- The 15:35 lecture has **256 audio-aligned cues**. The English translation is burned into the MP4, so it is visible without a separate file.
- `Captions-en.vtt` is the same English translation as a separate subtitle file. It is a **translation**, not a verbatim transcript of the Hinglish narration.
- `Captions-roman.vtt` transliterates the saved Hinglish synthesis input into Roman script. The companion HTML offers it as an optional track positioned near the top, separate from the burned-in English; other players may position it differently. The Roman text is not a human-certified verbatim transcript.
- The user-selected city-Hinglish voice is used throughout. The expanded lecture includes the later DoPT ordinary-LTC agent exception; special dispensations have different conditions.

## How timing and audio were checked

The multilingual Whisper small model (int8) was used to align the synthesis input against the actual narration clips. A separate automatic recognition pass, using a generic Hinglish prompt rather than the lesson text, was compared with the audio. The resulting unedited block recognition is in `notes/asr-review.json`, and the alignment and word timings are in `notes/caption-alignment.json`. The latter is bound to the current script and audio by SHA-256 hashes. English translations are additionally bound to their exact source-cue segmentation.

For the eight new clips from the boarding-pass chapter through the closing chapter, an additional whole-clip recognition pass (`notes/whole-audio-review.json`) yielded 873 matching word anchors: median alignment/recognition start-time difference 0.02 seconds, 99th percentile 0.36 seconds and maximum 0.57 seconds. This is only a cross-check on words both automatic passes matched, not a measure of all words or proof of correctness. The separately added LTC exception was also checked using automatic recognition. The local model file used had SHA-256 `ca732cb1379efc49417d028465f543d83a39de2c61f3027678de103dc404ce73`.

The dates narration was re-recorded to clarify “new rules” and “new table.” A prior technical-resignation passage was also re-recorded after recognition suggested a mispronunciation; the expanded lecture contains a new technical-resignation chapter. Timing at the later technical-resignation and closing examples was refined using a separate whole-clip recognition pass.

## Important limitation

**No one has listened through and human-verified the complete recording or its captions.** Automated recognition can mishear names, figures, Hindi or English; forced alignment can confidently match words even when they were not spoken. Translation and transliteration can also contain mistakes. Timing and wording may therefore still be wrong. For a genuinely human-verified verbatim transcript, a reviewer must listen to the entire recording and check each cue. `Narration-hi.txt` preserves the exact text supplied to the speech synthesizer; the detailed, source-linked written explanation is in the companion guide.
