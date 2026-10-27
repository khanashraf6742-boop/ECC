# Batch 03 — Daily Allowance Exceptions, Documentation and Deadlines

A practical companion for Central Government civilian **official** travel, with selected source checks as of 27 October 2026. This is an educational resource, not a sanction, and is not a complete legal consolidation. Examples are hypothetical.

## Start here

- [Illustrated course player and detailed guide](Batch-03-Guide.html)
- [Lecture video — MP4](Batch-03-Lecture.mp4) · [Audio — MP3](Batch-03-Audio.mp3)
- [Written guide and coverage ledger — Markdown](Batch-03-Guide.md)
- [Roman-Hinglish captions](Captions-roman.vtt) · [English translation](Captions-en.vtt) · [Narration / edit record](Narration-hi.txt)
- [Human caption-review player](Caption-Review.html) · [Automated checks and limitations](Caption-Check.md)

The lecture has 10 sections and 20 example-bearing screens in the user's selected city-Hinglish voice. The companion contains 50 example-bearing units, source links and a coverage ledger. The video is a shorter orientation than the guide.

## Corrections and open issues

- **Earlier train-order omission:** The original Batch 1 and 2 materials omitted DoE's 30 August 2023 order on Vande Bharat and Humsafar; the written guides and this batch now identify it. The earlier videos have **not** been re-rendered and still omit it. It concerns official TA, not LTC.
- **Local journey:** Government training supports a 15/35/50% local-food interpretation but the original 2018 letter was not authenticated. It is provisional, not a verified universal entitlement. An ASR warning led to removal of the percentage-list sentence from section 06; the full provisional list remains visible on the slide and in the guide. The original audio and a reproducible edit are included.
- **Advance versus claim:** The older advances compendium and a 2021 CAG office circular identify a 15-day tour-advance adjustment, distinct from the claim deadline. Later amendments and department-specific adoption are not exhaustively verified. The 2026 GFR compilation was located, but the available extraction did not reach Rule 290; filing periods rely on the directly read 2018 and 2021 DoE OMs, and the CAG circular corroborates the next-day due-for-payment date. That date is not the next-day filing deadline.
- **Not human-verified:** Automatic speech recognition and alignment do not establish verbatim speech or exact caption timing. For one tax example, recognition suggested Hindi number words different from the English number words supplied to synthesis; the caption uses that best-effort hypothesis, not a certified transcript. A complete human review has not been done. Review [Caption-Check.md](Caption-Check.md) and use the [review player](Caption-Review.html).
- Further source/coverage work remains for long halts, partial meals, station transfers, service-specific rules and other FR/SR decisions. Do not use this as proof of complete currency or coverage.

## Serve or rebuild

From this folder run `python3 serve_course.py 4177`. The range-capable server serves the series root for seeking and cross-batch navigation. For a live remote preview bind to `0.0.0.0` (the provided server does so). Install Pillow, Markdown and imageio-ffmpeg, or supply an FFmpeg with libass via `FFMPEG_BIN`:

```sh
python3 build_guide.py
python3 build_batch_03.py --audit
python3 build_batch_03.py --build
python3 build_review.py
python3 check_alignment.py
python3 -m unittest -v test_course
```

The renderer uses the included audio and cached timing; it checks script/audio/translation hashes. `assemble_section_06.py` reproduces the edit from `audio/source-06-original.mp3`; modifying audio requires new alignment and review. `align_captions.py` documents optional local faster-whisper processing (model weights are not included). Automatic tests cannot establish legal completeness or human-verbatim accuracy. Fonts and visual provenance are in `licenses/` and `assets/README.md`.
