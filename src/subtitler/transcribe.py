import asyncio
import logging

from deepgram import AsyncDeepgramClient
from deepgram.core.events import EventType
from deepgram.listen.v1.types import (
    ListenV1Results,
    ListenV1Metadata,
    ListenV1UtteranceEnd,
    ListenV1SpeechStarted,
)

from . import config


log = logging.getLogger(__name__.split('.')[-1])


ListenV1Response = (
    ListenV1Results | ListenV1Metadata | ListenV1UtteranceEnd | ListenV1SpeechStarted
)



async def audio_sender(connection, queue):

    while True:
        audio_buffer = await queue.get()
        await connection.send_media(audio_buffer)

    # # Send control messages
    # await connection.send_keep_alive()
    # await connection.send_finalize()
    # await connection.send_close_stream()


def handle_message(message: ListenV1Response, text_queue: asyncio.Queue) -> None:

    match message:
        case ListenV1Results():
            # TODO: do we need to handle `message.is_final`?
            transcript = message.channel.alternatives[0].transcript
            # send transcripts even if empty strings: cleans up the UI
            text_queue.put_nowait(transcript)
        case _:
            log.error(f'unhandled: {message=}')


async def run(audio_queue: asyncio.Queue, text_queue: asyncio.Queue):

    client = AsyncDeepgramClient()
    async with client.listen.v1.connect(
        model=config.DG_MODEL,
        encoding=config.DG_ENCODING,
        sample_rate=config.DG_SAMPLE_RATE,
        language=config.DG_LANGUAGE,
        punctuate='true',
    ) as connection:


        connection.on(EventType.OPEN, lambda _: log.info('connected'))
        connection.on(EventType.MESSAGE, lambda m: handle_message(m, text_queue))
        connection.on(EventType.CLOSE, lambda _: log.info('disconnected'))
        connection.on(EventType.ERROR, lambda err: log.error(f'{err}'))

        _audio_sender_task = asyncio.create_task(audio_sender(connection, audio_queue))
        log.info('audio sender running')

        log.info('listening')
        await connection.start_listening()
        log.info('done listening')
