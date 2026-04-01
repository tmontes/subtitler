import asyncio
import logging

import sounddevice as sd

from . import config


log = logging.getLogger(__name__.split('.')[-1])


async def stream_input(queue: asyncio.Queue):

    loop = asyncio.get_event_loop()

    def push_audio(buffer, _frames, _time, status):
        if status:
            log.warning(f'{status=}')
        log.debug(f'pushing {len(buffer)}')
        loop.call_soon_threadsafe(
            queue.put_nowait,
            bytes(buffer),
        )

    log.info('starting')
    with sd.RawInputStream(
        samplerate=config.SD_SAMPLE_RATE,
        dtype=config.SD_DTYPE,
        blocksize=config.SD_BLOCK_SIZE,
        callback=push_audio,
    ):
        while True:
            await asyncio.sleep(42)
