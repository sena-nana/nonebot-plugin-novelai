from dataclasses import dataclass
import mistune
from renderer import WordRenderer
import textwrap
from textwrap import dedent, indent
from PIL import Image, ImageFont, ImageDraw

_whitespace = "\t\n\x0b\x0c\r "


@dataclass
class TextRenderer:
    font: str = "Consolas"
    fontsize: int = 16


class MarkdownRenderer:
    def __init__(self, font="Consolas", fontsize=16, width=70):
        self.paragraph = TextRenderer()
        self.header = TextRenderer()
        self.header2 = TextRenderer()
        self.header3 = TextRenderer()
        self.list = TextRenderer()
        self.tasklist = TextRenderer()

    def __getattribute__(self, __name: str):
        if __name not in self.__dict__:
            self.__dict__[__name] = TextRenderer()
        return self.__dict__[__name]


class MarkdownWrapper:
    """
    类似于TextWrapper的markdown文本包装器，调用方式与TextWrapper不完全相同
    由于排版的特殊性，根据使用字体的不同，可能会出现结果不一致的情况
    :param width: 每行的宽度
    :param initial_indent: 第一行的缩进
    :param subsequent_indent: 后续行的缩进
    :param expand_tabs: 是否将tab转换为空格
    :param replace_whitespace: 是否将空白字符转换为空格
    :param tabsize: tab的宽度
    :param max_lines: 最大行数
    :param placeholder: 超出最大行数时的占位符
    :param renderer: MarkdownRenderer实例
    """

    unicode_whitespace_trans = {}
    uspace = ord(" ")
    for x in _whitespace:
        unicode_whitespace_trans[ord(x)] = uspace

    def __init__(
        self,
        width=70,
        initial_indent="",
        subsequent_indent="",
        expand_tabs=True,
        replace_whitespace=True,
        tabsize=8,
        *,
        max_lines=None,
        placeholder=" [...]",
        renderer=None,
    ):
        self.width = width
        self.initial_indent = initial_indent
        self.subsequent_indent = subsequent_indent
        self.expand_tabs = expand_tabs
        self.replace_whitespace = replace_whitespace
        self.tabsize = tabsize
        self.max_lines = max_lines
        self.placeholder = placeholder
        self.renderer = renderer

    def wrap(self, text: str):
        """
        对 text (字符串) 中的单独段落自动换行以使每行长度最多为 width 个字符
        所有自动换行选项均获取自 TextWrapper 实例的实例属性
        返回由输出行以及每行空白宽度组成的迭代器，行尾不带换行符
        如果自动换行输出结果没有任何内容，则引发异常
        """
        if self.expand_tabs:
            text = text.expandtabs(self.tabsize)
        if self.replace_whitespace:
            text = text.translate(self.unicode_whitespace_trans)

        if self.width <= 0:
            raise ValueError("invalid width %r (must be > 0)" % self.width)
        if self.max_lines is not None:
            if self.max_lines > 1:
                indent = self.subsequent_indent
            else:
                indent = self.initial_indent
            if len(indent) + len(self.placeholder.lstrip()) > self.width:
                raise ValueError("placeholder too large for max width")
        ast = mistune.markdown(
            text,
            renderer=WordRenderer(),
            plugins=["task_lists", "strikethrough", "url"],
        )
        return ast

    def fill(self, text):
        """
        对 text 中的单独段落自动换行并返回包含被自动换行段落的单独字符串以及空白宽度信息。
        """
        pass

    def parser(self, text):
        """
        返回解析后的ast
        """
        ast = mistune.markdown(
            text,
            renderer=WordRenderer(),
            plugins=["task_lists", "strikethrough", "url"],
        )
        return [i.parser() for i in ast]


def wrap(
    text: str,
    width: int = 70,
    *,
    expand_tabs: bool = True,
    tabsize: int = 8,
    replace_whitespace: bool = True,
    drop_whitespace: bool = True,
    initial_indent: str = "",
    subsequent_indent: str = "",
    fix_sentence_endings: bool = False,
    break_long_words: bool = True,
    break_on_hyphens: bool = True,
    max_lines: int = None,
    placeholder: str = "[...]",
) -> MarkdownWrapper:
    return MarkdownWrapper(text)


def fill(
    text: str,
    width: int = 70,
    *,
    expand_tabs: bool = True,
    tabsize: int = 8,
    replace_whitespace: bool = True,
    drop_whitespace: bool = True,
    initial_indent: str = "",
    subsequent_indent: str = "",
    fix_sentence_endings: bool = False,
    break_long_words: bool = True,
    break_on_hyphens: bool = True,
    max_lines: int = None,
    placeholder: str = "[...]",
):
    pass


def shorten(
    text: str,
    width: int = 70,
    *,
    fix_sentence_endings: bool = False,
    break_long_words: bool = True,
    break_on_hyphens: bool = True,
    placeholder: str = "[...]",
):
    ...


__all__ = [dedent, indent, MarkdownWrapper, wrap, fill, shorten]
