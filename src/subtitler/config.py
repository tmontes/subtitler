# General

SPEECH_LANG = 'en-US'
SUBTITLE_LANG = 'pt-PT'


# DeepL
# -----

DL_LANG = SUBTITLE_LANG


# Deepgram
# --------
# https://developers.deepgram.com/reference/speech-to-text/listen-streaming

DG_MODEL = 'nova-3'
DG_ENCODING = 'linear16'
DG_SAMPLE_RATE = 48_000
DG_LANGUAGE = SPEECH_LANG


# Sounddevice
# -----------

SD_DTYPE = {
    'linear16': 'int16'
}[DG_ENCODING]

SD_SAMPLE_RATE = DG_SAMPLE_RATE
SD_BLOCK_SIZE = SD_SAMPLE_RATE // 10
