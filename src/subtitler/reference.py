# Deepgram
# --------
# https://developers.deepgram.com/reference/speech-to-text/listen-streaming

DG_MODEL = 'nova-3'
DG_ENCODING = 'linear16'
DG_SAMPLE_RATE = 48_000
DG_LANGUAGE = 'en-US' # 'pt-PT'


# Sounddevice
# -----------

SD_DTYPE = {
    'linear16': 'int16'
}[DG_ENCODING]

SD_SAMPLE_RATE = DG_SAMPLE_RATE
