"""Batch 5 acceptance tests, authored before its implementation."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent

class Content(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import build_batch5 as b
        cls.b = b
        cls.cards, cls.scripts = b.content()

    def test_exact_coverage_once(self):
        self.assertEqual(len(self.cards), 55)
        self.assertEqual([u['card_id'] for s in self.scripts for u in s['units']], [c['id'] for c in self.cards])
        for c in self.cards:
            for key in ('ref','title','spoken_ref_roman','rule','explanation_roman','example_roman','trap','source'):
                self.assertTrue(c[key], (c['id'],key))
            for source in c['source'].split(';'):
                self.assertIn(source, self.b.SOURCES)

    def test_voice_and_language_budget(self):
        from batch5_roman import spoken, romanize
        self.assertEqual(len(self.scripts), 9)
        self.assertEqual(self.scripts[0]['voice'], 'voice-01')
        self.assertTrue(all(s['voice']=='voice-00' for s in self.scripts[1:]))
        for s in self.scripts:
            self.assertLessEqual(len(s['text']),1500)
            self.assertEqual(romanize(s['text']),s['roman_text'])
            self.assertIsNone(re.search('[\u0900-\u097f]',s['roman_text']))
        self.assertIn('Important dates', self.scripts[0]['roman_text'])
        self.assertIn('Aaj ',self.scripts[0]['text'])
        with self.assertRaisesRegex(ValueError, 'Unreviewed'):
            romanize('ज्ञात')

    def test_legal_corrections_are_explicit(self):
        alltext=' '.join(c['rule']+' '+c['trap'] for c in self.cards)
        for term in ('two Home Town','second two-year','unused','that four-year','forgone','2024–25','31 December 2026','NIL','30 June 2005','outward'):
            self.assertIn(term,alltext)
        self.assertIn('not',self.cards[21]['rule'])
        self.assertIn('NCR',self.cards[32]['ref'])
        self.assertIn('not',self.cards[33]['rule'])
        self.assertIn('eighth',self.cards[41]['rule'])

    def test_tables_all_rows_and_footnotes(self):
        from batch5_tables import TABLES
        self.assertEqual([t['number'] for t in TABLES], [1,2,3,4,5])
        self.assertTrue(all(t['rows'] and t['notes'] for t in TABLES))
        data=json.dumps(TABLES,ensure_ascii=False)
        for term in ('1 September 2016','31 December 2015','1 January 2025','31 August 2017','30 December 2016','2033','2034–37','forgone','2024–45','2025'):
            self.assertIn(term,data)
        for n in (3,4,5):
            self.assertGreaterEqual(len(TABLES[n-1]['rows']),10)

    def test_documents(self):
        self.b.documents(self.cards)
        for suffix in ('md','html'):
            text=(ROOT/f'batch-05.{suffix}').read_text()
            for c in self.cards:
                self.assertIn(c['id'],text)
            for n in range(1,6):
                self.assertIn(f'Table {n}',text)
            self.assertNotRegex(text,r'<script\b')
        self.assertGreater((ROOT/'batch-05.pdf').stat().st_size,10000)

    def test_all_layouts_and_partition(self):
        from PIL import Image
        from build_batch5_video import slide, opening, parts, merge_readable
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x.png'
            for c in self.cards:
                audit=slide(c,p)
                self.assertGreaterEqual(min(audit['body_font_sizes']),26)
                with Image.open(p) as image:
                    self.assertEqual(image.size,(1920,1080))
                    self.assertEqual(image.getpixel((960,1000)),(17,27,38))
            for kind in ('OPEN-LEGAL','OPEN-PRACTICAL'):
                self.assertEqual(opening(kind,p)['caption_band_height'],144)
        for s in self.scripts:
            self.assertEqual(' '.join(t for _,t in parts(s)).split(),s['text'].split())
        self.assertEqual(len(merge_readable([dict(start=0,end=.2,text='Example,'),dict(start=.2,end=3,text='normal words.')])),1)
        with self.assertRaisesRegex(ValueError,'too fast'):
            merge_readable([dict(start=0,end=.1,text='too many words')])
        with self.assertRaisesRegex(ValueError,'unreadably long'):
            merge_readable([dict(start=0,end=.8,text='word '*35),dict(start=.8,end=1.6,text='word '*35)])

    def test_preserve_earlier_deliveries(self):
        result=subprocess.run(['git','diff','7774ac7','--name-only','--','docs/ccs-ltc/batch-0[1-4]*','docs/ccs-ltc/build_batch[1-4]*','docs/ccs-ltc/batch[1-4]_*.py','docs/ccs-ltc/test_batch[1-4].py'],cwd=ROOT.parents[1],capture_output=True,text=True,check=True)
        self.assertEqual(result.stdout,'')

class Media(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=json.loads((ROOT/'batch-05-video-report.json').read_text())
        cls.sub=json.loads((ROOT/'batch-05-subtitle-report.json').read_text())

    def test_actual_1080p_and_full_decode(self):
        r=self.report
        self.assertEqual((r['width'],r['height']),(1920,1080))
        self.assertEqual(r['full_decode_check'],'passed')
        self.assertGreater(r['duration_seconds'],600)
        self.assertEqual(r['embedded_chapter_check'],'passed')
        self.assertEqual(len(r['chapters']),9)
        self.assertEqual(len(r['pages']),57)
        self.assertEqual(r['bytes'],(ROOT/'batch-05-video.mp4').stat().st_size)
        self.assertTrue(self.sub['audio_stream_unchanged'])

    def test_cues_match_spoken_transcript_and_are_readable(self):
        scripts=json.loads((ROOT/'batch-05-narration.json').read_text())
        cues=self.sub['cues']
        self.assertEqual(' '.join(s['roman_text'] for s in scripts).split(),' '.join(c['text'] for c in cues).split())
        previous=0
        for c in cues:
            self.assertGreaterEqual(c['start'],previous-.001)
            self.assertGreater(c['end'],c['start'])
            self.assertLessEqual(len(c['text'])/(c['end']-c['start']),35.01)
            self.assertIsNone(re.search('[\u0900-\u097f]',c['text']))
            previous=c['end']
        for ext in ('srt','vtt','ass'):
            text=(ROOT/f'batch-05-video.{ext}').read_text()
            self.assertIsNone(re.search('[\u0900-\u097f]',text))
        for p in self.report['pages']:
            self.assertGreater(p['end_seconds'],p['start_seconds'])

class Guardrails(unittest.TestCase):
    def test_script_rejects_missing_clauses(self):
        import build_batch5 as b
        from unittest.mock import patch
        with patch.object(b,'GROUPS',[(1,55)]), self.assertRaisesRegex(ValueError,'exactly once'):
            b.content()

    def test_script_rejects_service_budget_excess(self):
        import build_batch5 as b
        from unittest.mock import patch
        with patch.object(b,'INTRO','x'*1501), self.assertRaisesRegex(ValueError,'budget'):
            b.content()

    def test_script_rejects_nonreversible_caption(self):
        import build_batch5 as b
        from unittest.mock import patch
        with patch.object(b,'romanize',lambda text:'different'), self.assertRaisesRegex(ValueError,'round-trip'):
            b.content()

    def test_mapper_keeps_english_use_and_informal_style(self):
        from batch5_roman import spoken,romanize
        self.assertEqual(spoken('All India use karo.'),'All India use करो.')
        for s in json.loads((ROOT/'batch-05-narration.json').read_text()):
            self.assertFalse(any(w in s['text'] for w in ('रियायत','प्रतिपूर्ति','कार्मिक')))
            self.assertEqual(romanize(spoken(s['roman_text'])),s['roman_text'])

    def test_document_main(self):
        import build_batch5 as b
        b.main()

    def test_register_idempotent_and_prior_pointers_preserved(self):
        import csv,io
        from unittest.mock import patch
        import build_batch5 as b
        previous=subprocess.check_output(['git','show','7774ac7:docs/ccs-ltc/gid-coverage-register.csv'],cwd=ROOT.parents[1],text=True)
        baseline=list(csv.DictReader(io.StringIO(previous)))
        with tempfile.TemporaryDirectory() as d,patch.object(b,'ROOT',Path(d)):
            p=Path(d)/'gid-coverage-register.csv'
            p.write_text(previous)
            b.register()
            first=p.read_bytes()
            b.register()
            self.assertEqual(first,p.read_bytes())
            rows={r['id']:r for r in csv.DictReader(p.open())}
            self.assertEqual(len(rows),122)
            for r in baseline:
                self.assertIn(r['video_card'],rows[r['id']]['video_card'])
                self.assertEqual(r['coverage_status'],rows[r['id']]['coverage_status'])
            self.assertEqual(rows['10.1']['coverage_status'],'excluded-from-current-instruction')
            for ident in ('M-2025-FAQ','M-2025-GUIDE'):
                self.assertIn('partial',rows[ident]['coverage_status'])
            self.assertEqual(rows['M-2015-HQNCR']['coverage_status'],'covered-in-batch-5')

    def test_missing_selected_voice_clip_is_an_error(self):
        import build_batch5_video as v
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as d,patch.object(v,'WORK',Path(d)):
            with self.assertRaisesRegex(FileNotFoundError,'selected voice'):
                v.prepare_audio('not-run',[dict(file='missing.mp3')])

    def test_caption_rejects_ass_control_and_overwidth(self):
        import build_batch5_video as v
        from unittest.mock import patch
        with self.assertRaisesRegex(ValueError,'control character'):
            v.captions([dict(start=0,end=2,text='bad {override}')])
        with patch.object(v.acoustic,'wrap_caption',lambda t:t):
            with self.assertRaisesRegex(ValueError,'safe width'):
                v.captions([dict(start=0,end=2,text='W'*300)])

    def test_alignment_rejects_changed_transcript(self):
        import build_batch5_video as v
        from unittest.mock import patch
        s=json.loads((ROOT/'batch-05-narration.json').read_text())[1]
        with patch.object(v.acoustic,'split_phrases',lambda *a,**k:['wrong']):
            with self.assertRaisesRegex(ValueError,'changed the transcript'):
                v.align('not-run',None,s,{})

    def test_renderer_rejects_zero_time_card(self):
        import build_batch5_video as v
        with self.assertRaisesRegex(ValueError,'positive display'):
            v.render_raw('not-run',[dict(id='B5-01',start_seconds=1)], [dict(end_seconds=1)],[])

    def test_final_rejects_changed_audio(self):
        import build_batch5_video as v
        from unittest.mock import patch
        with patch.object(v,'run'),patch.object(v.acoustic,'audio_digest',side_effect=['a','b']):
            with self.assertRaisesRegex(ValueError,'AAC bitstream'):
                v.final('not-run',Path('raw'),[],[],{})

    def test_final_rejects_bad_metadata(self):
        import build_batch5_video as v
        from unittest.mock import patch
        def reader(*a,**k):
            yield dict(size=(1280,720),duration=3)
        with patch.object(v,'run'),patch.object(v.acoustic,'audio_digest',return_value='a'),patch.object(v.imageio_ffmpeg,'read_frames',reader):
            with self.assertRaisesRegex(ValueError,'metadata'):
                v.final('not-run',Path('raw'),[dict(end_seconds=3)],[],{})

    def test_actual_hashes_chapters_and_faststart(self):
        import imageio_ffmpeg,struct
        from build_subtitles import audio_digest
        r=json.loads((ROOT/'batch-05-video-report.json').read_text())
        sub=json.loads((ROOT/'batch-05-subtitle-report.json').read_text())
        scripts=json.loads((ROOT/'batch-05-narration.json').read_text())
        digest=hashlib.sha256((ROOT/'batch-05-narration.json').read_bytes()).hexdigest()
        self.assertEqual(digest,r['source_script_sha256'])
        self.assertEqual(digest,sub['source_script_sha256'])
        self.assertEqual(audio_digest(imageio_ffmpeg.get_ffmpeg_exe(),ROOT/'batch-05-video.mp4'),sub['audio_sha256'])
        for chapter,s in zip(r['chapters'],scripts,strict=True):
            self.assertEqual(chapter['source_text_sha256'],hashlib.sha256(s['text'].encode()).hexdigest())
        atoms=[]
        with (ROOT/'batch-05-video.mp4').open('rb') as f:
            offset=0
            while offset<r['bytes']:
                f.seek(offset)
                size,kind=struct.unpack('>I4s',f.read(8))
                if size==1:
                    size=struct.unpack('>Q',f.read(8))[0]
                if size==0:
                    size=r['bytes']-offset
                self.assertGreaterEqual(size,8)
                atoms.append(kind)
                offset+=size
        self.assertLess(atoms.index(b'moov'),atoms.index(b'mdat'))

    def test_pdf_all_cards_tables_no_devanagari_and_safe_bounds(self):
        import fitz
        pdf=fitz.open(ROOT/'batch-05.pdf')
        text=' '.join(p.get_text() for p in pdf)
        for i in range(1,56):
            self.assertIn(f'B5-{i:02}',text)
        for i in range(1,6):
            self.assertIn(f'Table {i}',text)
        self.assertNotRegex(text,'[\u0900-\u097f]')
        for page in pdf:
            for block in page.get_text('dict')['blocks']:
                if block['type']!=0:
                    continue
                for line in block['lines']:
                    for span in line['spans']:
                        x0,y0,x1,y1=span['bbox']
                        self.assertGreaterEqual(x0,35)
                        self.assertLessEqual(x1,page.rect.width-35)
                        self.assertGreaterEqual(y0,35)
                        self.assertLessEqual(y1,page.rect.height-15)

if __name__=='__main__':
    unittest.main()
