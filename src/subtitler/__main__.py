import asyncio
import os

from . import audio
from . import transcribe

import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()


async def async_main() -> None:

    audio_queue = asyncio.Queue()

    await asyncio.gather(
        audio.stream_input(audio_queue),
        transcribe.run(audio_queue),
    )


def main():
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        print('interrupted')



if __name__ == '__main__':
    main()