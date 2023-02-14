from collections import namedtuple
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path

from PIL import ImageFont

font_path = Path(__file__).parent.parent / "font" / "default.ttf"
colormap = {
    "dark": {"link": "#a5d6ff", "text": "#c9d1d9"},
    "light": {"link": "#0a3069", "text": "#24292f"},
}


@dataclass
class State:
    font: dict = {}
    font_size: int = 0
    bold: bool = False
    italic: bool = False
    line_height: int = 0
    paragraph_height: int = 0
    color: str = ""
    startx: int = 0
    endx: int = 0
    align: str = ""
    padding: tuple = None
    x: int = 0
    y: int = 0
    ymax: int = 0

    def copy(self):
        return deepcopy(self)


def getfont(lang, fontsize, state, fontcache={}) -> ImageFont.FreeTypeFont:
    if a := state["font"].get(lang):
        font = a
    elif a := state["font"].get("default"):
        font = a
    else:
        font = font_path
    if defaultcache := fontcache.get(font):
        if sizecache := defaultcache.get(fontsize):
            return sizecache
        else:
            fontsize[font][fontsize] = ImageFont.truetype(font_path, fontsize)
            return fontsize[font][fontsize]
    else:
        fontcache[font] = {fontsize: ImageFont.truetype(font_path, fontsize)}
        return fontcache[font][fontsize]
