import logging
import os

import asyncio

import deepl


log = logging.getLogger(__name__.split('.')[-1])



async def run(queue: asyncio.Queue):

    client = deepl.DeepLClient(
        auth_key=os.environ['DEEPL_API_KEY'],
        send_platform_info=False,
    )

    log.info('starting')
    while True:
        transcription = await queue.get()
        result = await asyncio.to_thread(
            client.translate_text,
            transcription,
            target_lang='pt-PT',
        )
        print(f'\n{result.text}')
