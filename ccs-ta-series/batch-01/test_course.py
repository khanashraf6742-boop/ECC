#!/usr/bin/env python3
"""Offline checks for the Batch 1 course. Run: python3 -m unittest -v test_course"""
from copy import deepcopy
from datetime import date, timedelta
from html.parser import HTMLParser
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from pathlib import Path
import hashlib
import json
import re
import threading
import unittest
from urllib.parse import unquote, urlparse

import build_batch_01 as lecture
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
            raise AssertionError(f'Invalid WebVTT timing: {lines[1]}')
        cues.append((match.group(1), match.group(2), match.group(3), ' '.join(lines[2:])))
    return raw, cues


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if 'id' in values:
            self.ids.append(values['id'])
        for attr in ('href', 'src'):
            if attr in values:
                self.links.append(values[attr])


class LessonTests(unittest.TestCase):
    def test_schema_and_missing_example(self):
        data = lecture.load_data()
        lecture.audit(data)
        broken = deepcopy(data)
        broken['sections'][0]['beats'][0]['example'] = ''
        with self.assertRaises(SystemExit):
            lecture.audit(broken)
        self.assertEqual(len(data['sections']), 21)
        self.assertEqual(sum(len(section['beats']) for section in data['sections']), 42)

    def test_alignment_keeps_spoken_numbers_together(self):
        prefix = 'word ' * 13
        line = prefix + 'two thousand kilo remaining'
        section = {'beats': [{'lines': [line]}, {'lines': ['end']}]}
        def words(text):
            return [{'text': word, 'start': i * .2, 'end': i * .2 + .15}
                    for i, word in enumerate(text.split())]
        blocks = [{'beat': 1, 'words': words(line)},
                  {'beat': 2, 'words': [{'text': 'end', 'start': 9, 'end': 10}]}]
        cues = align_captions.make_cues(section, blocks)
        self.assertTrue(any('two thousand' in cue['text'] for cue in cues))
        self.assertFalse(any(cue['text'].endswith(' two') for cue in cues))

    def test_2026_da_and_regional_transfer_exception(self):
        data = lecture.load_data()
        section = next(s for s in data['sections'] if s['audio'] == 'ta-updated-rates-transfer-effects.mp3')
        self.assertIn('60%', section['beats'][0]['rule'])
        self.assertIn('Rs 62.50 per km', section['beats'][0]['example'])
        self.assertIn('one-third', section['beats'][1]['rule'])
        self.assertIn('specified regions', section['beats'][1]['trap'])
        self.assertIn('not reopened', section['beats'][1]['key'])

    def test_2023_train_update_and_ta_air_booking(self):
        data = lecture.load_data()
        beat = data['sections'][4]['beats'][1]
        self.assertIn('VANDE BHARAT', str(beat['cards']))
        self.assertIn('HUMSAFAR', str(beat['cards']))
        self.assertIn('Rajdhani', beat['rule'])
        self.assertIn('Vande Bharat', beat['example'])
        air = next(s for s in data['sections'] if s['audio'] == 'ta-tour-air-booking.mp3')
        self.assertIn('16 Jun 2022', air['source'])
        self.assertIn('Official tour', lecture.section_tts_text(air))
        self.assertIn('seventy two hours', lecture.section_tts_text(air))
        # The comparison material remains in the guide, not the TA-focused lecture.
        self.assertFalse(any('ltc-faq' in s['audio'] for s in data['sections']))
        self.assertTrue(any('ta-food' in s['audio'] for s in data['sections']))

    def test_city_hinglish_script_is_preserved(self):
        data = lecture.load_data()
        saved = (ROOT / 'Narration-hi.txt').read_text(encoding='utf-8')
        self.assertIn('CITY HINGLISH NARRATION SCRIPT', saved)
        for section in data['sections']:
            with self.subTest(section=section['title']):
                self.assertIn(lecture.section_tts_text(section), saved)
        train_script = lecture.section_tts_text(data['sections'][4])
        self.assertIn('Vande Bharat', train_script)
        self.assertIn('Humsafar', train_script)

    def test_timeline_and_date_arithmetic(self):
        data = lecture.load_data()
        alignment = lecture.load_alignment()
        durations = [chapter['duration'] for chapter in alignment['sections']]
        timeline, captions, total = lecture.build_timeline(data, durations, alignment)
        self.assertEqual(len(timeline), 42)
        self.assertGreater(len(captions), 297)
        self.assertGreater(total, 1090.84)
        self.assertLessEqual(captions[-1][1], total)
        for left, right in zip(captions, captions[1:]):
            self.assertLessEqual(left[1], right[0] + .001)
        self.assertEqual(lecture.stamp(3723.456), '01:02:03.456')
        self.assertEqual(date(2026, 10, 1) + timedelta(days=60), date(2026, 11, 30))
        self.assertEqual(date(2026, 10, 1) + timedelta(days=180), date(2027, 3, 30))

    def test_both_subtitle_files_match_the_aligned_timeline(self):
        data = lecture.load_data()
        alignment = lecture.load_alignment()
        durations = [chapter['duration'] for chapter in alignment['sections']]
        _, captions, _ = lecture.build_timeline(data, durations, alignment)
        translations = lecture.translated_captions(data, alignment)
        dictionary = json.loads((ROOT / 'notes' / 'roman-hindi.json').read_text(encoding='utf-8'))
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
            with self.subTest(cue=i + 1):
                expected_times = (lecture.stamp(start), lecture.stamp(end))
                self.assertEqual(en[i][:2], expected_times)
                self.assertEqual(roman[i][:2], expected_times)
                self.assertEqual(en[i][3], translated)
                self.assertEqual(roman[i][3], lecture.romanize_hinglish(source, dictionary))
                self.assertIn('line:0%', en[i][2])
                self.assertNotIn('line:5%', roman[i][2])

    def test_stale_alignment_and_translation_are_rejected(self):
        data = lecture.load_data()
        alignment = lecture.load_alignment()
        durations = [chapter['duration'] for chapter in alignment['sections']]
        stale = deepcopy(alignment)
        stale['sections'][0]['audio_sha256'] = 'outdated'
        with self.assertRaisesRegex(ValueError, 'audio changed'):
            lecture.build_timeline(data, durations, stale)
        stale = deepcopy(alignment)
        stale['sections'][0]['script_sha256'] = 'outdated'
        with self.assertRaisesRegex(ValueError, 'narration text changed'):
            lecture.build_timeline(data, durations, stale)
        stale = deepcopy(alignment)
        stale['sections'][0]['cues'][0]['end'] = durations[0] + 1
        with self.assertRaisesRegex(ValueError, 'invalid or overlapping'):
            lecture.build_timeline(data, durations, stale)
        stale = deepcopy(alignment)
        stale['sections'][0]['cues'][0]['text'] += ' extra'
        with self.assertRaisesRegex(ValueError, 'different source cues'):
            lecture.translated_captions(data, stale)

    def test_audio_check_evidence_matches_current_clips(self):
        data = lecture.load_data()
        alignment = lecture.load_alignment()
        review = json.loads((ROOT / 'notes' / 'asr-review.json').read_text(encoding='utf-8'))
        self.assertIn('UNEDITED AUTOMATIC', review['disclosure'])
        self.assertEqual(len(review['sections']), len(data['sections']))
        for section, timed, checked in zip(data['sections'], alignment['sections'], review['sections']):
            with self.subTest(audio=section['audio']):
                self.assertEqual(section['audio'], checked['audio'])
                self.assertEqual(timed['audio_sha256'], checked['audio_sha256'])
                self.assertEqual(' '.join(w['text'] for w in timed['words']), lecture.section_tts_text(section))
        by_audio = {s['audio']: s for s in review['sections']}
        def recognized(name):
            return ' '.join(s['text'] for b in by_audio[name]['blocks'] for s in b['segments']).lower()
        self.assertIn('new rules', recognized('02-dates-and-safeguard.mp3'))
        self.assertIn('new table', recognized('02-dates-and-safeguard.mp3'))
        self.assertIn('technical resignation', recognized('15-technical-resignation.mp3'))
        whole = json.loads((ROOT / 'notes' / 'whole-audio-review.json').read_text(encoding='utf-8'))
        whole_names = {entry['audio'] for entry in whole['sections']}
        self.assertEqual(whole_names, {s['audio'] for s in data['sections']})
        for entry in whole['sections']:
            self.assertEqual(entry['audio_sha256'], hashlib.sha256((ROOT / 'audio' / entry['audio']).read_bytes()).hexdigest())

    def test_all_guide_units_have_sources_examples_and_cautions(self):
        text = (ROOT / 'Batch-01-Guide.md').read_text(encoding='utf-8')
        parts = re.split(r'(?m)^### (\d+)\. [^\n]+\n', text)
        units = {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}
        self.assertEqual(sorted(units), list(range(1, 85)))
        for number, unit in units.items():
            with self.subTest(unit=number):
                self.assertIn('**Source:**', unit)
                self.assertTrue('**Example' in unit or '| Example |' in unit)
                self.assertIn('**Trap.', unit)
        self.assertIn('₹2,812.50', units[32])
        self.assertIn('₹1,250', units[33])
        self.assertIn('₹422.50', units[35])
        self.assertIn('exactly twelve hours', units[39])
        self.assertIn('₹600', units[40])
        self.assertIn('₹30/km and ₹15/km', units[43])
        self.assertIn('₹40,000', units[46])
        self.assertIn('receipts/vouchers', units[48].lower())
        self.assertIn('2022', units[48])
        self.assertIn('₹2,287.50', units[50])
        self.assertIn('First Class', units[72])
        self.assertIn('Bunk', units[74])
        self.assertIn('family does not accompany', units[75])
        self.assertIn('not mandatory', units[75])
        self.assertIn('re-employing office/organisation pays both', units[76])
        self.assertIn('retiring organisation pays the joining TA', units[77])
        self.assertIn('re-employing organisation pays the admissible TA after completion', units[77])
        self.assertIn('middle/second-class', units[73])
        self.assertIn('₹62.50', units[78])
        self.assertIn('₹31.25', units[78])
        self.assertIn('₹18.75', units[78])
        self.assertIn('DoPT', units[79])
        self.assertIn('non-representational', units[84])
        self.assertIn('2017 master OM concordance', text)
        self.assertIn('5 June 2024', text)
        self.assertIn('shortest route', units[57])
        self.assertIn('not entitled to air travel', units[57])
        self.assertIn('not below Joint Secretary', units[58])
        self.assertIn('FAQ 71', units[58])
        self.assertIn('14 January 2025', units[68])
        self.assertIn('100 km each way', units[69])
        self.assertIn('medical certificate', units[70])
        self.assertIn('no fare reimbursement is claimed for the entire LTC journey', units[71])
        self.assertIn('not yet', text.lower())

    def test_caption_limits_and_optional_track_are_disclosed(self):
        notes = (ROOT / 'Narration-hi.txt').read_text(encoding='utf-8')
        explanation = (ROOT / 'Caption-Check.md').read_text(encoding='utf-8')
        html = (ROOT / 'Batch-01-Guide.html').read_text(encoding='utf-8')
        for text in (notes, explanation, html):
            with self.subTest(text=text[:32]):
                self.assertIn('automatic', text.lower())
                self.assertIn('human', text.lower())
                self.assertIn('verbatim', text.lower())
        self.assertIn('burned-in Roman-Hinglish', html)
        self.assertIn('Captions-en.vtt', html)
        self.assertIn('Captions-roman.vtt', html)
        self.assertIn('Caption-Review.html', html)
        self.assertNotIn('Captions-hi.vtt', html)
        review = (ROOT / 'Caption-Review.html').read_text(encoding='utf-8')
        self.assertIn('localStorage', review)
        self.assertIn('Export review', review)
        self.assertIn('not yet human-verified', review.lower())

    def test_review_player_is_bound_to_media_and_rejects_bad_cues(self):
        page = (ROOT / 'Caption-Review.html').read_text(encoding='utf-8')
        payload = re.search(r'const source=(\{[^\n]+\});', page)
        self.assertIsNotNone(payload)
        source = json.loads(payload.group(1))
        self.assertEqual(source['video_sha256'], hashlib.sha256((ROOT / 'Batch-01-Lecture.mp4').read_bytes()).hexdigest())
        self.assertEqual(source['caption_sha256'], hashlib.sha256((ROOT / 'Captions-roman.vtt').read_bytes()).hexdigest())
        parsed = build_review.parse_vtt((ROOT / 'Captions-roman.vtt').read_text(encoding='utf-8'))
        self.assertEqual(source['cues'], parsed)
        self.assertGreater(len(parsed), 297)
        self.assertIn('reviewed:false', page)
        self.assertIn('I listened and checked this cue', page)
        for bad in ('', 'WEBVTT\n\n1\n00:00:02.000 --> 00:00:01.000\ntext',
                    'WEBVTT\n\n1\n00:00:00.000 --> 00:00:02.000\nx\n\n2\n00:00:01.000 --> 00:00:03.000\ny'):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                build_review.parse_vtt(bad)

    def test_html_local_links_and_anchors(self):
        parser = LinkParser()
        parser.feed((ROOT / 'Batch-01-Guide.html').read_text(encoding='utf-8'))
        self.assertEqual(len(parser.ids), len(set(parser.ids)), 'duplicate HTML id')
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
        cls.thread.start()
        cls.port = cls.server.server_port
        cls.video = ROOT / 'Batch-01-Lecture.mp4'
        cls.size = cls.video.stat().st_size

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def request(self, path, headers=None):
        conn = HTTPConnection('127.0.0.1', self.port, timeout=5)
        conn.request('GET', path, headers=headers or {})
        response = conn.getresponse()
        result = response.status, dict(response.getheaders()), response.read()
        conn.close()
        return result

    def test_byte_range_and_suffix(self):
        status, headers, body = self.request('/Batch-01-Lecture.mp4', {'Range': 'bytes=20-29'})
        self.assertEqual(status, 206)
        self.assertEqual(headers['Content-Range'], f'bytes 20-29/{self.size}')
        self.assertEqual(headers['Content-Type'], 'video/mp4')
        with self.video.open('rb') as source:
            source.seek(20)
            self.assertEqual(body, source.read(10))
        status, headers, body = self.request('/Batch-01-Lecture.mp4', {'Range': 'bytes=-15'})
        self.assertEqual(status, 206)
        self.assertEqual(len(body), 15)
        self.assertEqual(headers['Content-Range'], f'bytes {self.size - 15}-{self.size - 1}/{self.size}')

    def test_invalid_range_and_guide(self):
        status, headers, body = self.request('/')
        self.assertEqual(status, 302)
        self.assertEqual(headers['Location'], '/Batch-01-Guide.html')
        self.assertEqual(body, b'')
        status, headers, body = self.request('/Batch-01-Lecture.mp4', {'Range': f'bytes={self.size}-'})
        self.assertEqual(status, 416)
        self.assertEqual(headers['Content-Range'], f'bytes */{self.size}')
        self.assertEqual(body, b'')
        status, _, body = self.request('/Batch-01-Guide.html')
        self.assertEqual(status, 200)
        self.assertIn(b'Watch the Batch 1 lecture', body)


if __name__ == '__main__':
    unittest.main()
