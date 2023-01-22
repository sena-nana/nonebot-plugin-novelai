class Base:

    text = ""
    type = ""

    def __init__(self, text: str = "", type: str = "text"):
        self.text = text
        self.type = type

    def __repr__(self) -> str:
        return self.parser().__repr__()

    def __str__(self) -> str:
        return self.text

    def parser(self):
        return {"class": self.__class__.__name__, "type": self.type, "text": self.text}


class Word(Base):
    """
    半宽字符类，用于表示英文字符和数字组合
    """


class Void(Base):
    """
    填白类
    """

    def __init__(self):
        pass

    def __str__(self) -> str:
        return " "

    def parser(self):
        return {"class": self.__class__.__name__}


class Full(Base):
    """
    全宽字符类，可以设置多个字符但不建议，可用于表示CJK字符
    """


class LeftFull(Word):
    """
    特殊字符类，用于表示全角左括号
    """


class Emoji(Full):
    """
    Emoji类，用于表示Emoji等方形字符
    """
