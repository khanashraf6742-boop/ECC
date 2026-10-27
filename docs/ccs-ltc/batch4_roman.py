"""Reviewed reversible words for Batch 4; no guessed transliteration or B1 changes."""
import re
from batch3_roman import WORD_MAP as PREVIOUS_WORD_MAP

EXTRA = '''
दें dein
अपनी apni
बार baar
चले chale
छोड़ chhod
घूमा ghooma
ही hi
करें karein
खरीदे khareede
किए kiye
कोई koi
लगाए lagaye
लेना lena
लिखे likhe
लिखो likho
मिलेंगी milengi
मिलनी milni
सीधा seedha
ऊपर upar
उसको usko
वापस wapas
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
            raise ValueError('Unreviewed Batch 4 Hindi word: ' + match[0])
        return WORD_MAP[match[0]]
    return re.sub(r'[\u0900-\u097f]+', replace, text)
