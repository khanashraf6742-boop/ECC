#!/usr/bin/env python3
"""Offline structural, source-caution, caption, review and HTTP-range checks.

Run from this directory: python3 -m unittest -v test_course
These checks cannot establish legal completeness or human-verbatim accuracy.
"""
from copy import deepcopy
from html.parser import HTMLParser
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse
import hashlib
import json
import re
import threading
import unittest

import build_batch_02 as lecture
import align_captions
import build_review
from serve_course import CourseHandler

ROOT = Path(__file__).resolve().parent


def read_vtt(name):
    raw = (ROOT / name).read_text(encoding='utf-8')
    cues = []
    for block in re.split(r'\n\s*\n', raw):
        lines = block.splitlines()
        if len(lines) < 3 or not lines[0].isdigit():
            continue
        match = re.fullmatch(r'(\d\d:\d\d:\d\d\.\d{3}) --> (\d\d:\d\d:\d\d\.\d{3})(.*)', lines[1])
        if not match:
            raise AssertionError(f'Invalid cue timing: {lines[1]}')
        cues.append((match.group(1), match.group(2), match.group(3), ' '.join(lines[2:])))
    return raw, cues


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links = [], []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if 'id' in values:
            self.ids.append(values['id'])
        for attr in ('href', 'src'):
            if attr in values:
                self.links.append(values[attr])


class LessonTests(unittest.TestCase):
    def test_schema_examples_and_stale_missing_example(self):
        data = lecture.load_data()
        lecture.audit(data)
        self.assertEqual(len(data['sections']), 10)
        self.assertEqual(sum(len(s['beats']) for s in data['sections']), 20)
        for section in data['sections']:
            for beat in section['beats']:
                self.assertEqual(len(beat['lines']), len(beat['english_lines']))
                self.assertTrue(all(len(line) <= 76 for line in beat['lines']))
        broken = deepcopy(data)
        broken['sections'][0]['beats'][0]['example'] = ''
        with self.assertRaises(SystemExit):
            lecture.audit(broken)

    def test_sources_examples_and_coverage_for_all_57_units(self):
        text = (ROOT / 'Batch-02-Guide.md').read_text(encoding='utf-8')
        parts = re.split(r'(?m)^### (\d+) — [^\n]+\n', text)
        units = {int(parts[i]): parts[i+1] for i in range(1, len(parts), 2)}
        self.assertEqual(sorted(units), list(range(1, 58)))
        for number, unit in units.items():
            with self.subTest(unit=number):
                self.assertRegex(unit, r'\[S\d+\]')
                self.assertTrue('**Example:' in unit or '| Example' in unit)
        self.assertIn('conflict', units[23].lower())
        self.assertIn('unresolved', units[23].lower())
        self.assertIn('Level 7', units[23])
        self.assertIn('one step below', units[29])
        self.assertIn('25%', units[30])
        self.assertIn('breakfast', units[31].lower())
        self.assertIn('Ladakh', units[46])
        self.assertIn('not reopened', units[46])
        self.assertIn('three- or four-class', units[34])
        self.assertIn('not automatically', units[35].lower())
        self.assertIn('₹30/km', units[42])
        self.assertIn('₹15/km', units[42])
        self.assertIn('not automatically', units[50])
        self.assertIn('human-verbatim', text)
        self.assertIn('not exhaustively audited', text.lower())

    def test_slides_distinguish_class_funding_and_conflict(self):
        d = lecture.load_data()['sections']
        air = d[0]['beats'][1]
        self.assertIn('13A', air['rule'])
        self.assertIn('17+', air['rule'])
        self.assertIn('first', d[3]['beats'][0]['rule'].lower())
        self.assertIn('next 14', d[3]['beats'][0]['rule'])
        self.assertIn('first 7', d[3]['beats'][1]['rule'])
        self.assertIn('conflict', d[5]['beats'][1]['rule'])
        self.assertIn('3 OR BELOW', str(d[6]['beats'][1]['cards']))
        self.assertIn('SCI', d[6]['beats'][1]['rule'])
        self.assertIn('AC taxi is not permissible', d[7]['beats'][0]['trap'])
        self.assertIn('neighbouring State', d[8]['beats'][0]['rule'])
        self.assertIn('not automatically', d[8]['beats'][1]['trap'])

    def test_narration_and_transliteration_coverage(self):
        data = lecture.load_data()
        saved = (ROOT / 'Narration-hi.txt').read_text(encoding='utf-8')
        dictionary = json.loads((ROOT / 'notes/roman-hindi.json').read_text(encoding='utf-8'))
        self.assertIn('CITY HINGLISH NARRATION SCRIPT', saved)
        self.assertIn('Chapter 04 opens with a sentence from chapter 06', saved)
        for section in data['sections']:
            script = lecture.section_tts_text(section)
            self.assertIn(script, saved)
            self.assertIsNone(re.search(r'[\u0900-\u097f]', lecture.romanize_hinglish(script, dictionary)))

    def test_alignment_and_timeline(self):
        data, alignment = lecture.load_data(), lecture.load_alignment()
        durations = [x['duration'] for x in alignment['sections']]
        timeline, captions, total = lecture.build_timeline(data, durations, alignment)
        self.assertEqual(len(timeline), 20)
        self.assertEqual(len(captions), 114)
        self.assertTrue(439 < total < 440)
        self.assertLessEqual(captions[-1][1], total)
        for before, after in zip(captions, captions[1:]):
            self.assertLessEqual(before[1], after[0] + .001)
        self.assertEqual(lecture.stamp(3723.456), '01:02:03.456')

    def test_vtt_timing_text_and_roman_script(self):
        data, alignment = lecture.load_data(), lecture.load_alignment()
        _, captions, _ = lecture.build_timeline(data, [x['duration'] for x in alignment['sections']], alignment)
        translations = lecture.translated_captions(data, alignment)
        dictionary = json.loads((ROOT / 'notes/roman-hindi.json').read_text(encoding='utf-8'))
        en_raw, en = read_vtt('Captions-en.vtt')
        roman_raw, roman = read_vtt('Captions-roman.vtt')
        for raw in (en_raw, roman_raw):
            self.assertTrue(raw.startswith('WEBVTT\n'))
            self.assertIsNone(re.search(r'[\u0900-\u097f]', raw))
            self.assertIn('human', raw.lower())
            self.assertIn('automatic', raw.lower())
        self.assertIn('translation', en_raw.lower())
        self.assertIn('transliteration', roman_raw.lower())
        self.assertEqual(len(en), len(captions))
        self.assertEqual(len(roman), len(captions))
        for i, ((start, end, source), translated) in enumerate(zip(captions, translations)):
            with self.subTest(cue=i+1):
                times = (lecture.stamp(start), lecture.stamp(end))
                self.assertEqual(en[i][:2], times)
                self.assertEqual(roman[i][:2], times)
                self.assertEqual(en[i][3], translated)
                self.assertEqual(roman[i][3], lecture.romanize_hinglish(source, dictionary))
                self.assertIn('line:0%', en[i][2])
        self.assertNotIn('road T\nA', roman_raw)
        self.assertNotIn('three\nhundred', roman_raw)
        self.assertTrue(any('T A' in line for line in lecture.wrap_caption('Hey everyone! Batch Two mein international air, sea aur road T A seekhenge.')))

    def test_number_groups_do_not_cross_cue_boundaries(self):
        line = 'word ' * 13 + 'two thousand kilo remaining'
        section = {'beats': [{'lines': [line]}, {'lines': ['end']}]}
        def words(text):
            return [{'text': word, 'start': i*.2, 'end': i*.2+.15} for i, word in enumerate(text.split())]
        blocks = [{'beat': 1, 'words': words(line)},
                  {'beat': 2, 'words': [{'text': 'end', 'start': 9, 'end': 10}]}]
        cues = align_captions.make_cues(section, blocks)
        self.assertTrue(any('two thousand' in c['text'] for c in cues))
        self.assertFalse(any(c['text'].endswith(' two') for c in cues))

    def test_rejects_stale_audio_script_and_translation(self):
        d, a = lecture.load_data(), lecture.load_alignment()
        durations = [x['duration'] for x in a['sections']]
        stale = deepcopy(a); stale['sections'][0]['audio_sha256'] = 'wrong'
        with self.assertRaisesRegex(ValueError, 'audio changed'):
            lecture.build_timeline(d, durations, stale)
        stale = deepcopy(a); stale['sections'][0]['script_sha256'] = 'wrong'
        with self.assertRaisesRegex(ValueError, 'narration text changed'):
            lecture.build_timeline(d, durations, stale)
        stale = deepcopy(a); stale['sections'][0]['cues'][0]['text'] += ' extra'
        with self.assertRaisesRegex(ValueError, 'different source cues'):
            lecture.translated_captions(d, stale)

    def test_audio_recognition_evidence_binds_to_all_current_clips(self):
        d, a = lecture.load_data(), lecture.load_alignment()
        block = json.loads((ROOT / 'notes/asr-review.json').read_text(encoding='utf-8'))
        whole = json.loads((ROOT / 'notes/whole-audio-review.json').read_text(encoding='utf-8'))
        self.assertIn('UNEDITED AUTOMATIC', block['disclosure'])
        self.assertEqual(len(block['sections']), 10)
        self.assertEqual(len(whole['sections']), 10)
        for s, aligned, review, full in zip(d['sections'], a['sections'], block['sections'], whole['sections']):
            digest = hashlib.sha256((ROOT / 'audio' / s['audio']).read_bytes()).hexdigest()
            self.assertEqual(digest, aligned['audio_sha256'])
            self.assertEqual(digest, review['audio_sha256'])
            self.assertEqual(digest, full['audio_sha256'])
            self.assertEqual(' '.join(x['text'] for x in aligned['words']), lecture.section_tts_text(s))
        self.assertIn('September 2023', ' '.join(x['text'] for x in whole['sections'][3]['segments']))
        self.assertTrue((ROOT / 'audio/source-04-original.mp3').is_file())

    def test_review_page_hashes_and_parser(self):
        page = (ROOT / 'Caption-Review.html').read_text(encoding='utf-8')
        match = re.search(r'const source=(\{[^\n]+\});', page)
        self.assertIsNotNone(match)
        source = json.loads(match.group(1))
        self.assertEqual(source['video_sha256'], hashlib.sha256((ROOT / 'Batch-02-Lecture.mp4').read_bytes()).hexdigest())
        self.assertEqual(source['caption_sha256'], hashlib.sha256((ROOT / 'Captions-roman.vtt').read_bytes()).hexdigest())
        self.assertEqual(source['cues'], build_review.parse_vtt((ROOT / 'Captions-roman.vtt').read_text(encoding='utf-8')))
        self.assertEqual(len(source['cues']), 114)
        self.assertIn('I listened and checked this cue', page)
        self.assertIn('not yet human-verified', page.lower())
        for bad in ('', 'WEBVTT\n\n1\n00:00:02.000 --> 00:00:01.000\ntext',
                    'WEBVTT\n\n1\n00:00:00.000 --> 00:00:02.000\nx\n\n2\n00:00:01.000 --> 00:00:03.000\ny'):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                build_review.parse_vtt(bad)

    def test_disclosure_and_html_local_links(self):
        html = (ROOT / 'Batch-02-Guide.html').read_text(encoding='utf-8')
        notes = (ROOT / 'Caption-Check.md').read_text(encoding='utf-8')
        for content in (html, notes):
            self.assertIn('automatic', content.lower())
            self.assertIn('human', content.lower())
            self.assertIn('verbatim', content.lower())
        self.assertIn('burned-in Roman-Hinglish', html)
        self.assertIn('Caption-Review.html', html)
        self.assertIn('Captions-en.vtt', html)
        self.assertIn('Captions-roman.vtt', html)
        parser = LinkParser(); parser.feed(html)
        self.assertEqual(len(parser.ids), len(set(parser.ids)))
        for link in parser.links:
            with self.subTest(link=link):
                if link.startswith('#'):
                    self.assertIn(unquote(link[1:]), parser.ids)
                elif not urlparse(link).scheme:
                    self.assertTrue((ROOT / unquote(link)).is_file())


class QuietHandler(CourseHandler):
    def log_message(self, *_args):
        pass


class RangeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), QuietHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start(); cls.port = cls.server.server_port
        cls.video = ROOT / 'Batch-02-Lecture.mp4'; cls.size = cls.video.stat().st_size

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown(); cls.server.server_close(); cls.thread.join()

    def request(self, path, headers=None):
        conn = HTTPConnection('127.0.0.1', self.port, timeout=5)
        conn.request('GET', path, headers=headers or {})
        response = conn.getresponse(); result = response.status, dict(response.getheaders()), response.read()
        conn.close(); return result

    def test_seek_ranges_suffix_and_invalid(self):
        path = '/batch-02/Batch-02-Lecture.mp4'
        status, headers, body = self.request(path, {'Range': 'bytes=20-29'})
        self.assertEqual(status, 206)
        self.assertEqual(headers['Content-Range'], f'bytes 20-29/{self.size}')
        with self.video.open('rb') as source:
            source.seek(20); self.assertEqual(body, source.read(10))
        status, headers, body = self.request(path, {'Range': 'bytes=-15'})
        self.assertEqual(status, 206); self.assertEqual(len(body), 15)
        status, headers, body = self.request(path, {'Range': f'bytes={self.size}-'})
        self.assertEqual(status, 416); self.assertEqual(headers['Content-Range'], f'bytes */{self.size}')

    def test_root_guide_and_cross_batch_link(self):
        status, headers, _ = self.request('/')
        self.assertEqual(status, 302)
        self.assertEqual(headers['Location'], '/batch-02/Batch-02-Guide.html')
        status, _, body = self.request(headers['Location'])
        self.assertEqual(status, 200); self.assertIn(b'Watch the Batch 2 lecture', body)
        status, _, body = self.request('/batch-01/Batch-01-Guide.html')
        self.assertEqual(status, 200); self.assertIn(b'Watch the Batch 1 lecture', body)


if __name__ == '__main__':
    unittest.main()
