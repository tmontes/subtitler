import asyncio
import logging

import sounddevice as sd

from . import reference as r


log = logging.getLogger(__name__.split('.')[-1])


async def stream_input(queue: asyncio.Queue):

    loop = asyncio.get_event_loop()

    def push_audio(buffer, frames, time, status):
        log.debug(f'pushing {len(buffer)} bytes')
        loop.call_soon_threadsafe(
            queue.put_nowait,
            bytes(buffer),
        )

    log.info('starting')
    with sd.RawInputStream(
        samplerate=r.SD_SAMPLE_RATE,
        dtype=r.SD_DTYPE,
        blocksize=2400,
        callback=push_audio,
    ):
        await asyncio.sleep(42)
