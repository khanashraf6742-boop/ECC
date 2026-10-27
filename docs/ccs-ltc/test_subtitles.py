"""Regression checks for the captioned edition; no speech service is needed."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).parent
SPEC = importlib.util.spec_from_file_location('ltc_subtitles', ROOT / 'build_subtitles.py')


class SubtitleTests(unittest.TestCase):
    def test_transcript_is_preserved_and_cues_are_bounded(self):
        report = json.loads((ROOT / 'subtitle-build-report.json').read_text())
        segments = json.loads((ROOT / 'narration.json').read_text())
        chapters = json.loads((ROOT / 'video-build-report.json').read_text())['chapters']
        cues = report['cues']
        self.assertGreater(len(cues), 100)
        previous_end = 0
        for cue in cues:
            self.assertGreaterEqual(cue['start'], previous_end)
            duration = cue['end'] - cue['start']
            self.assertGreater(duration, .35)
            self.assertLessEqual(duration, 8)
            self.assertLessEqual(len(cue['text']), 90)
            self.assertLessEqual(len(cue['text']) / duration, 30)
            self.assertLessEqual(cue['end'], chapters[cue['chapter'] - 1]['end_seconds'])
            self.assertGreaterEqual(cue['start'], chapters[cue['chapter'] - 1]['start_seconds'])
            previous_end = cue['end']
        for chapter, segment in enumerate(segments, 1):
            actual = ' '.join(c['text'] for c in cues if c['chapter'] == chapter)
            self.assertEqual(actual.split(), segment['text'].split())
        self.assertEqual(report['source_script_sha256'], hashlib.sha256((ROOT / 'narration.json').read_bytes()).hexdigest())
        self.assertEqual(report['alignment'], 'chapter-local MFCC / dynamic time warping against eSpeak NG reference speech')
        self.assertEqual(report['full_decode_check'], 'passed')
        self.assertEqual(report['audio_stream_unchanged'], True)

    def test_srt_vtt_and_ass_have_the_same_cues(self):
        cues = json.loads((ROOT / 'subtitle-build-report.json').read_text())['cues']
        srt = (ROOT / 'batch-01-video.srt').read_text()
        vtt = (ROOT / 'batch-01-video.vtt').read_text()
        ass = (ROOT / 'batch-01-video.ass').read_text()
        self.assertEqual(srt.count(' --> '), len(cues))
        self.assertEqual(vtt.count(' --> '), len(cues))
        self.assertEqual(ass.count('Dialogue: '), len(cues))
        self.assertTrue(vtt.startswith('WEBVTT\n'))
        self.assertIn('PlayResY: 1080', ass)
        self.assertIn('Noto Sans Devanagari', ass)
        # Legal references must remain in the delivered captions.
        self.assertIn('clause Roman one.', srt)
        self.assertIn('clause A.', srt)

    @unittest.skipUnless(importlib.util.find_spec('imageio_ffmpeg'), 'Install subtitle-requirements.txt')
    def test_final_audio_bitstream_matches_alignment_source(self):
        import imageio_ffmpeg
        report = json.loads((ROOT / 'subtitle-build-report.json').read_text())
        digest = subprocess.check_output([
            imageio_ffmpeg.get_ffmpeg_exe(), '-v', 'error', '-i', str(ROOT / 'batch-01-video.mp4'),
            '-map', '0:a:0', '-c:a', 'copy', '-f', 'hash', '-hash', 'sha256', '-'], text=True).strip()
        self.assertEqual(digest, report['audio_sha256'])
        self.assertEqual((ROOT / 'batch-01-video.mp4').stat().st_size, report['video_bytes'])

    @unittest.skipUnless(importlib.util.find_spec('imageio_ffmpeg'), 'Install subtitle-requirements.txt')
    def test_repeated_render_cannot_double_scale_or_burn_captions(self):
        before = hashlib.sha256((ROOT / 'batch-01-video.mp4').read_bytes()).hexdigest()
        result = subprocess.run([sys.executable, str(ROOT / 'build_subtitles.py'), '--render-only'],
                                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Video already captioned', result.stderr)
        self.assertEqual(before, hashlib.sha256((ROOT / 'batch-01-video.mp4').read_bytes()).hexdigest())

    def test_splitting_and_timestamp_rounding(self):
        module = importlib.util.module_from_spec(SPEC)
        SPEC.loader.exec_module(module)
        text = 'Rule one, sub rule three, clause Roman one. Union civil services और posts covered हैं.'
        parts = module.split_phrases(text)
        self.assertEqual(' '.join(parts).split(), text.split())
        self.assertTrue(all(len(part) <= 90 for part in parts))
        self.assertEqual(module.timestamp(59.9996), '00:01:00,000')
        self.assertEqual(module.timestamp(3600.123), '01:00:00,123')
        self.assertEqual(module.timestamp(12.34, vtt=True), '00:00:12.340')
        self.assertEqual(module.ass_timestamp(59.999), '0:01:00.00')


if __name__ == '__main__':
    unittest.main()
