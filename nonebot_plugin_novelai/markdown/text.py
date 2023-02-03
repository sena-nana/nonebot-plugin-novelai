import re
from word import Word, Base, Void, Full, LeftFull, Emoji

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
ch = re.compile("[\u4e00-\u9fff]+")
jp = re.compile(
    "[" "\u3040-\u30ff" "\u31f0-\u31ff" "\u3300-\u33ff" "\u3400-\u4dbf" "]+"
)


class Text:
    """
    文本包装器，将文本分解
    """

    __slots__ = ("children",)

    def __init__(self, text=None, type=""):
        self.children: list[Word] = []
        if isinstance(text, str):
            self.init(text, text_type=type)
        elif isinstance(text, Base):
            self.children.append(text)
        elif isinstance(text, list):
            self.children = text

    def init(self, i, text_type=""):
        def cjk(j):
            if a := re.match(pattern=ch, string=j):
                return a.group(), "ch"
            elif a := re.match(pattern=jp, string=j):
                return a.group(), "jp"
            else:
                return None, None

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
                    if not isinstance(self.children[-1], Void) and re.search(
                        pattern=right_p, string=self.children[-1].text
                    ):
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
                self.children.append(Emoji(raw_text))
            else:
                raw_text, lang = cjk(j)
                if not raw_text:
                    raw_text = j[0]

                if (
                    self.children
                    and not isinstance(self.children[-1], Void)
                    and re.search(right_p, self.children[-1].text)
                ):
                    self.children.append(Void())
                if (
                    self.children
                    and isinstance(self.children[-1], Full)
                    and self.children[-1].lang == lang
                ):
                    self.children[-1].text = self.children[-1].text + raw_text
                else:
                    self.children.append(Full(raw_text, text_type, lang))
            j = j.replace(raw_text, "", 1)

    def __repr__(self) -> str:
        return self.parser().__repr__()

    def __str__(self) -> str:
        return "".join(map(str, self.children))

    def parser(self):
        return {
            "class": self.__class__.__name__,
            "children": [i.parser() for i in self.children],
        }
