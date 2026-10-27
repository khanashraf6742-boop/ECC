"""Reviewed reversible words for Batch 2; no guessed transliteration or B1 changes."""
import re
from roman_subtitles import WORD_MAP as BATCH1_WORD_MAP

EXTRA = '''
अकेला akela
अच्छा achha
अंदर andar
आपके aapke
करती karti
कुछ kuch
खरीदी kharidi
घर ghar
घूमने ghoomne
चाहिये chahiye
जाते jaate
जाये jaaye
जोड़कर jodkar
जोड़ो jodo
जरूरी zaroori
बच्चे bachche
बढ़ा badha
बनाता banata
बनते bante
बंद band
बनकर bankar
बीच beech
भेजता bhejta
माँ maa
मिल mil
रहा raha
रहे rahe
रही rahi
रखो rakho
रहकर rehkar
रहना rehna
रहती rehti
लगेगी lagegi
लगेंगे lagenge
ले le
लेती leti
लेनी leni
लौटती lautti
वक़्त waqt
वही wahi
वहीं wahin
शादी shaadi
सारी saari
समझाइये samjhaiye
तब tab
थी thi
उसने usne
होगा hoga
होकर hokar
होता hota
बदल badal
अब ab
थे the
पास paas
पूरा poora
लिखा likha
गयी gayi
गये gaye
पढ़ padh
सकता sakta
'''
WORD_MAP = {**BATCH1_WORD_MAP, **dict(line.split() for line in EXTRA.strip().splitlines())}
# A single reviewed Hindi spelling per Roman word makes source -> speech -> caption reversible.
TO_HINDI = {roman: hindi for hindi, roman in WORD_MAP.items() if roman != 'use'}
# Here 'use' is the English verb, never the Hindi pronoun 'use/उसे'.


def spoken(text):
    return re.sub(r'\b[a-z]+\b', lambda m: TO_HINDI.get(m[0], m[0]), text)


def romanize(text):
    def replace(match):
        if match[0] not in WORD_MAP:
            raise ValueError('Unreviewed Batch 2 Hindi word: ' + match[0])
        return WORD_MAP[match[0]]
    return re.sub(r'[\u0900-\u097f]+', replace, text)
