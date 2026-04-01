import asyncio
import logging
import os

import deepl

from . import config


log = logging.getLogger(__name__.split('.')[-1])



async def run(text_queue: asyncio.Queue, ui_queue: asyncio.Queue):

    client = deepl.DeepLClient(
        auth_key=os.environ['DEEPL_API_KEY'],
        send_platform_info=False,
    )

    log.info('starting')
    while True:
        transcription = await text_queue.get()
        if transcription == '':
            # pass it along: cleans up the UI
            translated = ''
        else:
            # TODO: could we do better? more context, for example?
            result = await asyncio.to_thread(
                client.translate_text,
                transcription,
                target_lang=config.DL_LANG,
            )
            translated = result.text
        log.debug(f'sending {translated=}')
        await ui_queue.put(translated)
