from collections import list, namedtuple
from dataclasses import dataclass

from PIL import Image, ImageDraw, ImageFont

from ..parser.block import Block, Inline, RawText, Text
from .block import (
    BlockRenderer,
    Header1Renderer,
    Header2Renderer,
    Header3Renderer,
    ListRenderer,
    QuoteRenderer,
    Renderer,
    TextRenderer,
)
from .utils import State, getfont


class MarkdownRenderer:
    __slots__ = ("font", "fontsize", "lineheight", "renderer", "paragraph_height")

    def __init__(
        self,
        default_font="Consolas",
        fontsize=16,
        lineheight=1.5,
        paragraph_height=2,
    ):
        self.font: str = {"default": default_font}
        self.fontsize: int = fontsize
        self.lineheight: float = lineheight
        self.renderer = Renderer()
        self.paragraph_height = paragraph_height

    def __call__(self, ast, width):  # TODO
        state = State(
            font=self.font,
            font_size=self.fontsize,
            style=set(),
            line_height=self.lineheight,
            paragraph_height=self.paragraph_height,
            color="black",
            startx=0,
            endx=width,
            align="left",
        )
        renderast = []
        for i in ast:
            renderast.extend(
                self.renderer.get(i.type, self.renderer.p)(i, state, self.renderer)
            )
        return renderast
