"""Batch 2 acceptance contracts: legal coverage, script, captions and packaging."""
import csv
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).parent


class BatchTwoTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / 'batch-02.json').read_text())
        self.cards = self.data['cards']
        self.script = json.loads((ROOT / 'batch-02-narration.json').read_text())

    def test_clause_and_gid_coverage(self):
        refs = '\n'.join(c['ref'] for c in self.cards)
        for clause in 'abcdef':
            self.assertIn('Rule 4(' + clause + ')', refs)
        for clause in ('i', 'ii', 'iii', 'iv'):
            self.assertIn('Rule 4(d)(' + clause + ')', refs)
        for clause in ('i', 'ii', 'iii'):
            self.assertIn('Explanation 1(' + clause + ')', refs)
        for n in ('1', '2', '3', '4'):
            self.assertIn('Rule 4 GID (' + n + ')', refs)
        for clause in ('i', 'ii', 'vi'):
            self.assertIn('Rule 4 GID (2)(' + clause + ')', refs)
        for q in range(1, 13):
            self.assertIn('FAQ ' + str(q) + ';', refs)
        self.assertIn('FAQ 74;', refs)
        self.assertIn('FAQ 75;', refs)
        for c in self.cards:
            for k in ('id', 'ref', 'title', 'rule', 'explanation_roman', 'example_roman', 'trap', 'source'):
                self.assertTrue(c[k])
        self.assertEqual(len(set(c['id'] for c in self.cards)), len(self.cards))

    def test_all_cards_are_spoken_with_immediate_examples(self):
        units = [u for s in self.script for u in s['units']]
        self.assertEqual([u['card_id'] for u in units], [c['id'] for c in self.cards])
        self.assertLessEqual(len(self.script), 10)
        self.assertEqual(self.script[0]['voice'], 'voice-01')
        self.assertTrue(all(s['voice'] == 'voice-00' for s in self.script[1:]))
        for s in self.script:
            self.assertLessEqual(len(s['text']), 1500)
            if s['units']:
                text = ' '.join(' '.join((u['spoken_ref'], u['explanation'], 'Example, ' + u['example'])) for u in s['units'])
                self.assertEqual(s['text'], text)

    def test_no_devanagari_and_no_missing_caption_words(self):
        report = json.loads((ROOT / 'batch-02-subtitle-report.json').read_text())
        for ext in ('srt', 'vtt', 'ass'):
            text = (ROOT / ('batch-02-video.' + ext)).read_text()
            self.assertIsNone(re.search(r'[\u0900-\u097f]', text))
        for i, s in enumerate(self.script, 1):
            cues = [c for c in report['cues'] if c['chapter'] == i]
            self.assertEqual(' '.join(c['spoken_text'] for c in cues).split(), s['text'].split())
            self.assertEqual(' '.join(c['text'] for c in cues).split(), s['roman_text'].split())
        previous = 0
        for cue in report['cues']:
            self.assertGreaterEqual(cue['start'], previous)
            self.assertGreater(cue['end'], cue['start'])
            self.assertLessEqual(len(cue['text']) / (cue['end'] - cue['start']), 35)
            previous = cue['end']
        self.assertEqual(report['full_decode_check'], 'passed')
        self.assertTrue(report['audio_stream_unchanged'])

    def test_media_and_written_companions_match(self):
        r = json.loads((ROOT / 'batch-02-video-report.json').read_text())
        self.assertEqual(r['source_script_sha256'], hashlib.sha256((ROOT / 'batch-02-narration.json').read_bytes()).hexdigest())
        self.assertEqual((ROOT / r['file']).stat().st_size, r['bytes'])
        self.assertEqual(len(r['chapters']), len(self.script))
        self.assertEqual(r['full_decode_check'], 'passed')
        self.assertEqual(r['width'], 1920)
        self.assertEqual(r['height'], 1080)
        for ext in ('md', 'html'):
            text = (ROOT / ('batch-02.' + ext)).read_text()
            for card in self.cards:
                self.assertIn(card['id'], text)
        self.assertGreater((ROOT / 'batch-02.pdf').stat().st_size, 10000)
        self.assertGreater((ROOT / 'batch-02-hinglish.mp3').stat().st_size, 10000)

    def test_gid_register_records_actual_teaching_not_just_plans(self):
        with (ROOT / 'gid-coverage-register.csv').open() as file:
            rows = list(csv.DictReader(file))
        for ident in ('4.1', '4.2', '4.2.i', '4.2.ii', '4.2.vi', '4.3', '4.4', '7.5'):
            row = next(r for r in rows if r['id'] == ident)
            self.assertEqual(row['coverage_status'], 'covered-in-batch-2')
            self.assertTrue(row['video_card'].startswith('B2-'))

    def test_reversible_city_hinglish_not_translation(self):
        from batch2_roman import spoken, romanize
        self.assertEqual(spoken('All India use karo.'), 'All India use करो.')
        self.assertEqual(romanize(spoken('Bachche ke liye current rate nahi.')), 'Bachche ke liye current rate nahi.')
        with self.assertRaisesRegex(ValueError, 'Unreviewed'):
            romanize('असमीक्षित')
        for segment in self.script:
            self.assertEqual(romanize(segment['text']), segment['roman_text'])
            self.assertFalse(any(w in segment['text'] for w in ('परिवार', 'आश्रित', 'रियायत', 'प्रतिपूर्ति')))

    def test_caption_formats_lengths_and_actual_timing_bounds(self):
        report = json.loads((ROOT / 'batch-02-subtitle-report.json').read_text())
        chapters = json.loads((ROOT / 'batch-02-video-report.json').read_text())['chapters']
        for ext in ('srt', 'vtt'):
            self.assertEqual((ROOT / ('batch-02-video.' + ext)).read_text().count(' --> '), len(report['cues']))
        self.assertEqual((ROOT / 'batch-02-video.ass').read_text().count('Dialogue: '), len(report['cues']))
        for cue in report['cues']:
            chapter = chapters[cue['chapter'] - 1]
            self.assertGreaterEqual(cue['start'], chapter['start_seconds'])
            self.assertLessEqual(cue['end'], chapter['end_seconds'])
            self.assertGreaterEqual(cue['end'] - cue['start'], .55)
            self.assertLessEqual(cue['end'] - cue['start'], 8)
            self.assertLessEqual(len(cue['text']), 120)

    def test_actual_aac_chapters_and_faststart(self):
        import imageio_ffmpeg
        from build_subtitles import audio_digest
        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
        report = json.loads((ROOT / 'batch-02-video-report.json').read_text())
        captions = json.loads((ROOT / 'batch-02-subtitle-report.json').read_text())
        video = ROOT / 'batch-02-video.mp4'
        self.assertEqual(audio_digest(ffmpeg, video), captions['audio_sha256'])
        media = subprocess.run([ffmpeg, '-hide_banner', '-i', str(video)], text=True, capture_output=True).stderr
        for c in report['chapters']:
            self.assertIn(f'Chapter #0:{c["number"] - 1}: start {c["start_seconds"]:.6f}, end {c["end_seconds"]:.6f}', media)
        atoms = []
        with video.open('rb') as handle:
            offset = 0
            while offset < report['bytes']:
                handle.seek(offset)
                size, kind = struct.unpack('>I4s', handle.read(8))
                if size == 1:
                    size = struct.unpack('>Q', handle.read(8))[0]
                if size == 0:
                    size = report['bytes'] - offset
                self.assertGreaterEqual(size, 8)
                atoms.append(kind)
                offset += size
        self.assertLess(atoms.index(b'moov'), atoms.index(b'mdat'))

    def test_every_card_and_both_date_pages_render_without_clipping(self):
        from build_batch2_video import slide, opening
        from PIL import Image
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'slide.png'
            for c in self.cards:
                audit = slide(c, path)
                self.assertTrue(all(size >= 26 for size in audit['body_font_sizes']))
                with Image.open(path) as image:
                    self.assertEqual(image.size, (1920, 1080))
                    self.assertEqual(image.getpixel((960, 1000)), (17, 27, 38))
            for ident in ('OPEN-LEGAL', 'OPEN-PRACTICAL'):
                self.assertEqual(opening(ident, path)['caption_band_height'], 144)

    def test_phrase_partition_and_readability_fail_closed(self):
        from build_batch2_video import parts, merge_readable
        for segment in self.script:
            self.assertEqual(' '.join(t for _, t in parts(segment)).split(), segment['text'].split())
        cues = [dict(start=0, end=.3, text='Example,'), dict(start=.3, end=3, text='normal words.')]
        merged = merge_readable(cues)
        self.assertEqual(merged, [dict(start=0, end=3, text='Example, normal words.')])
        self.assertEqual(len(cues), 2)  # Input is not mutated.
        with self.assertRaisesRegex(ValueError, 'too fast'):
            merge_readable([dict(start=0, end=.1, text='An unreadable fast caption')])
        with self.assertRaisesRegex(ValueError, 'unreadably long'):
            merge_readable([dict(start=0, end=.8, text='word ' * 32), dict(start=.8, end=1.6, text='word ' * 32)])

    def test_partial_topics_and_all_six_illustrations_are_honest(self):
        with (ROOT / 'gid-coverage-register.csv').open() as file:
            rows = list(csv.DictReader(file))
        for ident in ('7.20', '7.20.iii', 'M-2025-FAQ', 'M-2025-GUIDE'):
            self.assertEqual(next(r['coverage_status'] for r in rows if r['id'] == ident), 'partially-covered-in-batch-2')
        for ident in ('7.5.I.i', '7.5.I.ii', '7.5.II.i', '7.5.II.ii', '7.5.II.iii', '7.5.II.iv'):
            self.assertEqual(next(r['coverage_status'] for r in rows if r['id'] == ident), 'covered-in-batch-2')
        self.assertEqual(len(rows), len({r['id'] for r in rows}))
        self.assertTrue(any(r['coverage_status'] == 'pending-topic-batch' for r in rows))


if __name__ == '__main__':
    unittest.main()
