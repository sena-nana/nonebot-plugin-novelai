import mistune
from text import Text
from block import Image, Inline, RawText, Block


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
            a = Text()
            a.children = children
            for i in a.children:
                i.type = "emphasis"
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
        for i in children:
            i.type = "ordered_list" if ordered else "list"
            i.level = level
        return children

    def list_item(self, children, level):
        return [Block(i, level, "list_item") for i in children]

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
        ast=[]
        for i in data:
            if isinstance(i, list):
                ast.extend(i)
            else:
                ast.append(i)
        return ast