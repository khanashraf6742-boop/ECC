"""Batch 4 legal-scope, spoken-reference, document and actual-media contracts."""
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


class BatchFourTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / 'batch-04.json').read_text())
        self.cards = self.data['cards']
        self.script = json.loads((ROOT / 'batch-04-narration.json').read_text())

    def test_scope_and_exact_references(self):
        self.assertEqual(self.data['master_chapters'], [10, 11, 12, 13, 14, 15])
        self.assertGreaterEqual(len(self.cards), 75)
        self.assertEqual([c['id'] for c in self.cards], [f'B4-{n:02}' for n in range(1, len(self.cards) + 1)])
        refs = '\n'.join(c['ref'] for c in self.cards)
        for label in ('Rule 7(1)', 'Rule 7(2)', 'Rule 7 GID (1)', 'Rule 7 GID (2)',
                      'Rule 7 GID (3)', 'Rule 7 GID (7)', 'Rule 7 GID (8)',
                      'Rule 7 GID (10)', 'Rule 7 GID (11)', 'Rule 7 GID (12)',
                      'Rule 7 GID (14)', 'Rule 7 GID (16)', 'Rule 7 GID (17)',
                      'Rule 7 GID (19)', 'Rule 7 GID (20)', 'FAQ 25', 'FAQ 26', 'FAQ 27',
                      '24.11.2022', '24.04.2018', '28.02.2020', 'Rule 15 GID (1)'):
            self.assertIn(label, refs)
        for c in self.cards:
            self.assertTrue(all(c[k] for k in ('ref', 'rule', 'explanation_roman', 'example_roman', 'trap', 'source')))
            self.assertTrue(all(s in self.data['sources'] for s in c['source'].split(';')))
        self.assertIn('four, one and two', self.cards[62]['spoken_ref_roman'])
        self.assertIn('four, two, employee limb', self.cards[63]['spoken_ref_roman'])
        self.assertIn('four, two, family limb', self.cards[64]['spoken_ref_roman'])
        self.assertIn('Borrowing office paid', self.cards[73]['example_roman'])
        self.assertIn('Ravi ka statutory tax', self.cards[76]['example_roman'])
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
        from batch4_roman import romanize, spoken
        self.assertEqual(spoken('All India use karo.'), 'All India use करो.')
        with self.assertRaisesRegex(ValueError, 'Unreviewed'):
            romanize('असमीक्षित')
        for s in self.script:
            self.assertEqual(romanize(s['text']), s['roman_text'])
            self.assertFalse(any(w in s['text'] for w in ('रियायत', 'प्रतिपूर्ति', 'कार्मिक')))
        for ext in ('srt', 'vtt', 'ass'):
            self.assertIsNone(re.search(r'[\u0900-\u097f]', (ROOT / ('batch-04-video.' + ext)).read_text()))

    def test_caption_words_timing_and_formats(self):
        r = json.loads((ROOT / 'batch-04-subtitle-report.json').read_text())
        chapters = json.loads((ROOT / 'batch-04-video-report.json').read_text())['chapters']
        self.assertEqual(r['source_script_sha256'], hashlib.sha256((ROOT / 'batch-04-narration.json').read_bytes()).hexdigest())
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
            self.assertEqual((ROOT / ('batch-04-video.' + ext)).read_text().count(' --> '), len(r['cues']))
        self.assertEqual((ROOT / 'batch-04-video.ass').read_text().count('Dialogue: '), len(r['cues']))

    def test_actual_media_audio_chapters_faststart(self):
        import imageio_ffmpeg
        from build_subtitles import audio_digest
        r = json.loads((ROOT / 'batch-04-video-report.json').read_text())
        s = json.loads((ROOT / 'batch-04-subtitle-report.json').read_text())
        video = ROOT / 'batch-04-video.mp4'
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
        html = (ROOT / 'batch-04.html').read_text()
        self.assertIn(str(len(self.cards)) + ' exact-reference cards', html)
        self.assertIn('<th>Who acts?</th>', html)
        self.assertNotIn('Co-residence?', html)
        self.assertIn('BATCH-04-README.md', (ROOT / 'batch-04.md').read_text())
        for ext in ('html', 'md'):
            text = (ROOT / ('batch-04.' + ext)).read_text()
            for c in self.cards:
                self.assertIn(c['id'], text)
            self.assertIn('01.07.2017', text)
            self.assertIn('2026', text)
        for name in ('batch-04.pdf', 'batch-04-hinglish.mp3'):
            self.assertGreater((ROOT / name).stat().st_size, 10000)
        self.assertIn('Important dates', self.script[0]['roman_text'])
        self.assertIn('one year', self.script[0]['roman_text'])
        self.assertIn('Aaj ', self.script[0]['text'])

    def test_every_layout_and_phrase_partition(self):
        from build_batch4_video import opening, slide, parts, merge_readable
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

    def test_repaired_passage_provenance_and_positive_display_time(self):
        repair = json.loads((ROOT / 'batch-04-audio-repair.json').read_text())
        report = json.loads((ROOT / 'batch-04-video-report.json').read_text())
        chapter = report['chapters'][6]
        self.assertEqual(repair['voice_id'], 'voice-00')
        self.assertEqual(repair['repair_card'], 'B4-43')
        self.assertEqual(repair['combined']['sha256'], chapter['source_clip_sha256'])
        self.assertEqual(chapter['card_ids'][0], 'B4-43')
        pages = report['pages']
        page = next(p for p in pages if p['id'] == 'B4-43')
        self.assertGreater(page['end_seconds'] - page['start_seconds'], 8)
        self.assertTrue(all(p['end_seconds'] > p['start_seconds'] for p in pages))

    def test_register_rebuild_is_idempotent_and_does_not_complete_parent_instruments(self):
        import build_batch4 as builder
        with tempfile.TemporaryDirectory() as folder:
            original_root = builder.ROOT
            target = Path(folder) / 'gid-coverage-register.csv'
            target.write_bytes((ROOT / target.name).read_bytes())
            try:
                builder.ROOT = Path(folder)
                builder.register()
                first = target.read_bytes()
                builder.register()
                self.assertEqual(first, target.read_bytes())
            finally:
                builder.ROOT = original_root

    def test_gid_register_updates_only_taught_scopes(self):
        with (ROOT / 'gid-coverage-register.csv').open() as f:
            rows = {r['id']: r for r in csv.DictReader(f)}
        for ident in ('15.1', '15.1.a', '15.1.b', '15.1.c'):
            self.assertEqual(rows[ident]['coverage_status'], 'covered-in-batch-4')
            self.assertNotIn('pending', rows[ident]['current_status'])
        for ident in ('7.1', '7.1.route', '7.1.vacation', '7.1.class', '7.1.notice', '7.1.record', '7.2', '7.3', '7.7', '7.8', '7.10', '7.11', '7.12',
                      '7.14', '7.16', '7.19', '7.20', '7.19.i', '7.19.ii', '7.19.iii', '7.19.iv', '7.19.v'):
            self.assertEqual(rows[ident]['coverage_status'], 'covered-in-batch-4')
            self.assertIn('B4-', rows[ident]['video_card'])
        for ident in ('7.15', '7.17', '7.20', '7.20.iii', 'M-2025-FAQ', 'M-2025-GUIDE'):
            self.assertIn('B2-', rows[ident]['video_card'])
            self.assertIn('B4-', rows[ident]['video_card'])
        self.assertEqual(rows['5.1.transition']['coverage_status'], 'excluded-from-current-instruction')
        self.assertTrue(any(r['coverage_status'] == 'pending-topic-batch' for r in rows.values()))


if __name__ == '__main__':
    unittest.main()
