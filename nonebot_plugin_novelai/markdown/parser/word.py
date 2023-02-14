from .utils import TextState


class Base:
    __slots__ = (
        "content",
        "bold",
        "italic",
        "color",
        "lang",
    )

    def __init__(
        self,
        content: str = "",
        bold: bool = False,
        italic: bool = False,
        lang: str = "",
        color: str = "",
    ):
        self.content = content
        self.bold = bold
        self.italic = italic
        self.lang = lang
        self.color = color

    def __repr__(self) -> str:
        return self.parser().__repr__()

    def __str__(self) -> str:
        return self.content

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, (Void, Emoji)):
            return False
        if isinstance(__o, Base):
            return (
                self.__class__ == __o.__class__
                and self.bold == __o.bold
                and self.italic == __o.italic
                and self.color == __o.color
                and self.lang == __o.lang
            )
        if isinstance(__o, TextState):
            return (
                self.__class__ == __o.classname
                and self.bold == __o.bold
                and self.italic == __o.italic
                and self.color == __o.color
                and self.lang == __o.lang
            )
        return False

    def parser(self):
        out = {
            "class": self.__class__.__name__,
            "content": self.content,
            "style": self.style,
            "lang": self.lang,
        }
        return out

    def __len__(self) -> int:
        return len(self.content)


class Word(Base):
    """
    半宽字符类，用于表示英文字符和数字组合
    """


class Void(Base):
    """
    填白类
    """

    __slots__ = "is_space"

    def __init__(self, is_space: bool = False):
        self.is_space = is_space

    def __str__(self) -> str:
        return " "

    def parser(self):
        return {"class": self.__class__.__name__}

    def __len__(self) -> int:
        return 1

    def __eq__(self, __o: object) -> bool:
        return __o.__class__ == self.__class__


class Full(Base):
    """
    全宽字符类，可以设置多个字符但不建议，可用于表示CJK字符
    """


class LeftFull(Word):
    """
    特殊字符类，用于表示全角左括号
    """


class Emoji(Void):
    """
    Emoji类，用于表示Emoji等方形字符
    """

    __slots__ = "content"

    def __init__(self, content: str):
        self.content = content

    def __str__(self) -> str:
        return self.content

    def parser(self):
        return {"class": self.__class__.__name__, "content": self.content}

    def __len__(self) -> int:
        return 2
