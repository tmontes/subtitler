import asyncio
import logging
import os
import tkinter as tk

import certifi

# motivation: maybe the Python installation has no certificate store available
os.environ['SSL_CERT_FILE'] = certifi.where()

from . import audio
from . import transcribe
from . import translate
from . import ui



log = logging.getLogger(__package__)



def setup_logging() -> None:

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname).1s %(name)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    logging.getLogger('deepl').setLevel(logging.WARNING)



async def async_main(root_window: tk.Tk) -> None:

    audio_queue = asyncio.Queue()
    text_queue = asyncio.Queue()
    ui_queue = asyncio.Queue()

    await asyncio.gather(
        audio.stream_input(audio_queue),
        transcribe.run(audio_queue, text_queue),
        translate.run(text_queue, ui_queue),
        ui.run(root_window, ui_queue),
    )



def main() -> None:

    setup_logging()
    root_window = ui.create()

    try:
        log.info('start')
        asyncio.run(async_main(root_window))
    except KeyboardInterrupt:
        log.info('interrupted')



if __name__ == '__main__':
    main()
