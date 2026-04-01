import asyncio

from deepgram import AsyncDeepgramClient
from deepgram.core.events import EventType
from deepgram.listen.v1.types import (
    ListenV1Results,
    ListenV1Metadata,
    ListenV1UtteranceEnd,
    ListenV1SpeechStarted,
)

from . import reference as r


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


def handle_message(message: ListenV1Response) -> None:

    match message:
        case ListenV1Results():
            is_final = message.is_final
            transcript = message.channel.alternatives[0].transcript
            if transcript:
                print(f'{is_final=} {transcript=}')
        case _:
            print(f'unhandled: {message=}')


async def run(queue: asyncio.Queue):

    client = AsyncDeepgramClient()
    async with client.listen.v1.connect(
        model=r.DG_MODEL,
        encoding=r.DG_ENCODING,
        sample_rate=r.DG_SAMPLE_RATE,
        language=r.DG_LANGUAGE,
        punctuate='true',
    ) as connection:


        connection.on(EventType.OPEN, lambda _: print("Connection opened"))
        connection.on(EventType.MESSAGE, handle_message)
        connection.on(EventType.CLOSE, lambda _: print("Connection closed"))
        connection.on(EventType.ERROR, lambda error: print(f"Caught: {error}"))

        # Helper task
        audio_sender_task = asyncio.create_task(audio_sender(connection, queue))
        print('Audio now running...')

        # Start listening
        print('start listening...')
        await connection.start_listening()
        print('done listening...')
