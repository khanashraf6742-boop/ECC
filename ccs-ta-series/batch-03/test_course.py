#!/usr/bin/env python3
"""Offline structure, source-caution, caption, review and HTTP-range checks.

Run: python3 -m unittest -v test_course
These tests do not certify legal completeness or human-verbatim accuracy.
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

import build_batch_03 as lecture
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
        m = re.fullmatch(r'(\d\d:\d\d:\d\d\.\d{3}) --> (\d\d:\d\d:\d\d\.\d{3})(.*)', lines[1])
        if not m:
            raise AssertionError('Invalid cue timing: ' + lines[1])
        cues.append((m[1], m[2], m[3], ' '.join(lines[2:])))
    return raw, cues


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.tags = [], [], []
    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        self.tags.append(tag)
        if 'id' in values: self.ids.append(values['id'])
        for attr in ('href', 'src'):
            if attr in values: self.links.append(values[attr])


class LessonTests(unittest.TestCase):
    def test_lesson_schema_examples_and_voice(self):
        data=lecture.load_data(); lecture.audit(data)
        self.assertEqual(data['speaker'], 'voice-00 (user selected)')
        self.assertEqual(len(data['sections']),10)
        self.assertEqual(sum(len(s['beats']) for s in data['sections']),20)
        for sec in data['sections']:
            for beat in sec['beats']:
                self.assertEqual(len(beat['lines']),len(beat['english_lines']))
                self.assertTrue(all(len(l)<=76 for l in beat['lines']))
                for field in ('rule','example','trap','key'): self.assertTrue(beat[field])
        broken=deepcopy(data);broken['sections'][0]['beats'][0]['example']=''
        with self.assertRaises(SystemExit): lecture.audit(broken)

    def test_fifty_sourced_units_each_have_example(self):
        text=(ROOT/'Batch-03-Guide.md').read_text(encoding='utf-8')
        parts=re.split(r'(?m)^### (\d+) — [^\n]+\n',text)
        units={int(parts[i]):parts[i+1] for i in range(1,len(parts),2)}
        self.assertEqual(sorted(units),list(range(1,51)))
        for number,unit in units.items():
            with self.subTest(unit=number):
                self.assertRegex(unit,r'\[S\d+\]')
                self.assertIn('**Example:',unit)
        self.assertEqual(len(re.findall(r'^\[S\d+\]: https?://',text,re.M)),23)
        self.assertIn('not** obtain an authenticated original',units[27])
        self.assertIn('₹350',units[27])
        self.assertIn('60 days',units[37]);self.assertIn('180 days',units[38]);self.assertIn('15 days',units[42])
        self.assertIn('due for payment',units[37]);self.assertIn('not the next-day filing deadline',units[37])
        self.assertIn('not the filing deadline',lecture.load_data()['sections'][8]['beats'][0]['example'])
        self.assertIn('not forfeited',units[44]);self.assertIn('two outstanding',units[45])
        self.assertIn('₹600',units[8]);self.assertIn('₹896',units[21]);self.assertIn('₹15/km',units[16])
        self.assertIn('beyond available extraction',text)
        self.assertIn('not exhaustively audited',text.lower())
        self.assertIn('human-verbatim',text.lower())

    def test_correction_and_open_topics_are_visible(self):
        d=lecture.load_data()['sections'];text=(ROOT/'Batch-03-Guide.md').read_text(encoding='utf-8')
        self.assertIn('Vande Bharat',d[0]['beats'][1]['rule'])
        self.assertIn('Humsafar',d[0]['beats'][1]['rule'])
        self.assertIn('Shatabdi',text);self.assertIn('Rajdhani',text)
        self.assertIn('not been re-rendered',text)
        self.assertIn('not retrieved',str(d[5]['beats'][1]['cards']).lower())
        self.assertIn('not authenticated',text.lower())
        self.assertTrue((ROOT/'audio/source-06-original.mp3').is_file())
        self.assertIn('sentence',d[5]['caption_note'])
        self.assertIn('number',d[3]['caption_note'])
        for n in ('01','02'):
            md=(ROOT.parent/f'batch-{n}'/f'Batch-{n}-Guide.md').read_text(encoding='utf-8')
            self.assertIn('Batch 3 correction to earlier video',md)
            self.assertIn('not been re-rendered',md)
            html=(ROOT.parent/f'batch-{n}'/f'Batch-{n}-Guide.html').read_text(encoding='utf-8')
            self.assertIn('Batch 3 correction to earlier video',html)
            self.assertIn('not been re-rendered',html)

    def test_script_transliteration_and_edit_provenance(self):
        data=lecture.load_data();script=(ROOT/'Narration-hi.txt').read_text(encoding='utf-8')
        dic=json.loads((ROOT/'notes/roman-hindi.json').read_text(encoding='utf-8'))
        self.assertIn('not a certified transcript',script)
        self.assertIn('Section 06 removes',script)
        self.assertIn('ORIGINAL SYNTHESIS INPUT:',script)
        for s in data['sections']:
            lines=lecture.section_tts_text(s)
            self.assertIn(lines,script)
            self.assertIsNone(re.search(r'[\u0900-\u097f]',lecture.romanize_hinglish(lines,dic)))
            if 'synthesis_input' in s:self.assertIn(s['synthesis_input'],script)

    def test_alignment_timeline_and_stale_data_rejection(self):
        data,a=lecture.load_data(),lecture.load_alignment()
        dur=[x['duration'] for x in a['sections']]
        timeline,captions,total=lecture.build_timeline(data,dur,a)
        self.assertEqual(len(timeline),20);self.assertEqual(len(captions),92)
        self.assertTrue(345<total<346,(total,))
        self.assertLessEqual(captions[-1][1],total)
        for before,after in zip(captions,captions[1:]):self.assertLessEqual(before[1],after[0]+.001)
        stale=deepcopy(a);stale['sections'][0]['audio_sha256']='wrong'
        with self.assertRaisesRegex(ValueError,'audio changed'):lecture.build_timeline(data,dur,stale)
        stale=deepcopy(a);stale['sections'][0]['script_sha256']='wrong'
        with self.assertRaisesRegex(ValueError,'narration text changed'):lecture.build_timeline(data,dur,stale)
        stale=deepcopy(a);stale['sections'][0]['cues'][0]['text']+=' extra'
        with self.assertRaisesRegex(ValueError,'different source cues'):lecture.translated_captions(data,stale)

    def test_vtt_tracks_match_timeline_and_are_roman(self):
        data,a=lecture.load_data(),lecture.load_alignment()
        _,cues,_=lecture.build_timeline(data,[x['duration'] for x in a['sections']],a)
        en=lecture.translated_captions(data,a)
        dic=json.loads((ROOT/'notes/roman-hindi.json').read_text(encoding='utf-8'))
        enraw,envtt=read_vtt('Captions-en.vtt'); rraw,rvtt=read_vtt('Captions-roman.vtt')
        for raw in (enraw,rraw):
            self.assertTrue(raw.startswith('WEBVTT\n'))
            self.assertIsNone(re.search(r'[\u0900-\u097f]',raw))
            self.assertIn('human',raw.lower());self.assertIn('automatic',raw.lower())
        self.assertIn('translation',enraw.lower());self.assertIn('transliteration',rraw.lower())
        self.assertEqual(len(cues),len(envtt));self.assertEqual(len(cues),len(rvtt))
        for i,((start,end,spoken),translation) in enumerate(zip(cues,en)):
            with self.subTest(cue=i+1):
                times=(lecture.stamp(start),lecture.stamp(end))
                self.assertEqual(envtt[i][:2],times);self.assertEqual(rvtt[i][:2],times)
                self.assertEqual(envtt[i][3],translation)
                self.assertEqual(rvtt[i][3],lecture.romanize_hinglish(spoken,dic))
                self.assertIn('line:0%',envtt[i][2])

    def test_number_group_cues(self):
        line='word '*13+'two thousand kilo remaining'
        section={'beats':[{'lines':[line]},{'lines':['end']}]}
        words=lambda text:[{'text':w,'start':i*.2,'end':i*.2+.15} for i,w in enumerate(text.split())]
        blocks=[{'beat':1,'words':words(line)},{'beat':2,'words':[{'text':'end','start':9,'end':10}]}]
        cues=align_captions.make_cues(section,blocks)
        self.assertTrue(any('two thousand' in c['text'] for c in cues))
        self.assertFalse(any(c['text'].endswith(' two') for c in cues))

    def test_recognition_hashes_bind_every_current_clip(self):
        d,a=lecture.load_data(),lecture.load_alignment()
        b=json.loads((ROOT/'notes/asr-review.json').read_text(encoding='utf-8'))
        w=json.loads((ROOT/'notes/whole-audio-review.json').read_text(encoding='utf-8'))
        self.assertIn('UNEDITED AUTOMATIC',b['disclosure'])
        self.assertEqual(len(b['sections']),10);self.assertEqual(len(w['sections']),10)
        for sec,aligned,block,full in zip(d['sections'],a['sections'],b['sections'],w['sections']):
            digest=hashlib.sha256((ROOT/'audio'/sec['audio']).read_bytes()).hexdigest()
            self.assertEqual(digest,aligned['audio_sha256'])
            self.assertEqual(digest,block['audio_sha256'])
            self.assertEqual(digest,full['audio_sha256'])
            self.assertEqual(' '.join(x['text'] for x in aligned['words']),lecture.section_tts_text(sec))

    def test_review_page_hashes_and_vtt_validation(self):
        page=(ROOT/'Caption-Review.html').read_text(encoding='utf-8')
        match=re.search(r'const source=(\{[^\n]+\});',page);self.assertIsNotNone(match)
        j=json.loads(match.group(1))
        self.assertEqual(j['video_sha256'],hashlib.sha256((ROOT/'Batch-03-Lecture.mp4').read_bytes()).hexdigest())
        self.assertEqual(j['caption_sha256'],hashlib.sha256((ROOT/'Captions-roman.vtt').read_bytes()).hexdigest())
        self.assertEqual(j['cues'],build_review.parse_vtt((ROOT/'Captions-roman.vtt').read_text(encoding='utf-8')))
        self.assertEqual(len(j['cues']),92)
        self.assertIn('I listened and checked this cue',page)
        self.assertIn('not yet human-verified',page.lower())
        for bad in ('','WEBVTT\n\n1\n00:00:02.000 --> 00:00:01.000\ntext',
                    'WEBVTT\n\n1\n00:00:00.000 --> 00:00:02.000\nx\n\n2\n00:00:01.000 --> 00:00:03.000\ny'):
            with self.subTest(bad=bad),self.assertRaises(ValueError):build_review.parse_vtt(bad)

    def test_html_disclosure_accessibility_and_local_links(self):
        html=(ROOT/'Batch-03-Guide.html').read_text(encoding='utf-8')
        check=(ROOT/'Caption-Check.md').read_text(encoding='utf-8')
        for content in (html,check):
            self.assertIn('automatic',content.lower());self.assertIn('human',content.lower());self.assertIn('verbatim',content.lower())
        self.assertIn('burned-in Roman-Hinglish',html)
        self.assertIn('Caption-Review.html',html)
        self.assertIn('aria-label',html);self.assertIn('Skip to the companion guide',html)
        parser=LinkParser();parser.feed(html);self.assertEqual(len(parser.ids),len(set(parser.ids)))
        for link in parser.links:
            with self.subTest(link=link):
                if link.startswith('#'):self.assertIn(unquote(link[1:]),parser.ids)
                elif not urlparse(link).scheme:self.assertTrue((ROOT/unquote(link)).is_file(),link)
        self.assertNotIn('http://localhost',html)


class QuietHandler(CourseHandler):
    def log_message(self,*_args):pass

class RangeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),QuietHandler)
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()
        cls.port=cls.server.server_port;cls.video=ROOT/'Batch-03-Lecture.mp4';cls.size=cls.video.stat().st_size
    @classmethod
    def tearDownClass(cls):cls.server.shutdown();cls.server.server_close();cls.thread.join()
    def request(self,path,headers=None):
        c=HTTPConnection('127.0.0.1',self.port,timeout=5);c.request('GET',path,headers=headers or {})
        r=c.getresponse();result=r.status,dict(r.getheaders()),r.read();c.close();return result
    def test_seek_ranges_suffix_and_invalid(self):
        p='/batch-03/Batch-03-Lecture.mp4'
        status,h,body=self.request(p,{'Range':'bytes=20-29'});self.assertEqual(status,206)
        self.assertEqual(h['Content-Range'],f'bytes 20-29/{self.size}')
        with self.video.open('rb') as source:source.seek(20);self.assertEqual(body,source.read(10))
        status,h,body=self.request(p,{'Range':'bytes=-15'});self.assertEqual(status,206);self.assertEqual(len(body),15)
        status,h,body=self.request(p,{'Range':f'bytes={self.size}-'});self.assertEqual(status,416)
        self.assertEqual(h['Content-Range'],f'bytes */{self.size}')
    def test_root_guide_and_cross_batch(self):
        status,h,_=self.request('/');self.assertEqual(status,302)
        self.assertEqual(h['Location'],'/batch-03/Batch-03-Guide.html')
        status,_,body=self.request(h['Location']);self.assertEqual(status,200);self.assertIn(b'Watch the Batch 3 lecture',body)
        status,_,body=self.request('/batch-02/Batch-02-Guide.html');self.assertEqual(status,200);self.assertIn(b'Batch 3 correction',body)

if __name__=='__main__':unittest.main()
