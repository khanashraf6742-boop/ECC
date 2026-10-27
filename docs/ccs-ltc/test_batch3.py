"""Batch 3 legal-scope, spoken-reference, document and actual-media contracts."""
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


class BatchThreeTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / 'batch-03.json').read_text())
        self.cards = self.data['cards']
        self.script = json.loads((ROOT / 'batch-03-narration.json').read_text())

    def test_scope_and_exact_references(self):
        self.assertEqual(self.data['master_chapters'], [9])
        self.assertEqual(len(self.cards), 32)
        self.assertEqual([c['id'] for c in self.cards], [f'B3-{n:02}' for n in range(1, 33)])
        refs = '\n'.join(c['ref'] for c in self.cards)
        for clause in ('i', 'ii', 'iii', 'iv'):
            self.assertIn('Rule 5 GID (1), criterion (' + clause + ')', refs)
        for label in ('Rule 4(e)', 'Rule 5', 'Rule 6', 'Rule 7 GID (4)', 'FAQ 19;', 'FAQ 20;'):
            self.assertIn(label, refs)
        for c in self.cards:
            self.assertTrue(all(c[k] for k in ('ref', 'rule', 'explanation_roman', 'example_roman', 'trap', 'source')))
            self.assertTrue(all(s in self.data['sources'] for s in c['source'].split(';')))
        self.assertNotIn('Rule 5(2)', refs)  # No invented statutory subrules.

    def test_every_card_spoken_once_reference_point_example(self):
        self.assertEqual([u['card_id'] for s in self.script for u in s['units']], [c['id'] for c in self.cards])
        self.assertEqual(self.script[0]['voice'], 'voice-01')
        self.assertTrue(all(s['voice'] == 'voice-00' for s in self.script[1:]))
        self.assertLessEqual(len(self.script), 10)
        for s in self.script:
            self.assertLessEqual(len(s['text']), 1500)
            if s['units']:
                self.assertEqual(s['text'], ' '.join(' '.join((u['spoken_ref'], u['explanation'], 'Example, ' + u['example'])) for u in s['units']))

    def test_romanisation_and_no_formal_hindi(self):
        from batch3_roman import romanize, spoken
        self.assertEqual(spoken('All India use karo.'), 'All India use करो.')
        with self.assertRaisesRegex(ValueError, 'Unreviewed'):
            romanize('असमीक्षित')
        for s in self.script:
            self.assertEqual(romanize(s['text']), s['roman_text'])
            self.assertFalse(any(w in s['text'] for w in ('रियायत', 'प्रतिपूर्ति', 'कार्मिक')))
        for ext in ('srt', 'vtt', 'ass'):
            self.assertIsNone(re.search(r'[\u0900-\u097f]', (ROOT / ('batch-03-video.' + ext)).read_text()))

    def test_caption_words_timing_and_formats(self):
        r = json.loads((ROOT / 'batch-03-subtitle-report.json').read_text())
        chapters = json.loads((ROOT / 'batch-03-video-report.json').read_text())['chapters']
        self.assertEqual(r['source_script_sha256'], hashlib.sha256((ROOT / 'batch-03-narration.json').read_bytes()).hexdigest())
        for i, segment in enumerate(self.script, 1):
            cues = [c for c in r['cues'] if c['chapter'] == i]
            self.assertEqual(' '.join(c['spoken_text'] for c in cues).split(), segment['text'].split())
            self.assertEqual(' '.join(c['text'] for c in cues).split(), segment['roman_text'].split())
        end = 0
        for c in r['cues']:
            self.assertGreaterEqual(c['start'], end)
            self.assertGreaterEqual(c['end'] - c['start'], .55)
            self.assertLessEqual(c['end'] - c['start'], 8)
            self.assertLessEqual(len(c['text']) / (c['end'] - c['start']), 35)
            self.assertLessEqual(len(c['text']), 150)
            self.assertLessEqual(c['end'], chapters[c['chapter'] - 1]['end_seconds'])
            end = c['end']
        for ext in ('srt', 'vtt'):
            self.assertEqual((ROOT / ('batch-03-video.' + ext)).read_text().count(' --> '), len(r['cues']))
        self.assertEqual((ROOT / 'batch-03-video.ass').read_text().count('Dialogue: '), len(r['cues']))

    def test_actual_media_audio_chapters_faststart(self):
        import imageio_ffmpeg
        from build_subtitles import audio_digest
        r = json.loads((ROOT / 'batch-03-video-report.json').read_text())
        s = json.loads((ROOT / 'batch-03-subtitle-report.json').read_text())
        video = ROOT / 'batch-03-video.mp4'
        self.assertEqual(video.stat().st_size, r['bytes'])
        self.assertEqual((r['width'], r['height']), (1920, 1080))
        self.assertEqual(r['full_decode_check'], 'passed')
        self.assertEqual(r['source_script_sha256'], s['source_script_sha256'])
        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
        self.assertEqual(audio_digest(ffmpeg, video), s['audio_sha256'])
        media = subprocess.run([ffmpeg, '-hide_banner', '-i', str(video)], text=True, capture_output=True).stderr
        self.assertEqual(len(r['chapters']), len(self.script))
        for c in r['chapters']:
            self.assertIn(f'Chapter #0:{c["number"] - 1}: start {c["start_seconds"]:.6f}, end {c["end_seconds"]:.6f}', media)
        atoms = []
        with video.open('rb') as f:
            offset = 0
            while offset < r['bytes']:
                f.seek(offset)
                size, kind = struct.unpack('>I4s', f.read(8))
                if size == 1:
                    size = struct.unpack('>Q', f.read(8))[0]
                if size == 0:
                    size = r['bytes'] - offset
                self.assertGreaterEqual(size, 8)
                atoms.append(kind)
                offset += size
        self.assertLess(atoms.index(b'moov'), atoms.index(b'mdat'))
        self.assertEqual([p['id'] for p in r['pages']][2:], [c['id'] for c in self.cards])

    def test_written_companions_and_date_opening(self):
        html = (ROOT / 'batch-03.html').read_text()
        self.assertIn('32 exact-reference cards', html)
        self.assertIn('<th>Who acts?</th>', html)
        self.assertNotIn('Co-residence?', html)
        self.assertIn('BATCH-03-README.md', (ROOT / 'batch-03.md').read_text())
        for ext in ('html', 'md'):
            text = (ROOT / ('batch-03.' + ext)).read_text()
            for c in self.cards:
                self.assertIn(c['id'], text)
            self.assertIn('31.10.1958', text)
            self.assertIn('2026', text)
        for name in ('batch-03.pdf', 'batch-03-hinglish.mp3'):
            self.assertGreater((ROOT / name).stat().st_size, 10000)
        self.assertIn('Important dates', self.script[0]['roman_text'])
        self.assertIn('expired', self.script[0]['roman_text'])
        self.assertIn('Aaj ', self.script[0]['text'])

    def test_every_layout_and_phrase_partition(self):
        from build_batch3_video import opening, slide, parts, merge_readable
        from PIL import Image
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'slide.png'
            for c in self.cards:
                audit = slide(c, path)
                self.assertTrue(all(size >= 26 for size in audit['body_font_sizes']))
                with Image.open(path) as image:
                    self.assertEqual(image.size, (1920, 1080))
                    self.assertEqual(image.getpixel((960, 1000)), (17, 27, 38))
            for name in ('OPEN-LEGAL', 'OPEN-PRACTICAL'):
                self.assertEqual(opening(name, path)['caption_band_height'], 144)
        for s in self.script:
            self.assertEqual(' '.join(text for _, text in parts(s)).split(), s['text'].split())
        cues = [dict(start=0, end=.3, text='Example,'), dict(start=.3, end=3, text='normal words.')]
        self.assertEqual(merge_readable(cues), [dict(start=0, end=3, text='Example, normal words.')])
        self.assertEqual(len(cues), 2)
        with self.assertRaisesRegex(ValueError, 'too fast'):
            merge_readable([dict(start=0, end=.1, text='Too much fast text')])
        with self.assertRaisesRegex(ValueError, 'unreadably long'):
            merge_readable([dict(start=0, end=.8, text='word ' * 32), dict(start=.8, end=1.6, text='word ' * 32)])

    def test_gid_coverage_does_not_reactivate_expired_window(self):
        with (ROOT / 'gid-coverage-register.csv').open() as f:
            rows = {r['id']: r for r in csv.DictReader(f)}
        for ident in ('5.1', '5.1.i', '5.1.ii', '5.1.iii', '5.1.iv', '5.1.note', '7.4'):
            self.assertEqual(rows[ident]['coverage_status'], 'covered-in-batch-3')
            self.assertIn('B3-', rows[ident]['video_card'])
        self.assertEqual(rows['5.1.transition']['current_status'], 'expired-one-time-window')
        self.assertEqual(rows['5.1.transition']['coverage_status'], 'excluded-from-current-instruction')
        for ident in ('M-2025-FAQ', 'M-2025-GUIDE'):
            self.assertTrue(rows[ident]['coverage_status'].startswith('partially-covered'))
            self.assertIn('B2-', rows[ident]['video_card'])
            self.assertIn('B3-', rows[ident]['video_card'])
        self.assertTrue(any(r['coverage_status'] == 'pending-topic-batch' for r in rows.values()))


if __name__ == '__main__':
    unittest.main()
