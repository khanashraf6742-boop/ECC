#!/usr/bin/env python3
"""Acoustically align the approved transcript and burn captions into the existing MP4.

No speech is regenerated in the deliverable. eSpeak is an alignment-only reference;
MFCC/DTW maps its phrase boundaries onto the actual soundtrack, chapter by chapter.
Usage: python build_subtitles.py [--align-only | --render-only]
The original MP4 is replaced atomically only after a complete successful decode.
"""
import argparse
import ctypes
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

from roman_subtitles import caption

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'video-work' / 'subtitles'
VIDEO = ROOT / 'batch-01-video.mp4'
REPORT = ROOT / 'subtitle-build-report.json'
STEM = ROOT / 'batch-01-video'
SCRIPT = ROOT / ('video-narration.json' if (ROOT / 'video-narration.json').exists() else 'narration.json')
SAMPLE_RATE = 16000
FRAME_STEP = .02


def split_phrases(text, limit=84):
    """Keep sentence punctuation and every spoken word; limit subtitle reading load."""
    phrases = []
    for sentence in re.split(r'(?<=[.!?])\s+', text.strip()):
        words = sentence.split()
        while words:
            count = 1
            while count < len(words) and len(' '.join(words[:count + 1])) <= limit:
                count += 1
            # Prefer a comma break, but never isolate a single short word.
            if count < len(words):
                commas = [i + 1 for i, word in enumerate(words[:count]) if word.endswith(',') and i >= 3]
                if commas and commas[-1] >= count // 2:
                    count = commas[-1]
            # Do not leave a one/two-word tail flashing in its own caption.
            if 0 < len(words) - count < 3 and count >= 6:
                count -= 3 - (len(words) - count)
            phrases.append(' '.join(words[:count]))
            words = words[count:]
    return phrases


def timestamp(seconds, vtt=False):
    milliseconds = round(seconds * 1000)
    hours, remainder = divmod(milliseconds, 3600000)
    minutes, remainder = divmod(remainder, 60000)
    secs, ms = divmod(remainder, 1000)
    return f'{hours:02}:{minutes:02}:{secs:02}{"." if vtt else ","}{ms:03}'


def ass_timestamp(seconds):
    centiseconds = round(seconds * 100)
    hours, remainder = divmod(centiseconds, 360000)
    minutes, remainder = divmod(remainder, 6000)
    secs, cs = divmod(remainder, 100)
    return f'{hours}:{minutes:02}:{secs:02}.{cs:02}'


class ReferenceSpeech:
    """Synchronous eSpeak NG API; the callback is kept alive for the entire session."""
    def __init__(self):
        import espeakng_loader
        import numpy as np
        self.np = np
        self.lib = espeakng_loader.load_library()
        self.lib.espeak_Initialize.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
        self.rate = self.lib.espeak_Initialize(2, 0, str(espeakng_loader.get_data_path()).encode(), 0)
        if self.rate <= 0:
            raise RuntimeError('Unable to initialize the bundled eSpeak NG library')
        callback_type = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(ctypes.c_short), ctypes.c_int, ctypes.c_void_p)
        self.parts = []

        def collect(samples, count, events):
            if samples and count:
                self.parts.append(np.ctypeslib.as_array(samples, shape=(count,)).copy())
            return 0

        self.callback = callback_type(collect)
        self.lib.espeak_SetSynthCallback.argtypes = [callback_type]
        self.lib.espeak_SetSynthCallback(self.callback)
        self.lib.espeak_SetVoiceByName.argtypes = [ctypes.c_char_p]
        if self.lib.espeak_SetVoiceByName(b'hi') != 0:
            raise RuntimeError('Hindi reference voice is unavailable')
        self.lib.espeak_SetParameter(1, 175, 0)  # words/minute
        self.lib.espeak_Synth.argtypes = [ctypes.c_char_p, ctypes.c_size_t, ctypes.c_uint,
                                         ctypes.c_int, ctypes.c_uint, ctypes.c_uint,
                                         ctypes.c_void_p, ctypes.c_void_p]

    def synthesize(self, text):
        self.parts = []
        encoded = text.encode('utf-8')
        status = self.lib.espeak_Synth(encoded, len(encoded) + 1, 0, 1, 0, 1 | 4096, None, None)
        self.lib.espeak_Synchronize()
        if status != 0 or not self.parts:
            raise RuntimeError(f'Alignment reference synthesis failed: {status}')
        from scipy.signal import resample_poly
        from math import gcd
        divisor = gcd(self.rate, SAMPLE_RATE)
        raw = self.np.concatenate(self.parts).astype('float64')
        return resample_poly(raw, SAMPLE_RATE // divisor, self.rate // divisor)


def decode_audio(ffmpeg, start, duration):
    import numpy as np
    command = [ffmpeg, '-v', 'error', '-ss', str(start), '-i', str(VIDEO),
               '-t', str(duration), '-vn', '-ac', '1', '-ar', str(SAMPLE_RATE),
               '-af', 'asetpts=N/SR/TB', '-f', 's16le', '-']
    return np.frombuffer(subprocess.check_output(command), dtype='<i2').astype('float64')


def features(signal):
    import numpy as np
    from python_speech_features import mfcc
    values = mfcc(signal, samplerate=SAMPLE_RATE, winlen=.05, winstep=FRAME_STEP,
                  numcep=13, nfilt=40, nfft=1024, appendEnergy=False)[:, 1:]
    # Cepstral mean/variance normalization reduces speaker and microphone differences.
    return (values - values.mean(axis=0)) / np.maximum(values.std(axis=0), 1e-6)


def align_chapter(ffmpeg, reference, segment, chapter):
    import numpy as np
    from scipy.spatial.distance import cdist
    from dtw import dtw
    phrases = split_phrases(segment['text'])
    pieces = [reference.synthesize(phrase) for phrase in phrases]
    boundaries = np.cumsum([0] + [len(piece) for piece in pieces]) / SAMPLE_RATE
    ref_features = features(np.concatenate(pieces))
    real_features = features(decode_audio(ffmpeg, chapter['start_seconds'],
                                         chapter['end_seconds'] - chapter['start_seconds']))
    distances = cdist(ref_features, real_features, metric='cosine')
    path = dtw(distances, step_pattern='symmetric2', keep_internals=False)
    # A boundary is mapped from the acoustic warp, never from text length/duration ratios.
    ref_frames, real_frames = np.asarray(path.index1), np.asarray(path.index2)
    mapped = []
    for boundary in boundaries:
        frame = min(round(boundary / FRAME_STEP), len(ref_features) - 1)
        selected = real_frames[ref_frames == frame]
        mapped.append(float(np.median(selected)) * FRAME_STEP)
    mapped[0] = 0.0
    mapped[-1] = chapter['end_seconds'] - chapter['start_seconds']
    cues = [{'chapter': chapter['number'], 'start': round(chapter['start_seconds'] + start, 3),
             'end': round(chapter['start_seconds'] + end, 3), 'text': phrase}
            for start, end, phrase in zip(mapped, mapped[1:], phrases)]
    # Very short spoken fragments remain with their neighbour instead of flashing.
    merged = []
    for cue in cues:
        if merged and (cue['end'] - cue['start'] < .55 or merged[-1]['end'] - merged[-1]['start'] < .55):
            previous = merged.pop()
            merged.append({**previous, 'end': cue['end'], 'text': previous['text'] + ' ' + cue['text']})
        else:
            merged.append(cue)
    if len(merged) > 1 and merged[0]['end'] - merged[0]['start'] < .55:
        first, second = merged[:2]
        merged = [{**first, 'end': second['end'], 'text': first['text'] + ' ' + second['text']}] + merged[2:]
    return merged, {'chapter': chapter['number'], 'dtw_normalized_distance': float(path.normalizedDistance),
                    'reference_seconds': round(boundaries[-1], 3), 'cue_count': len(merged)}


def wrap_caption(text):
    """Explicit two-line wrapping; preserve words and Devanagari grapheme clusters."""
    if len(text) <= 46:
        return text
    words = text.split()
    choices = [(' '.join(words[:i]), ' '.join(words[i:])) for i in range(1, len(words))]
    left, right = min(choices, key=lambda pair: abs(len(pair[0]) - len(pair[1])))
    return left + '\n' + right


def write_caption_files(cues):
    srt, vtt = [], ['WEBVTT\n']
    ass = ['[Script Info]', 'ScriptType: v4.00+', 'PlayResX: 1920', 'PlayResY: 1080',
           'WrapStyle: 2', 'ScaledBorderAndShadow: yes', '', '[V4+ Styles]',
           'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, '
           'Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, '
           'Alignment, MarginL, MarginR, MarginV, Encoding',
           'Style: Default,Atkinson Hyperlegible,40,&H00FFFFFF,&H00FFFFFF,&H00111B26,&H00111B26,'
           '0,0,0,0,100,100,0,0,1,1,0,2,110,110,12,1', '', '[Events]',
           'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text']
    for index, cue in enumerate(cues, 1):
        text = wrap_caption(cue['text'])
        srt.append(f'{index}\n{timestamp(cue["start"])} --> {timestamp(cue["end"])}\n{text}\n')
        vtt.append(f'{index}\n{timestamp(cue["start"], True)} --> {timestamp(cue["end"], True)}\n{text}\n')
        if any(char in text for char in '{}\\'):
            raise ValueError('ASS control characters are not allowed in narration')
        ass.append(f'Dialogue: 0,{ass_timestamp(cue["start"])},{ass_timestamp(cue["end"])},Default,,0,0,0,,'
                   + text.replace('\n', r'\N'))
    for extension, lines in [('srt', srt), ('vtt', vtt), ('ass', ass)]:
        STEM.with_suffix('.' + extension).write_text('\n'.join(lines).rstrip('\n') + '\n', encoding='utf-8')


def audio_digest(ffmpeg, video):
    return subprocess.check_output([ffmpeg, '-v', 'error', '-i', str(video), '-map', '0:a:0',
                                    '-c:a', 'copy', '-f', 'hash', '-hash', 'sha256', '-'], text=True).strip()


def render(ffmpeg, report):
    target = WORK / 'captioned.mp4'
    (WORK / 'fonts').mkdir(exist_ok=True)
    shutil.copyfile(ROOT / 'video-fonts' / 'AtkinsonHyperlegible-Regular.ttf', WORK / 'fonts' / 'AtkinsonHyperlegible-Regular.ttf')
    # All slides remain visible: scale the entire frame into a 936px-high teaching area.
    # The remaining 144px are an opaque caption band, not an overlay on legal text.
    filters = ('scale=1664:936,pad=1920:1080:128:0:color=0x111b26,'
               "ass=batch-01-video.ass:fontsdir=video-work/subtitles/fonts")
    source_hash = audio_digest(ffmpeg, VIDEO)
    subprocess.run([ffmpeg, '-hide_banner', '-y', '-i', str(VIDEO),
                    '-map', '0:v:0', '-map', '0:a:0', '-map_metadata', '0', '-map_chapters', '0',
                    '-metadata', 'title=CCS LTC Batch 1 - Important dates and GIDs - Roman Hinglish',
                    '-metadata', 'comment=Roman-Hinglish phrase captions. Dates and GID opening; original ten core chapters retained.',
                    '-vf', filters, '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '22',
                    '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart', str(target)], cwd=ROOT, check=True)
    subprocess.run([ffmpeg, '-v', 'error', '-xerror', '-i', str(target), '-map', '0:v:0',
                    '-map', '0:a:0', '-f', 'null', '-'], check=True)
    if audio_digest(ffmpeg, target) != source_hash:
        raise RuntimeError('The captioned video must preserve the original AAC bitstream')
    report.update({'full_decode_check': 'passed', 'audio_stream_unchanged': True,
                   'audio_sha256': source_hash, 'burned_in': True, 'embedded_mov_text': False,
                   'video_bytes': target.stat().st_size})
    target.replace(VIDEO)
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    video_report_path = ROOT / 'video-build-report.json'
    video_report = json.loads(video_report_path.read_text())
    video_report.update({'bytes': VIDEO.stat().st_size, 'subtitles': {
        'burned_in': True, 'embedded_track': None, 'srt': 'batch-01-video.srt',
        'vtt': 'batch-01-video.vtt', 'report': REPORT.name, 'caption_band_height': 144},
        'note': 'Dates/GID opening and original core narration; AAC unchanged during caption pass. Roman-Hinglish captions. '
                'Phrase captions acoustically aligned within sixteen chapter boundaries.'})
    video_report_path.write_text(json.dumps(video_report, ensure_ascii=False, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--align-only', action='store_true')
    group.add_argument('--render-only', action='store_true')
    args = parser.parse_args()
    import imageio_ffmpeg
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    WORK.mkdir(parents=True, exist_ok=True)
    video_report = json.loads((ROOT / 'video-build-report.json').read_text())
    if video_report.get('subtitles', {}).get('burned_in'):
        raise RuntimeError('Video already captioned. Restore the clean pre-caption MP4 and video-build-report.json first.')
    if not args.render_only:
        segments = json.loads(SCRIPT.read_text())
        chapters = json.loads((ROOT / 'video-build-report.json').read_text())['chapters']
        reference = ReferenceSpeech()
        cues, audit = [], []
        for segment, chapter in zip(segments, chapters, strict=True):
            aligned, metrics = align_chapter(ffmpeg, reference, segment, chapter)
            cues.extend(caption(cue) for cue in aligned)
            audit.append(metrics)
            print(f'Chapter {chapter["number"]}: {len(aligned)} acoustic phrase cues', flush=True)
        report = {'source_script_sha256': hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),
                  'alignment': 'chapter-local MFCC / dynamic time warping against eSpeak NG reference speech',
                  'frame_step_seconds': FRAME_STEP, 'source_script_file': SCRIPT.name,
                  'language': 'Roman-script city Hinglish; reviewed transliteration, not English translation',
                  'timing_precision_note': 'Automatic phrase-level acoustic alignment, not certified word-level timing.',
                  'full_decode_check': 'not rendered', 'chapters': audit, 'cues': cues}
        write_caption_files(cues)
        REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    if not args.align_only:
        report = json.loads(REPORT.read_text())
        if report.get('burned_in'):
            raise RuntimeError('Video already captioned. Restore the clean pre-caption MP4 before rendering again.')
        render(ffmpeg, report)


if __name__ == '__main__':
    main()
