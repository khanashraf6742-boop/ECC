"""Reviewed, deterministic city-Hinglish romanisation, not an English translation.

Only Hindi words actually present in this edition are mapped. Unknown words fail
closed instead of silently emitting Devanagari or a guessed transliteration.
English legal terms, dates, numbers and punctuation are left untouched.
"""
import re

HINDI_WORDS = re.compile(r'[\u0900-\u097f]+')
PAIRS = '''
अकेले akele
अगले agle
अपने apne
अभी abhi
अलग alag
आए aaye
आएगा aayega
आज aaj
आता aata
आती aati
आते aate
आप aap
आया aaya
इस is
इससे isse
इसी isi
इसे ise
उस us
उसका uska
उसके uske
उसी usi
उसे use
एक ek
और aur
कई kai
कम kam
कर kar
करके karke
करता karta
करती karti
करते karte
करना karna
करने karne
करे kare
करेंगे karenge
करो karo
कहता kehta
का ka
काम kaam
किया kiya
किसी kisi
की ki
के ke
को ko
खुद khud
चलने chalne
चाहिए chahiye
चुकी chuki
जा ja
जाने jaane
जैसी jaisi
जो jo
तक tak
तो toh
था tha
दिखे dikhe
दूसरा doosra
दूसरे doosre
देखकर dekhkar
देखो dekho
देता deta
देती deti
देना dena
दो do
दोनों dono
दोबारा dobara
दौरान dauraan
न na
नया naya
नहीं nahi
ने ne
पढ़ो padho
पर par
पहले pehle
पुराना purana
पुराने purane
फिर phir
बनता banta
बनती banti
बना bana
बनाओ banao
बाकी baaki
बाद baad
बिना bina
बोलना bolna
बोले bole
बोलो bolo
भी bhi
मंजूर manzoor
मत mat
मतलब matlab
मानो maano
मिल mil
मिलता milta
मिलती milti
मिलने milne
मिला mila
मिलेगी milegi
में mein
यही yahi
या ya
ये yeh
रखो rakho
रहने rehne
लगता lagta
लगाओ lagao
लिए liye
लिया liya
ली li
लेकिन lekin
लो lo
लौटे laute
वजह wajah
वाला wala
वाली wali
वाले wale
वो woh
सकती sakti
सकते sakte
समझो samjho
सही sahi
साथ saath
सिर्फ sirf
से se
हटता hatta
हर har
हिसाब hisaab
हुआ hua
हुई hui
है hai
हैं hain
हो ho
हों hon
होंगी hongi
होंगे honge
होगा hoga
होगी hogi
होती hoti
होते hote
होना hona
होनी honi
होने hone
'''
WORD_MAP = dict(line.split() for line in PAIRS.strip().splitlines())


def romanize(text):
    def replace(match):
        word = match.group()
        if word not in WORD_MAP:
            raise ValueError(f'Unreviewed Hindi word in Roman captions: {word}')
        return WORD_MAP[word]
    return HINDI_WORDS.sub(replace, text)


def caption(cue):
    spoken = cue.get('spoken_text', cue['text'])
    return {**cue, 'spoken_text': spoken, 'text': romanize(spoken)}
