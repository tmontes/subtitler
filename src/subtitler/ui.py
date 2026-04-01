import asyncio
import itertools as it
import logging
import tkinter as tk


from . import config


log = logging.getLogger(__name__.split('.')[-1])


_CANVAS_NAME = 'subtitles'

_CANVAS_ITEMS = []
_BORDER = config.UI_FONT_BORDER
_TEXT_DELTAS = list(it.product((-_BORDER, 0, _BORDER), (-_BORDER, 0, _BORDER)))
_TEXT_DELTAS.remove((0, 0))


def _create_text(canvas: tk.Canvas, w: int, h: int, text: str) -> None:

    def canvas_create_text(*, color: str, dx: int, dy:int) -> int:
        return canvas.create_text(
            dx + w // 2,
            dy + h // 2,
            width=w - config.UI_H_PADDING,
            text=text,
            fill=color,
            font=config.UI_FONT,
            anchor='center',
        )

    for dx, dy in _TEXT_DELTAS:
        _CANVAS_ITEMS.append(
            canvas_create_text(color='black', dx=dx, dy=dy)
        )
    _CANVAS_ITEMS.append(
        canvas_create_text(color='white', dx=0, dy=0)
    )


def _update_text(root_window: tk.Tk, text: str) -> None:

    canvas = root_window.nametowidget(_CANVAS_NAME)
    for item_id in _CANVAS_ITEMS:
        canvas.itemconfig(item_id, text=text)
    root_window.update()



def create() -> tk.Tk:

    # transparent root window: works on macOS, other platforms need other "thingies"
    root_window = tk.Tk()
    root_window.overrideredirect(True)
    root_window.wm_attributes("-transparent", True)
    root_window.config(bg='systemTransparent')

    x = config.UI_H_PADDING
    y = root_window.winfo_screenheight() - config.UI_V_PADDING - config.UI_HEIGHT
    w = root_window.winfo_screenwidth() - config.UI_H_PADDING * 2
    h = config.UI_HEIGHT
    root_window.geometry(f'{w}x{h}+{x}+{y}')

    canvas = tk.Canvas(
        root_window,
        width=w,
        height=h,
        bg='systemTransparent',
        bd=0,
        highlightthickness=0,
        name=_CANVAS_NAME,
    )
    canvas.pack()

    _create_text(canvas, w, h, config.UI_HELLO)
    root_window.wm_attributes("-topmost", True)
    root_window.update()

    return root_window



async def run(root_window: tk.Tk, queue: asyncio.Queue) -> None:

    await asyncio.sleep(config.UI_HELLO_SECONDS)
    _update_text(root_window, '')

    while True:
        text = await queue.get()
        log.debug(f'{text=}')
        _update_text(root_window, text)
