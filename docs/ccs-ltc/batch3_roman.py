"""Reviewed reversible words for Batch 3; no guessed transliteration or B1 changes."""
import re
from batch2_roman import WORD_MAP as PREVIOUS_WORD_MAP

EXTRA = '''
आई aayi
अपना apna
बदली badli
बाहर bahar
बनेगा banega
बस bas
भेजे bheje
भेजी bheji
बोलकर bolkar
चारों chaaron
चाहता chahta
चुका chuka
दे de
दी di
दूर door
हुए hue
जा jaa
जाकर jaakar
जाता jaata
जगह jagah
जिस jis
उनकी unki
जाओ jao
कभी kabhi
कहाँ kahan
करेगा karega
करेगी karegi
कहकर kehkar
क्या kya
लिखकर likhkar
लिखने likhne
मिलेगा milega
नाम naam
रहते rehte
उनका unka
वहाँ wahan
'''
WORD_MAP = {**PREVIOUS_WORD_MAP, **dict(line.split() for line in EXTRA.strip().splitlines())}
# A single reviewed Hindi spelling per Roman word makes source -> speech -> caption reversible.
TO_HINDI = {roman: hindi for hindi, roman in WORD_MAP.items() if roman != 'use'}
# Here 'use' is the English verb, never the Hindi pronoun 'use/उसे'.


def spoken(text):
    return re.sub(r'\b[a-z]+\b', lambda m: TO_HINDI.get(m[0], m[0]), text)


def romanize(text):
    def replace(match):
        if match[0] not in WORD_MAP:
            raise ValueError('Unreviewed Batch 3 Hindi word: ' + match[0])
        return WORD_MAP[match[0]]
    return re.sub(r'[\u0900-\u097f]+', replace, text)
