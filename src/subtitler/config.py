# General

SPEECH_LANG = 'en-US'
SUBTITLE_LANG = 'pt-PT'

UI_HEIGHT = 210
UI_H_PADDING = 64
UI_V_PADDING = 32

UI_FONT = ('Helvetica', 64, 'bold')
UI_FONT_BORDER = 3

UI_SECONDS_MIN = 2
UI_SECONDS_MAX = 7
UI_CHARACTERS_PER_SECOND = 15

UI_HELLO = 'subtitler ready'


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
