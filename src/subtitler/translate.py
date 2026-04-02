import asyncio
import logging
import os

import deepl

from . import config



log = logging.getLogger(__name__.split('.')[-1])



async def run(text_queue: asyncio.Queue, ui_queue: asyncio.Queue) -> None:

    log.info('starting')
    client = deepl.DeepLClient(
        auth_key=os.environ['DEEPL_API_KEY'],
        send_platform_info=False,
    )

    while True:
        transcription = await text_queue.get()
        # TODO: could we do better? more context, for example?
        result = await asyncio.to_thread(
            client.translate_text,
            transcription,
            target_lang=config.DL_LANG,
        )
        if isinstance(result, list):
            translated = result[0].text if result else ''
            log.warning(f'non-unique? {result=}')
        else:
            translated = result.text
        log.debug(f'sending {translated=}')
        await ui_queue.put(translated)
