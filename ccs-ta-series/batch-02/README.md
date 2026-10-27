# Batch 02 — International Air, Foreign DA, Sea and Road TA

An educational companion to the supplied Travelling Allowance guide for Central Government civilian official travel and training. Examples are hypothetical; the [detailed guide and coverage ledger](Batch-02-Guide.html) identify the applicable-source checks and remaining gaps. Read alongside [Batch 01](../batch-01/Batch-01-Guide.html).

## Start here

- [Illustrated course, player and detailed guide](Batch-02-Guide.html)
- [Lecture video — MP4, 7:19, 1920 × 1080](Batch-02-Lecture.mp4)
- [Audio — MP3](Batch-02-Audio.mp3) · [source-linked guide — Markdown](Batch-02-Guide.md)
- [Roman-Hinglish caption sidecar](Captions-roman.vtt) · [English translation sidecar](Captions-en.vtt) · [synthesis/assembly script](Narration-hi.txt)
- [Human caption-review player](Caption-Review.html) · [automated checks and limitations](Caption-Check.md)

The lecture uses the selected city-Hinglish voice, 10 sections and 20 example-bearing screens. Roman-Hinglish captions are burned in; the HTML player offers an optional English translation. The written guide contains 57 individually sourced example-bearing units and a coverage ledger. It is more detailed than the video.

## Important limitations

- **Foreign DA Levels 2–9:** extraction of the official-hosted 2023 MEA scan reads 75%, but unofficial transcriptions read 79%. No visually verified authoritative page was obtained to resolve this. Do not use either figure to prepare a claim until the competent authority verifies it. The 2023 MEA country list is the latest relevant one located, not a certification that no later revision exists; service-specific adoption dates can differ.
- **Rates and coverage:** 2026 Dearness Allowance and the first 25% escalation are discussed only where the relevant provision supports it; the change to 60% does not automatically mean another increase. Subsequent orders, amendments, historical FR/SR provisos, Government decisions, FAQs, special-service instructions and every country row are not exhaustively audited. The guide identifies other open calculations and source questions.
- **Captions:** automatic alignment and speech recognition were run on all clips, but no human has reviewed all speech and captions. The Roman text is transliteration of synthesis/assembly input, not a certified verbatim transcript; English is a translation. Check [Caption-Check.md](Caption-Check.md) and use the review page if a verbatim audit is required. The chapter 04 opening uses a documented splice of the same selected voice and was automatically rechecked.

## Use or rebuild locally

Run `python3 serve_course.py 4175` from this folder and open `http://localhost:4175/`. The range-capable server serves the series directory and redirects to the Batch 2 guide, allowing video seeking and cross-batch navigation. Static files may also open locally, though browser caption restrictions vary.

The included source, voice clips and timing evidence allow reconstruction without generating new speech. Install Pillow, Markdown and imageio-ffmpeg (or use an available FFmpeg with libass and specify `FFMPEG_BIN`); then run:

```sh
python3 build_guide.py
python3 build_batch_02.py --audit
python3 build_batch_02.py --build
python3 build_review.py
python3 check_alignment.py
python3 -m unittest -v test_course
```

The renderer checks audio/script hashes, aligned cue order and translation bindings before building. `build_review.py` binds the review page to the current MP4 and Roman VTT hashes; rebuild it after either changes. `assemble_section_04.py` explains and can reconstruct the chapter 04 edit, but a rebuild changes the audio and requires fresh alignment and review. `align_captions.py` documents the optional local faster-whisper model workflow; model weights are not included. Automatic tests verify structure, links, source cautions, media hashes, subtitle timing and HTTP range handling, **not** legal completeness or human-verbatim accuracy. Font licences and illustration provenance are in `licenses/` and `assets/README.md`.
