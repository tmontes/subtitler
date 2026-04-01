import os

import asyncio

import deepl



async def run(queue: asyncio.Queue):

    client = deepl.DeepLClient(
        auth_key=os.environ['DEEPL_API_KEY'],
        send_platform_info=False,
    )

    while True:
        transcription = await queue.get()
        result = await asyncio.to_thread(
            client.translate_text,
            transcription,
            target_lang='pt-PT',
        )
        print(f'\n{result.text}\n')
