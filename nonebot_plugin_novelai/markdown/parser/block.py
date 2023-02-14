from .text import Text
from .word import Base


class Inline:
    """
    内联符号
    """

    __slots__ = ("type",)

    def __init__(self, type):
        self.type = type

    def __repr__(self) -> str:
        return self.parser().__repr__()

    def __str__(self) -> str:
        return f"Inline({self.type})"

    def parser(self):
        return {
            "class": self.__class__.__name__,
            "type": self.type,
        }

    def __len__(self) -> int:
        return 0


class Image(Inline):
    """
    图片块
    """

    __slots__ = ("src", "width", "height", "radius")

    def __init__(self, src: str, width=0, height=0, radius=0):
        self.src = src
        self.width = width
        self.height = height
        self.radius = radius

    def __repr__(self) -> str:
        return self.parser().__repr__()

    def __str__(self) -> str:
        return f"Image({self.src})"

    def parser(self):
        return {
            "class": self.__class__.__name__,
            "src": self.src,
            "width": self.width,
            "height": self.height,
            "radius": self.radius,
        }

    def __len__(self) -> int:
        return self.width


class RawText(Inline):
    """
    纯文本块
    """

    __slots__ = ("content", "type")

    def __init__(self, content: str = "", type: str = ""):
        self.content = content
        self.type = type

    def __str__(self) -> str:
        return "\n" + self.content + "\n"

    def parser(self):
        return {
            "class": self.__class__.__name__,
            "content": self.content,
            "type": self.type,
        }

    def __len__(self) -> int:
        return len(self.content)


class Block:
    """
    文本块
    """

    __slots__ = (
        "children",
        "type",
        "align",
    )

    def __init__(
        self,
        children,
        type="p",
        align="",
    ) -> None:
        if isinstance(children, str):
            children = [Text(children)]
        if isinstance(children, (Text, Inline, Block)):
            children = [children]
        if isinstance(children, Base):
            children = [Text(children)]
        if isinstance(children, list):
            self.children = children
        self.type = type
        self.align = align

    def __str__(self) -> str:
        return "".join(map(str, self.children)) + "\n"

    def __repr__(self) -> str:
        return self.parser().__repr__()

    def parser(self):
        return {
            "class": self.__class__.__name__,
            "children": [i.parser() for i in self.children],
            "state": self.state,
            "predraw": self.predraw,
            "postdraw": self.postdraw,
        }

    def __len__(self) -> int:
        return sum(map(len, self.children))
