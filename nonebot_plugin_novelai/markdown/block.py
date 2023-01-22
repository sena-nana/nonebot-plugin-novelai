from .text import Text
from .word import Base


class Inline:
    """
    内联符号
    """

    type = ""

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


class Image(Inline):
    """
    图片块
    """

    src = ""
    type = "image"

    def __init__(self, src: str):
        self.src = src

    def __repr__(self) -> str:
        return self.parser().__repr__()

    def __str__(self) -> str:
        return f"Image({self.src})"

    def parser(self):
        return {
            "class": self.__class__.__name__,
            "src": self.src,
            "type": self.type,
        }


class RawText(Inline):
    """
    纯文本块
    """

    content = ""
    type = ""

    def __init__(self, content: str, type: str):
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


class Block:
    """
    文本块
    """

    def __init__(
        self,
        children,
        level=1,
        type="paragraph",
    ) -> None:
        if isinstance(children, str):
            children = Text(children)
        if isinstance(children, (Text, Inline, Block)):
            children = [children]
        if isinstance(children, Base):
            children = [Text(children)]
        if isinstance(children, list):
            self.children = children
        self.type = type
        self.level = level

    def __str__(self) -> str:
        return "\n" + "".join(map(str, self.children))

    def __repr__(self) -> str:
        return self.parser().__repr__()

    def parser(self):
        return {
            "class": self.__class__.__name__,
            "children": [i.parser() for i in self.children],
            "type": self.type,
            "level": self.level,
        }
