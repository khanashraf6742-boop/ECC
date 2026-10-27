#!/usr/bin/env python3
"""Regenerate the Batch 3 automatic recognition and audio-alignment evidence.

Requires ``pip install faster-whisper`` plus a locally supplied multilingual
Whisper small CTranslate2 model. This tool never downloads model weights or
calls a speech service. The delivered data were made with an int8 model whose
model.bin SHA-256 is recorded in notes/caption-alignment.json.

The speech is first transcribed without the lesson script as a prompt. The best-effort
caption text is then force-aligned to the audio; the two checks are separate passes
of the *same* model, not independent human verification. The manually selected
block boundaries in notes/caption-plan.json must be updated if audio changes.

Example: python3 align_captions.py --model /path/to/whisper-small-ct2
Use --output-dir for a separate run; --only requires a non-default output dir.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import textwrap
from pathlib import Path

from build_batch_03 import HERE, load_data, section_tts_text

PLAN = HERE / 'notes' / 'caption-plan.json'
PROMPT = ('Hinglish mein baat karein, Hindi aur English mix. '
          'Example: hum office ka rule samjhenge aur check karenge.')


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def merge_tokens(tokens, start: float, end: float, offset: float) -> list[dict]:
    """Combine punctuation and model tokens back into whitespace-separated words."""
    words = []
    for token in tokens:
        text = token['word']
        if not text:
            continue
        begin = max(start, min(end, offset + float(token['start'])))
        finish = max(start, min(end, offset + float(token['end'])))
        if text[0].isspace() or not words:
            words.append({'text': text.strip(), 'start': round(begin, 3),
                          'end': round(finish, 3), 'probability': float(token['probability'])})
        else:
            words[-1]['text'] += text
            words[-1]['end'] = round(max(words[-1]['end'], finish), 3)
    return words


def make_cues(section: dict, blocks: list[dict]) -> list[dict]:
    cues = []
    for beat_number, beat in enumerate(section['beats'], 1):
        words = [word for block in blocks if block['beat'] == beat_number for word in block['words']]
        cursor = 0
        for line in beat['lines']:
            parts = textwrap.wrap(line, width=76, break_long_words=False,
                                  break_on_hyphens=False, replace_whitespace=True)
            if len(parts) > 1 and len(parts[-1]) < 22:
                previous, tail = parts[-2].split(), parts[-1].split()
                while len(' '.join(tail)) < 25 and len(previous) > 4:
                    tail.insert(0, previous.pop())
                parts[-2], parts[-1] = ' '.join(previous), ' '.join(tail)
            # Keep a multiword spoken number together. A cue ending in “two”
            # while the next starts “thousand” is misleading during playback.
            number_words = {'one', 'two', 'three', 'four', 'five', 'six', 'seven',
                            'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen',
                            'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen',
                            'nineteen', 'twenty', 'thirty', 'forty', 'fifty', 'sixty',
                            'seventy', 'eighty', 'ninety', 'hundred', 'thousand'}
            for i in range(len(parts) - 1):
                previous, following = parts[i].split(), parts[i + 1].split()
                while (len(previous) > 1 and previous[-1].strip('.,').lower() in number_words
                       and following[0].strip('.,').lower() in number_words):
                    following.insert(0, previous.pop())
                parts[i], parts[i + 1] = ' '.join(previous), ' '.join(following)
            for part in parts:
                count = len(part.split())
                group = words[cursor:cursor + count]
                cursor += count
                if not group or ' '.join(word['text'] for word in group) != part:
                    raise ValueError('Aligned words do not reconstruct the caption text')
                cues.append({'beat': beat_number, 'start': group[0]['start'],
                             'end': group[-1]['end'], 'text': part})
        if cursor != len(words):
            raise ValueError('Unused aligned words remain')
    for first, second in zip(cues, cues[1:]):
        if first['end'] > second['start']:
            boundary = round((first['end'] + second['start']) / 2, 3)
            first['end'], second['start'] = boundary, boundary
    if any(cue['start'] >= cue['end'] for cue in cues):
        raise ValueError('An aligned caption has zero or negative duration')
    if ' '.join(cue['text'] for cue in cues) != section_tts_text(section):
        raise ValueError('Captions do not reconstruct the alignment text')
    return cues


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model', type=Path, required=True, help='Local CTranslate2 Whisper model directory')
    parser.add_argument('--output-dir', type=Path, default=HERE / 'notes')
    parser.add_argument('--threads', type=int, default=2)
    parser.add_argument('--only', type=int, help='Process one 1-based section into a separate output directory')
    args = parser.parse_args()
    if args.only is not None and args.output_dir.resolve() == (HERE / 'notes').resolve():
        parser.error('--only must be combined with a separate --output-dir')
    model_file = args.model / 'model.bin'
    if not model_file.is_file():
        parser.error('A local CTranslate2 model.bin is required; models are not downloaded')
    from faster_whisper import WhisperModel
    from faster_whisper.audio import decode_audio
    from faster_whisper.tokenizer import Tokenizer

    data = load_data()
    plan = json.loads(PLAN.read_text(encoding='utf-8'))
    if len(plan) != len(data['sections']):
        raise ValueError('Caption plan and lesson section counts differ')
    model = WhisperModel(str(args.model), device='cpu', compute_type='int8', cpu_threads=args.threads)
    tokenizer = Tokenizer(model.hf_tokenizer, True, task='transcribe', language='hi')
    align_sections, asr_sections = [], []
    for number, (section, block_plan) in enumerate(zip(data['sections'], plan), 1):
        if args.only is not None and number != args.only:
            continue
        audio_path = HERE / 'audio' / section['audio']
        audio = decode_audio(str(audio_path))
        duration = len(audio) / 16000
        if abs(block_plan[0][3]) > 0.001 or abs(block_plan[-1][4] - duration) > .05:
            raise ValueError(f'Section {number}: update the plan to match the current audio duration')
        blocks, checks = [], []
        for beat, lo, hi, start, end in block_plan:
            if not (0 <= start < end <= duration + .05 and end - start < 29.7):
                raise ValueError(f'Section {number}: invalid block: {start}-{end}')
            source = ' '.join(section['beats'][beat - 1]['lines'][lo:hi])
            tokens = tokenizer.encode(' ' + source)
            if len(tokens) >= 440:
                raise ValueError(f'Section {number}: alignment block has too many text tokens')
            left, right = max(0, start - .15), min(duration, end + .15)
            chunk = audio[round(left * 16000):round(right * 16000)]
            features = model.feature_extractor(chunk)[..., :-1]
            aligned = model.find_alignment(tokenizer, [tokens], model.encode(features),
                                           round(len(chunk) / 160))[0]
            if ''.join(word['word'] for word in aligned).strip() != source:
                raise ValueError(f'Section {number}: model tokenizer changed the input text')
            words = merge_tokens(aligned, start, end, left)
            if ' '.join(word['text'] for word in words) != source:
                raise ValueError(f'Section {number}: aligned word grouping failed')
            blocks.append({'beat': beat, 'line_start': lo, 'line_end': hi,
                           'start': start, 'end': end, 'words': words})

            # A separate recognition pass; the known lesson text is not used as a prompt.
            speech = audio[round(start * 16000):round(end * 16000)]
            segments, _ = model.transcribe(speech, language='en', beam_size=3,
                                           word_timestamps=True, condition_on_previous_text=True,
                                           vad_filter=False, temperature=0.0, initial_prompt=PROMPT)
            checked = [{'start': round(start + segment.start, 3),
                        'end': round(start + segment.end, 3), 'text': segment.text}
                       for segment in segments]
            checks.append({'beat': beat, 'start': start, 'end': end, 'segments': checked})
            print(f'Section {number:02d}, beat {beat}: {start:.2f}-{end:.2f} seconds checked', flush=True)

        for beat in (1, 2):
            recovered = [line for block in blocks if block['beat'] == beat
                         for line in section['beats'][beat - 1]['lines'][block['line_start']:block['line_end']]]
            if recovered != section['beats'][beat - 1]['lines']:
                raise ValueError(f'Section {number}: plan does not cover each line exactly once')
        audio_hash = sha(audio_path)
        align_sections.append({
            'audio': section['audio'], 'audio_sha256': audio_hash, 'duration': duration,
            'beat_boundary': next(block['start'] for block in blocks if block['beat'] == 2),
            'cues': make_cues(section, blocks),
            'script_sha256': hashlib.sha256(section_tts_text(section).encode('utf-8')).hexdigest(),
            'words': [{'beat': block['beat'], **word} for block in blocks for word in block['words']],
        })
        asr_sections.append({'audio': section['audio'], 'audio_sha256': audio_hash, 'blocks': checks})
    if not align_sections:
        raise ValueError('No section selected')
    metadata = {
        'alignment': 'Whisper small multilingual int8 cross-attention forced alignment of TTS text to the audio; cue boundaries derive from word timings.',
        'recognition': 'The same model transcribed each block separately using a generic Hinglish style prompt, without the lesson text as a prompt.',
        'human_review': 'No human listening or verbatim certification has been performed; automatic recognition and alignment can still be wrong.',
        'model_sha256': sha(model_file),
    }
    review = {'disclosure': 'UNEDITED AUTOMATIC RECOGNITION OUTPUT. It is not an authoritative transcript: it can translate, omit, hallucinate, or misspell words.',
              'method': 'Whisper small multilingual int8, language hint en, generic Hinglish style prompt, beam 3; no lesson text as prompt.',
              'sections': asr_sections}
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for filename, payload in [('caption-alignment.json', {'sections': align_sections, 'method': metadata}),
                              ('asr-review.json', review)]:
        target = args.output_dir / filename
        temporary = target.with_suffix('.json.tmp')
        temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        temporary.replace(target)
    print(f'Wrote alignment and ASR review to {args.output_dir}', flush=True)


if __name__ == '__main__':
    main()
