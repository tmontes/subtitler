import asyncio
import logging
import os

from . import audio
from . import transcribe
from . import translate

import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()


log = logging.getLogger(__package__)


def setup_logging():

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname).1s %(name)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )


async def async_main() -> None:

    audio_queue = asyncio.Queue()
    text_queue = asyncio.Queue()

    await asyncio.gather(
        audio.stream_input(audio_queue),
        transcribe.run(audio_queue, text_queue),
        translate.run(text_queue),
    )


def main():
    setup_logging()
    try:
        log.info('start')
        asyncio.run(async_main())
    except KeyboardInterrupt:
        log.info('interrupted')



if __name__ == '__main__':
    main()
