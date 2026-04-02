import asyncio
import itertools as it
import logging
import tkinter as tk

from . import config



log = logging.getLogger(__name__.split('.')[-1])



_CANVAS_WIDGET_NAME = 'subtitles'
_CANVAS_TEXT_ITEMS = []
_FAKE_OUTLINE_DELTAS = list(it.product(
    (-config.UI_FONT_BORDER, 0, config.UI_FONT_BORDER),
    (-config.UI_FONT_BORDER, 0, config.UI_FONT_BORDER)),
)
_FAKE_OUTLINE_DELTAS.remove((0, 0))



def _create_subtitle_widget(canvas: tk.Canvas, w: int, h: int, text: str) -> None:

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

    # fake black outline: same text, shifted +/- delta_x and delta_y
    for dx, dy in _FAKE_OUTLINE_DELTAS:
        _CANVAS_TEXT_ITEMS.append(canvas_create_text(color='black', dx=dx, dy=dy))
    # white text over the black shifted text instances
    _CANVAS_TEXT_ITEMS.append(canvas_create_text(color='white', dx=0, dy=0))



def _update_subtitle_text(root_window: tk.Tk, text: str) -> None:

    canvas = root_window.nametowidget(_CANVAS_WIDGET_NAME)
    for item_id in _CANVAS_TEXT_ITEMS:
        canvas.itemconfig(item_id, text=text)
    root_window.update()



def _cleanup_subtitle_text(root_window: tk.Tk) -> None:

    return _update_subtitle_text(root_window, text='')



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
        name=_CANVAS_WIDGET_NAME,
    )
    canvas.pack()

    _create_subtitle_widget(canvas, w, h, '')
    root_window.wm_attributes("-topmost", True)
    root_window.update()

    return root_window



def _schedule_cleanup(loop, root_window, text):

    hold_duration = min(
        config.UI_SECONDS_MAX,
        max(
            config.UI_SECONDS_MIN,
            len(text) / config.UI_CHARACTERS_PER_SECOND,
        )
    )
    return loop.call_later(hold_duration, _cleanup_subtitle_text, root_window)



async def run(root_window: tk.Tk, queue: asyncio.Queue) -> None:

    log.info('starting')
    loop = asyncio.get_event_loop()

    def update_subtitle_text(text: str) -> asyncio.Handle:
        _update_subtitle_text(root_window, text)
        return _schedule_cleanup(loop, root_window, text)

    cleanup_timer = update_subtitle_text(config.UI_HELLO)

    while True:
        subtitle_text = await queue.get()
        cleanup_timer.cancel()
        log.debug(f'{subtitle_text=}')
        cleanup_timer = update_subtitle_text(subtitle_text)
