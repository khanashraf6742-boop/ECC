"""Video-specific coverage, readable-slide and packaging checks."""
import hashlib
import importlib.util
import json
import struct
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).parent


class VideoContentTests(unittest.TestCase):
    def test_video_summaries_cover_every_card_in_order(self):
        summaries = json.loads((ROOT / 'video-summaries.json').read_text())
        cards = json.loads((ROOT / 'batch-01.json').read_text())['cards']
        self.assertEqual([s['card_id'] for s in summaries], [c['id'] for c in cards])
        for summary in summaries:
            self.assertTrue(summary['point'])
            self.assertTrue(summary['example'])
            self.assertLessEqual(len(summary['point']), 120)
            self.assertLessEqual(len(summary['example']), 120)

    def test_video_chapters_do_not_reorder_the_spoken_clauses(self):
        segments = json.loads((ROOT / 'narration.json').read_text())
        summaries = json.loads((ROOT / 'video-summaries.json').read_text())
        self.assertEqual(len(segments), 10)
        self.assertEqual([u['card_id'] for s in segments for u in s['units']], [s['card_id'] for s in summaries])
        self.assertTrue(all(len(s['units']) <= 4 for s in segments))

    def test_packaged_video_has_matching_chapters_and_faststart(self):
        report = json.loads((ROOT / 'video-build-report.json').read_text())
        video = ROOT / report['file']
        self.assertEqual(video.stat().st_size, report['bytes'])
        self.assertLess(report['bytes'], 100 * 1024 * 1024)
        self.assertEqual((report['width'], report['height']), (1920, 1080))
        self.assertEqual(report['full_decode_check'], 'passed')
        self.assertEqual(report['source_script_sha256'], hashlib.sha256((ROOT / report.get('source_script_file', 'narration.json')).read_bytes()).hexdigest())
        self.assertEqual(len(report['chapters']), 16)
        self.assertEqual([card for chapter in report['chapters'] for card in chapter['card_ids'] if card.startswith('B1-')], [f'B1-{n:02}' for n in range(1, 31)])
        cursor = 0
        for chapter in report['chapters']:
            self.assertAlmostEqual(cursor, chapter['start_seconds'], places=2)
            self.assertGreater(chapter['end_seconds'], cursor)
            cursor = chapter['end_seconds']
        self.assertLess(abs(cursor - report['duration_seconds']), 1)
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

    def test_font_license_is_included(self):
        self.assertIn('SIL OPEN FONT LICENSE', (ROOT / 'video-fonts' / 'OFL.txt').read_text())
        for name in ('AtkinsonHyperlegible-Regular.ttf', 'AtkinsonHyperlegible-Bold.ttf'):
            self.assertGreater((ROOT / 'video-fonts' / name).stat().st_size, 10000)


@unittest.skipUnless(importlib.util.find_spec('PIL') and importlib.util.find_spec('mutagen'), 'Install video-requirements.txt for rendering tests')
class VideoRenderTests(unittest.TestCase):
    def test_all_chapter_slides_render_without_clipping(self):
        spec = importlib.util.spec_from_file_location('ltc_video', ROOT / 'build_video.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        segments = json.loads((ROOT / 'narration.json').read_text())
        summaries = {s['card_id']: s for s in json.loads((ROOT / 'video-summaries.json').read_text())}
        with tempfile.TemporaryDirectory() as directory:
            for index, segment in enumerate(segments):
                path = Path(directory) / f'{index}.png'
                audit = module.render_slide(index, segment, summaries, path)
                self.assertEqual(audit['canvas'], [1920, 1080])
                self.assertTrue(path.exists())
                self.assertTrue(all(size >= 26 for size in audit['body_font_sizes']))
        with self.assertRaises(ValueError):
            module.wrap('UnbrokenLongWord', module.font(30), 1)
        with self.assertRaises(ValueError):
            module.fit('Too much text ' * 1000, 100, 20, 30, 26)


if __name__ == '__main__':
    unittest.main()
