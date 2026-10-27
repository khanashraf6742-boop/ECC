"""Acceptance tests for the dates-first / Roman-Hinglish / GID edition."""
import csv
import json
from pathlib import Path
import re
import unittest

from roman_subtitles import romanize

ROOT = Path(__file__).parent


class UpdatedEditionTests(unittest.TestCase):
    def test_roman_hinglish_is_not_an_english_translation(self):
        self.assertEqual(romanize('Rules की start date है.'), 'Rules ki start date hai.')
        self.assertEqual(romanize('Rule 2(1), 2026-2029: नहीं मिलता.'), 'Rule 2(1), 2026-2029: nahi milta.')
        with self.assertRaisesRegex(ValueError, 'Unreviewed'):
            romanize('असमीक्षित')

    def test_every_caption_is_roman_and_matches_the_spoken_script(self):
        report = json.loads((ROOT / 'subtitle-build-report.json').read_text())
        segments = json.loads((ROOT / 'video-narration.json').read_text())
        self.assertEqual(len(segments), 16)
        for chapter, segment in enumerate(segments, 1):
            cues = [c for c in report['cues'] if c['chapter'] == chapter]
            self.assertEqual(' '.join(c['spoken_text'] for c in cues).split(), segment['text'].split())
            self.assertEqual(' '.join(c['text'] for c in cues).split(), romanize(segment['text']).split())
        for extension in ('srt', 'vtt', 'ass'):
            self.assertIsNone(re.search(r'[\u0900-\u097f]', (ROOT / f'batch-01-video.{extension}').read_text()))

    def test_dates_precede_the_original_video_and_gids_have_examples(self):
        segments = json.loads((ROOT / 'video-narration.json').read_text())
        self.assertTrue(all(s['file'].startswith('update-dates-') for s in segments[:5]))
        self.assertEqual(segments[5]['file'], 'update-gids-01.mp3')
        self.assertEqual(segments[6:], json.loads((ROOT / 'narration.json').read_text()))
        for segment in segments[:6]:
            expected = ' '.join(' '.join((u['spoken_ref'], u['explanation'], 'Example, ' + u['example']))
                                for u in segment['units'])
            self.assertEqual(segment['text'], expected)
            self.assertLessEqual(len(segment['text']), 1500)
        units = [u for s in segments[:6] for u in s['units']]
        self.assertEqual(len(units), 17)
        for unit in units:
            self.assertTrue(all(unit[k] for k in ('legal_ref', 'spoken_ref', 'explanation', 'example', 'source')))
        text = ' '.join(s['text'] for s in segments[:6])
        self.assertIn('outward journey', text)
        self.assertIn('penal interest', text)
        self.assertIn('encouraged', text)
        self.assertIn('authenticate', text)

    def test_full_series_gid_register_is_honest_about_pending_coverage(self):
        with (ROOT / 'gid-coverage-register.csv').open() as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(len([r for r in rows if r['record_type'] == 'historical-parent']), 40)
        self.assertTrue(any(r['current_status'] == 'expired-one-time-window' for r in rows))
        self.assertTrue(any(r['coverage_status'] == 'pending-topic-batch' for r in rows))
        for gid, card in [('7.6', 'G1-02'), ('7.9', 'G1-01')]:
            row = next(r for r in rows if r['id'] == gid)
            self.assertEqual(row['coverage_status'], 'covered-in-updated-batch-1')
            self.assertEqual(row['video_card'], card)
        self.assertTrue(all(r['current_status'] != 'obsolete-because-old' for r in rows))


if __name__ == '__main__':
    unittest.main()
