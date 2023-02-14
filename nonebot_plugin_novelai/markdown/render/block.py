from collections import namedtuple
from dataclasses import dataclass

from PIL import Image, ImageDraw, ImageFont

from ..parser.block import Block, Inline, RawText, Text
from ..parser.word import Full, Void, Word
from .utils import State, getfont

Step = namedtuple("Step", ["func", "kwargs"])


class Buffer:
    __slots__ = ("maxheight", "buffer", "width")

    def __init__(self):
        self.maxheight = 0
        self.buffer = []
        self.width = []

    def clear(self):
        self.buffer.clear()
        self.width.clear()
        self.maxheight = 0

    def updateheight(self, height):
        self.maxheight = max(self.maxheight, height)

    def append(self, step, width):
        self.buffer.append(step)
        self.width.append(width)

    def extend(self, steps, width):
        self.buffer.extend(steps)
        self.width.extend(width)

    def __iter__(self):
        return zip(self.buffer, self.width)

    def __len__(self):
        return len(self.buffer)

    def getwidth(self, index=0):
        if index == 0:
            return sum(self.width)
        else:
            return sum(self.width[:index])

    def pop(self):
        return self.buffer.pop(), self.width.pop()

    def countvoid(self):
        return sum(1 for i in self.buffer if i.__class__ == Void)


class TextRenderer:
    def __call__(
        self,
        state: State,
        linewidth: int,
        i: Text,
        buffer: Buffer,
    ):
        for j in i.children:  # TODO
            if isinstance(j, (Word, Full)):
                bold = j.bold or state.bold
                italic = j.italic or state.italic
                font = getfont(j.lang, state.font, state.font_size)
                text = j.content
                text_width, text_height = font.getsize(text)
                buffer.updateheight(text_height)
                buffer.append(j, text_width)
                all_width = buffer.getwidth()
                if all_width > (linewidth + state.font_size * 2):
                    self.cut(buffer, linewidth, state.font_size)

    def cut(self, buffer: Buffer, linewidth: int, fontsize: int):
        for i in range(len(buffer)):
            if buffer.buffer[-i].__class__ == Void:
                count = buffer.countvoid()
                diff = linewidth - buffer.getwidth(-i - 1)
                return buffer.buffer[-i - 1], buffer.width[-i - 1]
            if buffer.getwidth(-i) < (linewidth - fontsize * 2):
                break

    def draw(self, state: State, queue: list, i: Word):  # TODO
        ...

    def void(self, state: State, width: int):
        state.x += width


class BlockRenderer:
    __slots__ = "state"

    def __init__(self):
        self.state = State()

    def preprocess(self, ast: Block, state: State, queue: list):
        """
        对于每个块，都会先调用这个函数，用于预处理state
        """
        state_copy = state.copy()
        if self.state.font_size:
            state_copy.font_size = state.font_size * self.state.font_size
        if self.state.font:
            state_copy.font.update(self.state.font)
        if self.state.color:
            state_copy.color = self.state.color
        if self.state.padding:
            state_copy.startx = self.state.padding[3]
            state_copy.endx -= self.state.padding[1]
        state_copy.x = state_copy.startx
        state_copy.y = state_copy.padding[0]
        if self.state.line_height:
            state_copy.line_height = self.state.line_height * state.line_height
        if self.state.align:
            state_copy.align = self.state.align
        state_copy.bold = self.state.bold or state.bold
        state_copy.italic = self.state.italic or state.italic
        return state_copy

    def predraw(self, ast: Block, state: State, queue: list):
        """
        在draw之前调用，用于添加一些额外的步骤
        """
        pass

    def draw(
        self,
        ast: Block,
        state: State,
        renderer: "Renderer",
    ) -> list:
        """
        用于绘制块
        """
        if ast.children:
            queue = list()
            if not isinstance(ast.children[0], Block):
                void_width = state.font_size * 0.5
                x = 0
                linewidth = state.endx - state.startx
                buffer = Buffer()
                for i in ast.children:
                    if isinstance(i, Text):
                        renderer.text(state, queue, void_width, x, linewidth, i, buffer)
                    else:
                        renderer.__getattribute__(i.type)(state, queue, i, buffer)
                if buffer:
                    for i in buffer:
                        if isinstance(i, (Word, Full)):
                            renderer.text.draw(state, queue, i)
                        elif isinstance(i, (Void)):
                            renderer.text.void(state, void_width)
                        else:
                            renderer.__getattribute__(i.type).draw(state, queue, i)
            else:
                queue = renderer.__getattribute__(i.type)(state, queue, ast.children)
        return queue

    def postdraw(
        self,
        ast: Block,
        state: State,
        queue: list,
        interqueue: list,
    ):
        """
        再draw之后调用，用于添加一些额外的步骤
        """
        queue.extend(interqueue)

    def postprocess(self, ast: Block, state: State, queue: list):
        """
        在所有步骤之后调用，用于回退state
        """
        if self.state.padding:
            state.endx += self.state.padding[1]
            state.startx -= self.state.padding[3]
            state.y += self.state.padding[2]
        state.y += (
            self.state.paragraph_height or state.paragraph_height
        ) * state.font_size
        state.x = state.startx

    def __call__(
        self,
        ast: Block,
        state: State,
        renderer: dict,
        queue: list = None,
    ):

        if not queue:
            queue = list()
        state_copy = self.preprocess(ast, state, queue)
        self.predraw(ast, state_copy, queue)
        interqueue = self.draw(ast, state_copy, renderer)
        self.postdraw(ast, state_copy, queue, interqueue)
        self.postprocess(ast, state, queue)
        return queue


class Header1Renderer(BlockRenderer):
    def __init__(self):
        self.state = State(font_size=2, padding=(0, 10), bold=True)

    def postprocess(self, ast: Block, state: State, queue: list):
        queue.append(
            Step(
                func="line",
                kwargs={
                    "xy": (
                        state.startx,
                        state.y + state.line_height,
                        state.endx,
                        state.y + state.line_height,
                    ),
                    "fill": state.color + "aa",
                    "width": state.font_size / 10,
                },
            )
        )
        state.y += state.paragraph_height * state.font_size
        state.x = state.startx


class Header2Renderer(Header1Renderer):
    def __init__(self):
        self.state = State(font_size=1.5, padding=(0, 10), bold=True)


class Header3Renderer(Header1Renderer):
    def __init__(self):
        self.state = State(font_size=1.25, padding=(0, 10), bold=True)


class ListRenderer(BlockRenderer):
    def draw(self, ast: Block, state: State, queue: list):
        queue.append(
            Step(
                func="text",
                kwargs={
                    "text": "●",
                    "xy": (state.x, state.y),
                    "font": getfont("en", state.font, state.font_size),
                    "fill": state.color,
                },
            )
        )
        state.x += state.font_size * 1.5
        state.startx += state.font_size * 1.5


class NewLineRenderer(BlockRenderer):
    ...


class QuoteRenderer(BlockRenderer):
    def preprogress(self, ast: Block, state: State):
        self.state.padding = (state.font_size * 1.5, 0)
        self.state.startx += state.font_size * 1.5
        self.state.color = self.state.color + "aa"  # TODO


@dataclass
class Renderer:
    p: BlockRenderer = BlockRenderer()
    h1: Header1Renderer = Header1Renderer()
    h2: Header2Renderer = Header2Renderer()
    h3: Header3Renderer = Header3Renderer()
    list: ListRenderer = ListRenderer()
    tasklist: ListRenderer = ListRenderer()
    quote: QuoteRenderer = QuoteRenderer()
    text: TextRenderer = TextRenderer()

    def __getattribute__(self, __name: str):
        if __name in self.__dict__:
            return self.__dict__[__name]
        else:
            return self.p

    def __setattr__(self, __name: str, __value) -> None:
        if __name in self.__dict__:
            self.__dict__[__name] = __value
        else:
            self.p = __value
