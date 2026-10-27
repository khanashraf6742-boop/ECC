#!/usr/bin/env python3
"""Compare automatically aligned words with a separate whole-clip ASR pass.

This is an exploratory check, not a measure of verbatim correctness. It matches
exact Roman-letter word forms with difflib; repeated words may be paired with the
wrong occurrence and numbers may not match at all. The passes use the same model
and neither has been human-verified. Run: python3 check_alignment.py
"""
from __future__ import annotations

import difflib
import json
import re
import statistics
from pathlib import Path

from build_batch_01 import romanize_hinglish

ROOT = Path(__file__).resolve().parent


def clean(text: str) -> str:
    return re.sub(r'[^a-z]', '', text.lower())


def main() -> None:
    notes = ROOT / 'notes'
    alignment = json.loads((notes / 'caption-alignment.json').read_text(encoding='utf-8'))
    whole = json.loads((notes / 'whole-audio-review.json').read_text(encoding='utf-8'))
    dictionary = json.loads((notes / 'roman-hindi.json').read_text(encoding='utf-8'))
    recognition = {entry['audio']: entry for entry in whole['sections']}
    all_differences: list[float] = []
    for chapter in alignment['sections']:
        name = chapter['audio']
        if not name.startswith('ta-') or name not in recognition:
            continue
        target = []
        for word in chapter['words']:
            token = clean(romanize_hinglish(word['text'], dictionary))
            if token:
                target.append((token, word['start']))
        heard = []
        for segment in recognition[name]['segments']:
            for word in segment['words']:
                token = clean(word['text'])
                if token:
                    heard.append((token, word['start']))
        matches = difflib.SequenceMatcher(a=[w[0] for w in target],
                                          b=[w[0] for w in heard], autojunk=False)
        differences = []
        for block in matches.get_matching_blocks():
            for offset in range(block.size):
                differences.append(abs(target[block.a + offset][1] - heard[block.b + offset][1]))
        differences.sort()
        all_differences.extend(differences)
        if differences:
            p99 = differences[min(len(differences) - 1, int(len(differences) * .99))]
            print(f'{name}: {len(differences)} matches; median {statistics.median(differences):.3f}s; '
                  f'p99 {p99:.3f}s; max {differences[-1]:.3f}s')
    if not all_differences:
        raise SystemExit('No comparable cached whole-clip recognition found.')
    all_differences.sort()
    p99 = all_differences[min(len(all_differences) - 1, int(len(all_differences) * .99))]
    print(f'TOTAL: {len(all_differences)} matches; median {statistics.median(all_differences):.3f}s; '
          f'p99 {p99:.3f}s; max {all_differences[-1]:.3f}s')
    print('Matches are a partial automated subset, not a human-verified error rate.')


if __name__ == '__main__':
    main()
