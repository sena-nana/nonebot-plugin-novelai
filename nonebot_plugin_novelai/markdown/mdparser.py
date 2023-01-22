import re
import mistune


class Base:

    text = ""
    type = ""

    def __init__(self, text: str = "", type: str = "text"):
        self.text = text
        self.type = type

    def __add__(self, other) -> "Text":
        if isinstance(other, (Base, str)):
            return self + Text(other)
        elif isinstance(other, Text):
            if (
                isinstance(other.children[0], self.__class__)
                and other.children[0].type == self.type
            ):
                other.children[0].text = self.text + other.children[0].text

                return other
            else:
                if (
                    self.text[-1] in RIGHT_FULL | RIGHT_HALF
                    or other.children[0].text[0] in LEFT_HALF | LEFT_FULL
                ):
                    other.children.insert(0, Void())
                other.children.insert(0, self)
                return other
        elif isinstance(other, (Block, Inline)):
            return Text(self) + other
        else:
            raise NotImplementedError

    def __radd__(self, other):
        if isinstance(other, (Base, str)):
            return Text(other) + self
        raise NotImplementedError

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

    def __add__(self, other):
        if isinstance(other, Text):
            if other.children[0].__class__ == self.__class__:
                return other
            other.children.insert(0, self)
            return other
        if isinstance(other, (str, Word, Full)):
            return Text(other)
        if isinstance(other, (Block, Inline)):
            return other
        if isinstance(other, Void):
            return self

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


TO_HALF = r"""!?｡"#$%&'()*+,-/:;<=>@[\]^_`{|}~"""
FROM = "！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～"

HALF = r"""､–—‛„‟… !?｡"#$%&'*+,-/:;<=>@\^_`|~〃‧"""
LEFT_HALF = "([{｢“‘"
RIGHT_HALF = ")]}｣”’"
LEFT_FULL = "｟《「『【〔〖〘〚〝"
RIGHT_FULL = "｠》」』】〕〗〙〛〞〟。、"

trans = str.maketrans(FROM, TO_HALF)

word_p = re.compile("([a-zA-Z0-9\+\.､–—‛„‟…!\?｡\"#\$%&'*+,-/:;<=>@\\\^_`\|~〃‧]+)")
right_p = re.compile("([\)\]\}｣”’｠》」』】〕〗〙〛〞〟。、]+)")
left_full_p = re.compile("([｟《「『【〔〖〘〚〝]+)")
left_half_p = re.compile("([\(\[\{｢“‘]+)")
space = re.compile("\s")
emoji = re.compile(
    "["
    "\U0001F300-\U0001F64F"
    "\U0001F680-\U0001F6FF"
    "\u2600-\u2B55"
    "\U00010000-\U0010ffff]+"
)


class Text:
    def __init__(self, text=Word(), type="text"):
        self.children: list[Word] = []
        if isinstance(text, str):
            self._init(text, text_type=type)
        elif isinstance(text, Base):
            self.children.append(text)
        else:
            raise ValueError

    def _init(self, i, text_type="text"):
        if isinstance(i, dict):
            j = i["text"].translate(trans)

        elif isinstance(i, str):
            j = i.translate(trans).replace("- [ ] ", "◻️").replace("- [x] ", "☑️")
        else:
            raise ValueError
        while j:
            raw_text = ""
            if raw := re.match(pattern=word_p, string=j):
                raw_text = raw.group()
                if self.children:
                    if re.search(pattern=right_p, string=self.children[-1].text):
                        self.children.append(Void())
                    if (
                        isinstance(self.children[-1], Word)
                        and self.children[-1].type == text_type
                    ):
                        self.children[-1].text = self.children[-1].text + raw_text
                    else:
                        if not isinstance(self.children[-1], Void):
                            self.children.append(Void())
                        word = Word(raw_text, text_type)
                        self.children.append(word)
                else:
                    self.children.append(Word(raw_text, text_type))
            elif raw := re.match(pattern=left_half_p, string=j):
                raw_text = raw.group()

                if self.children:
                    self.children.append(Void())
                self.children.append(Word(raw_text, text_type))
            elif raw := re.match(pattern=left_full_p, string=j):
                raw_text = raw.group()

                if self.children:
                    self.children.append(Void())
                self.children.append(LeftFull(raw_text, text_type))
            elif raw := re.match(pattern=right_p, string=j):
                raw_text = raw.group()

                if (
                    self.children
                    and isinstance(self.children[-1], Word)
                    and self.children[-1].type == text_type
                ):
                    self.children[-1].text = self.children[-1].text + raw_text
                else:
                    self.children.append(Word(raw_text, text_type))
            elif raw := re.match(pattern=space, string=j):
                raw_text = raw.group()
                self.children.append(Void())
            elif raw := re.match(pattern=emoji, string=j):
                raw_text = raw.group()

                self.children.append(Emoji(raw_text, text_type))
            else:
                raw_text = j[0]

                if self.children and re.search(right_p, self.children[-1].text):
                    self.children.append(Void())
                if self.children and isinstance(self.children[-1], Full):
                    self.children[-1].text = self.children[-1].text + raw_text
                else:
                    self.children.append(Full(raw_text, text_type))
            j = j.replace(raw_text, "", 1)

    def __add__(self, other):
        print(self, other)
        if isinstance(other, Void) and isinstance(self.children[-1], Void):
            return self
        elif isinstance(other, Text):
            word = other.children.pop(0)
            if (
                isinstance(word, self.children[-1].__class__)
                and word.type == self.children[-1].type
            ):
                self.children[-1].text = self.children[-1].text + word.text
            else:
                if not isinstance(self.children[-1], (Word, Full)):
                    if (
                        self.children[-1].text[-1] in RIGHT_FULL + RIGHT_HALF
                        or word.text[0] in LEFT_HALF + LEFT_FULL
                    ):
                        self.children.append(Void())
                self.children.append(word)
            self.children.extend(other.children)
            return self
        elif isinstance(other, (str, Base)):
            return self + Text(other)
        elif isinstance(other, (Block)):
            other.children.insert(0, self)
            return other
        elif isinstance(other, Inline):
            return Block([self, other])
        else:
            raise NotImplementedError

    def __radd__(self, other):
        if isinstance(other, (str, Base)):
            return Text(other) + self
        if other is None:
            return self
        raise NotImplementedError

    def __repr__(self) -> str:
        return self.parser().__repr__()

    def __str__(self) -> str:
        return "".join(map(str, self.children))

    def parser(self):
        return {
            "class": self.__class__.__name__,
            "children": [i.parser() for i in self.children],
        }


class Inline:
    type = ""

    def __init__(self, type):
        self.type = type

    def __add__(self, other):
        if isinstance(other, (Inline, Text)):
            return Block(self, other)
        if isinstance(other, Block):
            other.children.insert(0, self)
            return other
        if isinstance(other, (str, Base)):
            return Block(self, Text(other))

    def __radd__(self, other):
        if isinstance(other, (Inline, Text)):
            return Block(other, self)
        if isinstance(other, Block):
            other.children.append(self)
            return other
        if isinstance(other, (str, Base)):
            return Block(Text(other), self)

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
    content = ""
    type = ""

    def __init__(self, content: str, type: str):
        self.content = content
        self.type = type

    def __str__(self) -> str:
        return "\n"+self.content+"\n"

    def parser(self):
        return {
            "class": self.__class__.__name__,
            "content": self.content,
            "type": self.type,
        }


class Block:
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

    def __add__(self, other):
        if isinstance(other, Block):
            return Mdparser([self, other])
        elif isinstance(other, (Text, Base, str)):
            self.children[-1] += other
            return self

    def __radd__(self, other):
        return Text(other) + self

    def __str__(self) -> str:
        return "\n"+"".join(map(str, self.children))

    def __repr__(self) -> str:
        return self.parser().__repr__()

    def parser(self):
        return {
            "class": self.__class__.__name__,
            "children": [i.parser() for i in self.children],
            "type": self.type,
            "level": self.level,
        }


class WordRenderer(mistune.AstRenderer):
    NAME = "word"

    def text(self, text):
        return Text(text)

    def link(self, link, children=None, title=None):
        if isinstance(children, list):
            return Text(str(children[0]), "link")
        else:
            return Text(link, type="link")

    def image(self, src, alt="", title=None):
        return Image(src)

    def codespan(self, text):
        return RawText(text, "code")

    def linebreak(self):
        return Inline("linebreak")

    def emphasis(self, children):
        if len(children) == 1:
            return children.pop()
        else:
            a=Text()
            a.children=children
            for i in a.children:
                i.type="emphasis"
            return a

    def inline_html(self, html):
        return RawText(html, "html")

    def heading(self, children, level):
        return Block(children, level, "heading")

    def newline(self):
        return Block([], 1, "newline")

    def thematic_break(self):
        return Inline("thematic_break")

    def paragraph(self, children):
        return Block(children, 1, "paragraph")

    def block_code(self, children, info=None):
        return Block(children, 1, "code")

    def block_html(self, children):
        return Block(children, 1, "html")

    def block_text(self, children):
        if len(children) == 1:
            return children.pop()
        else:
            return Text("".join(map(str, children)))

    def strong(self, children):
        if len(children) == 1:
            return children.pop()
        else:
            return Text("".join(map(str, children)), "strong")

    def block_quote(self, children):
        return Block(children, 1, "quote")

    def list(self, children, ordered, level, start=None):
        return Block(children, level, "ordered_list" if ordered else "list")

    def list_item(self, children, level):
        if len(children) == 1:
            return children.pop()
        else:
            return Block(children, level, "list_item")

    def task_list_item(self, children, level, checked):
        return Block(children, level, "checked" if checked else "blank")

    def _create_default_method(self, name):
        def __ast(children):
            return Block(children, 1, name)

        return __ast

    def _get_method(self, name):
        try:
            return self.__getattribute__(name)
        except AttributeError:
            method = self._methods.get(name)
            if not method:
                raise AttributeError('No renderer "{!r}"'.format(name))
            return method

    def finalize(self, data):
        return list(data)


class Mdparser:
    def __init__(self, text) -> None:
        self.children = mistune.markdown(
            text,
            renderer=WordRenderer(),
            plugins=["task_lists", "strikethrough", "url"],
        )
        self.__repr__()

    def __repr__(self) -> str:
        a = "".join([repr(i) + "," for i in self.children])
        return f"Mdparser({a})"

    def __add__(self, other):
        if isinstance(other, Mdparser):
            self.children.extend(other.children)
            return self
        elif isinstance(other, (str, Base)):
            return self + Mdparser(other)
        elif isinstance(other, Text):
            self.children.append(other)
            return self
        else:
            raise NotImplementedError

    def __radd__(self, other):
        if isinstance(other, Mdparser):
            self.children = other.children + self.children
            return self
        if isinstance(other, (str, Base)):
            return Mdparser(other) + self
        if isinstance(other, (Text, Inline)):
            self.children.insert(0, other)
            return self
        else:
            raise NotImplementedError

    def __str__(self) -> str:
        return "".join(map(str, self.children))
