# Batch 02 — caption and audio checks

**Status: automated checks only. No person has listened through the complete lecture or certified its captions as verbatim.** The checks below reduce some mechanical errors; they do not establish that every word was spoken correctly or that every cue is perfectly timed.

## What is included

- The 439.5-second illustrated MP4 has 10 sections, 20 teaching screens and **114 burned-in Roman-Hinglish caption cues**. `Captions-roman.vtt` is a matching optional sidecar. Roman captions transliterate the saved selected-voice synthesis/assembly text; they are not an independent human transcript of the recording.
- `Captions-en.vtt` is a manually written English **translation**, not a verbatim English transcript. Its cues use the same automatically aligned time intervals; the HTML player places this optional track near the top so that it does not normally overlap the burned-in Roman track. Players may render it differently.
- `Narration-hi.txt` records the Devanagari/English synthesis text, while the captions displayed in the video and sidecars are in Roman script. An automated transliteration dictionary is in `notes/roman-hindi.json`.
- The lesson data, audio hashes, manually chosen beat boundaries, aligned words/cues, independent-of-script recognition outputs and translations are in `notes/`. Forced alignment and unprompted recognition are separate passes of the **same** multilingual Whisper small model; they are not independent human verification. Model weights are not distributed.

## What was checked

1. Every audio file was decoded, its hash bound to its section, and the supplied synthesis text was forced-aligned to it. Cue text reconstructs the saved narration text; cues are monotonic, do not overlap and stay within the audio/slide boundary. This proves consistency with the *supplied text*, not that the voice actually spoke all of it.
2. A whole-clip automatic speech-recognition pass was performed without the lesson script as a prompt; a second pass was run for each alignment block. Both are fallible and can omit, merge, mishear, invent or translate words and numbers. Their outputs are saved unedited in `notes/whole-audio-review.json` and `notes/asr-review.json`.
3. A partial exact-word comparison between forced timing and whole-clip recognition found **839** matchable Roman-letter words, with median absolute timing difference **0.02 s**, 99th percentile **0.30 s**, and maximum **3.70 s**. The maximum is a repeated “dollars” word paired with the wrong occurrence in chapter 04. This is not a word-error rate, does not include unmatchable words/numbers, and is not proof that every cue is accurate.
4. An initial automatic pass misrecognised the numeric year in chapter 04 as “2030s”. The first sentence was replaced with the already-generated same-voice sentence from chapter 06, where the year was spoken out as “twenty twenty three”; the original chapter 04 clip is retained as `audio/source-04-original.mp3`. `assemble_section_04.py` documents the edit. The new automated passes recognise “September 2023”; this is still **not** a human listening check.
5. On the complete 04 clip, recognition also merged the overseas schedule as “70–75%” in one pass; the separate block pass recognised “7 days 75%”. Other recognitions merge a Level 6–8 phrase or misspell “13A”. This illustrates model uncertainty, not a determination of which reading the voice actually says. A human should prioritise the class numbers, negations, 2023 date, 7/14/75/50/60 duration slabs, ₹30/₹15 and ₹3,125 examples, and clip joins.
6. The two VTT files use the aligned cue times and contain no Devanagari. The sidecar line-wrapper keeps “T A” and multiword spoken numbers together across line breaks. The video's subtitle band uses its own libass line wrapping. The optional English track is a translation and should not be used as a verbatim transcript.

## Human review remains open

Open [Caption-Review.html](Caption-Review.html) alongside `Batch-02-Lecture.mp4`. For **every cue**, listen, edit the Roman wording/timing if necessary, check the assertion box only after listening, and export the JSON/VTT. The review record is bound to the video and Roman-caption SHA-256 hashes; a checked box is a reviewer's assertion, not independent proof. Importing a record does not change the MP4, and an exported VTT does not update the English track or burned-in subtitles. A corrected video requires rebuilding and rechecking.

## Published file hashes

| File | SHA-256 |
|---|---|
| `Batch-02-Lecture.mp4` | `c9c4c25d25adef5e318cef49f3bf03aa2c036dd9191aa168d1993e9250f638b1` |
| `Batch-02-Audio.mp3` | `755b33b2dfe3f8810769d7207fac4f37634ab18fdfeea71444d1fe248e57a3e8` |
| `Captions-roman.vtt` | `efcdec56b584f4c91d4f8902375243c02357bf370ea31a07f0d6b4181fcf770e` |
| `Captions-en.vtt` | `135319e983aee26f96daeacbaa96d96d3c2261e7d267715edea90c7a202bd65c` |

The lecture and source-linked guide are educational; see the guide's coverage ledger for legal-source gaps and the unresolved foreign Level 2–9 percentage.
