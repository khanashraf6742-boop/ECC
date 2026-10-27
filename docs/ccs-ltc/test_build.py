"""Content-contract and generated-artifact checks; no network or TTS required."""
import csv
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).parent


class ContentTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / 'batch-01.json').read_text())

    def test_every_card_has_an_immediate_example_and_reference(self):
        cards = self.data['cards']
        self.assertEqual(len(cards), 30)
        self.assertEqual(len({c['id'] for c in cards}), len(cards))
        sources = {s['id'] for s in self.data['sources']}
        for card in cards:
            for key in ('ref', 'title', 'rule', 'explanation', 'example', 'trap', 'status'):
                self.assertTrue(card[key].strip(), (card['id'], key))
            self.assertTrue(card['example'].startswith('Hypothetical'))
            self.assertIn(card['source'], sources)

    def test_every_clause_and_proviso_has_an_anchor(self):
        refs = '\n'.join(c['ref'] for c in self.data['cards'])
        for ref in ['Rule 1(1)', 'Rule 1(2)', 'Rule 2(2)', 'Rule 3']:
            self.assertIn(ref, refs)
        for clause in ('i', 'ii', 'iii', 'iv'):
            self.assertIn(f'Rule 1(3)({clause})', refs)
        for clause in 'abcdefg':
            self.assertIn(f'Rule 1(4)({clause})', refs)
        for limb in ['categories', 'completed service', 'certification', 'Hometown limb', 'Any Place in India limb']:
            self.assertIn('Rule 2(1): ' + limb, refs)
        for limb in ['conditions', 'proviso', 'official illustration']:
            self.assertIn('Rule 2(3): ' + limb, refs)

    def test_roadmap_maps_chapters_once_and_all_appendices(self):
        chapters = [n for b in self.data['batches'] for n in b['chapters']]
        self.assertEqual(sorted(chapters), list(range(1, 81)))
        with (ROOT / 'source-inventory.csv').open() as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 108)
        self.assertEqual(sorted(int(r['number']) for r in rows if r['kind'] == 'appendix'), list(range(1, 29)))
        self.assertEqual(sorted(int(r['number']) for r in rows if r['kind'] == 'chapter'), list(range(1, 81)))
        self.assertTrue(all('Pending' in b['status'] for b in self.data['batches'][1:]))

    def test_voice_script_within_per_call_budget(self):
        segments = json.loads((ROOT / 'narration.json').read_text())
        self.assertLessEqual(len(segments), 10)
        for segment in segments:
            self.assertLessEqual(len(segment['text']), 1500)
            self.assertIn(segment['voice'], {'voice-00', 'voice-01'})
        self.assertGreater((ROOT / 'batch-01-hinglish.mp3').stat().st_size, 10000)

    def test_each_card_is_spoken_once_with_reference_then_example(self):
        segments = json.loads((ROOT / 'narration.json').read_text())
        units = [unit for segment in segments for unit in segment['units']]
        self.assertEqual([u['card_id'] for u in units], [c['id'] for c in self.data['cards']])
        expected = [
            'Rule one, sub rule one.', 'Rule one, sub rule two.',
            'Rule one, sub rule three, opening words.',
            *[f'Rule one, sub rule three, clause Roman {n}.' for n in ('one', 'two', 'three', 'four')],
            *[f'Rule one, sub rule four, clause {letter}.' for letter in 'ABCDEFG'],
            *[f'Rule two, sub rule one, {part}.' for part in ('covered categories', 'completed service condition', 'certification condition', 'Hometown duration condition', 'Any Place in India duration condition')],
            'Rule two, sub rule two.',
            'Rule two, sub rule three, immediate re employment and continuity.',
            'Rule two, sub rule three, provided that condition, also called the proviso.',
            'Rule two, sub rule three, official illustration.',
            'Rule three, employee coverage.',
            'Rule three, family coverage, read with Rule four, clause D.',
            'Rule three, cross reference to Rules nine and eleven, and the July first, twenty twenty five FAQ, question six.',
            'September third, twenty twenty five DoPT Guidelines, applicability Note one.',
            'September third, twenty twenty five DoPT Guidelines, applicability Note two.',
            'September third, twenty twenty five DoPT Guidelines, paragraph two.',
            'Batch one teaching checklist, not a separate legal rule.',
        ]
        self.assertEqual([u['spoken_ref'] for u in units], expected)
        for unit, card in zip(units, self.data['cards']):
            self.assertEqual(unit['legal_ref'], card['ref'])
            self.assertTrue(unit['explanation'])
            self.assertTrue(unit['example'])
        for segment in segments[1:]:
            expected_text = ' '.join(
                u['spoken_ref'] + ' ' + u['explanation'] + ' Example, ' + u['example'] + (' ' + u['caution'] if u['caution'] else '')
                for u in segment['units']
            )
            self.assertEqual(segment['text'], expected_text)
        # Rule 2(1) has no separately lettered clauses: topic labels must not invent them.
        rule_two_units = [u for u in units if u['legal_ref'].startswith('Rule 2(1)')]
        self.assertEqual(len(rule_two_units), 5)
        self.assertTrue(all('clause' not in u['spoken_ref'] for u in rule_two_units))

    def test_city_hinglish_audio_avoids_formal_hindi(self):
        segments = json.loads((ROOT / 'narration.json').read_text())
        text = '\n'.join(s['text'] for s in segments)
        for word in ('उदाहरण', 'प्रावधान', 'अवधि', 'पात्रता', 'अनुमोदन', 'अधिसूचना', 'कीजिए', 'मानिए', 'समझिए', 'उन्नीस', 'छब्बीस', 'सत्ताईस', 'उनतीस'):
            self.assertNotIn(word, text)
        self.assertIn('city Hinglish', text)
        self.assertIn('Example', text)
        self.assertIn('joining', text)
        self.assertIn('twenty twenty six', text)

    def test_correction_and_open_items_are_explicit(self):
        duration_cards = [c for c in self.data['cards'] if 'limb' in c['ref']]
        self.assertEqual(len(duration_cards), 2)
        self.assertTrue(all('joining' in c['rule'] for c in duration_cards))
        self.assertTrue(any(c['status'] == 'text-checked-date-pending' for c in self.data['cards']))
        self.assertIn('not officially authenticated', (ROOT / 'REVIEW-NOTES.md').read_text().lower())

    def test_generated_outputs_are_safe_and_complete(self):
        spec = importlib.util.spec_from_file_location('ltc_build', ROOT / 'build.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as directory:
            module.build(ROOT, Path(directory))
            html = (Path(directory) / 'batch-01.html').read_text()
            md = (Path(directory) / 'batch-01.md').read_text()
            with (Path(directory) / 'spoken-reference-map.csv').open() as handle:
                reference_map = list(csv.DictReader(handle))
        self.assertEqual([row['card_id'] for row in reference_map], [card['id'] for card in self.data['cards']])
        for row in reference_map:
            self.assertIn(row['spoken_ref'], html)
            self.assertIn(row['spoken_ref'], md)
            self.assertIn(int(row['audio_chapter']), range(2, 11))
        for card in self.data['cards']:
            self.assertIn('id="' + card['id'] + '"', html)
            self.assertIn(card['ref'], md)
            self.assertLess(md.index(card['explanation']), md.index(card['example']))
        self.assertIn('data:audio/mpeg;base64,', html)
        self.assertNotIn('<script src=', html)
        self.assertIn('Condensed Hinglish audio', html)
        self.assertIn('original Gazette', md)
        self.assertIn('Source register', md)
        self.assertIn('prefers-reduced-motion', html)
        self.assertIn('aria-live="polite"', html)


if __name__ == '__main__':
    unittest.main()
