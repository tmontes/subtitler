import asyncio
import sounddevice as sd

from . import reference as r


async def stream_input(queue: asyncio.Queue):

    loop = asyncio.get_event_loop()

    def push_audio(buffer, frames, time, status):
        loop.call_soon_threadsafe(
            queue.put_nowait,
            bytes(buffer),
        )

    with sd.RawInputStream(
        samplerate=r.SD_SAMPLE_RATE,
        dtype=r.SD_DTYPE,
        blocksize=2400,
        callback=push_audio,
    ):
        await asyncio.sleep(42)
