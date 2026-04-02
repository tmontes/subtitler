import asyncio
import logging

from deepgram import AsyncDeepgramClient
from deepgram.core.events import EventType
from deepgram.listen.v1.socket_client import AsyncV1SocketClient
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



async def audio_sender(connection: AsyncV1SocketClient, audio_queue: asyncio.Queue) -> None:

    log.info('audio sender starting')
    while True:
        audio_buffer = await audio_queue.get()
        await connection.send_media(audio_buffer)



def handle_message(message: ListenV1Response, text_queue: asyncio.Queue) -> None:

    match message:
        case ListenV1Results():
            # TODO: do we need to handle `message.is_final`?
            transcript = message.channel.alternatives[0].transcript
            if transcript:
                # don't send empty strings
                text_queue.put_nowait(transcript)
        case _:
            log.error(f'unhandled: {message=}')



async def run(audio_queue: asyncio.Queue, text_queue: asyncio.Queue) -> None:

    log.info('starting')
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

        # must keep a reference to the task object to prevent garbage collection
        # see https://docs.python.org/3/library/asyncio-task.html#asyncio.create_task
        _audio_sender_task = asyncio.create_task(audio_sender(connection, audio_queue))

        log.info('starting listening')
        await connection.start_listening()
        log.info('done listening')
