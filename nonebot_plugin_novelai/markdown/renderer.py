import mistune
from text import Text
from block import Image, Inline, RawText, Block


class WordRenderer(mistune.AstRenderer):
    NAME = "word"

    def text(self, text):
        return Text(text)

    def link(self, link, children=None, title=None):
        if isinstance(children, list):
            a = children.pop(0)
            while children:
                a.children.extend(children.pop(0).children)
            for i in a.children:
                i.type.add("link")
            return a
        else:
            return Text(link, type="link")

    def image(self, src, alt="", title=None):
        return Image(src)

    def codespan(self, text):
        return RawText(text, "code")

    def linebreak(self):
        return Inline("linebreak")

    def emphasis(self, children):
        if isinstance(children, list):
            a = children.pop(0)
            while children:
                a.children.extend(children.pop(0).children)
        else:
            a = children
        for i in a.children:
            i.type.add("emphasis")
        return a

    def inline_html(self, html):
        return RawText(html, "html")

    def heading(self, children, level):
        return Block(children, "h" + str(level))

    def newline(self):
        return Block([], "newline")

    def thematic_break(self):
        return Inline("thematic_break")

    def paragraph(self, children):
        if isinstance(children, Block):
            return children
        a = []
        for i in children:
            a.extend(i.children)
        return Block(a, "paragraph")

    def block_code(self, children, info=None):
        return Block(children, "code")

    def block_html(self, children):
        return Block(children, "html")

    def block_text(self, children):
        if isinstance(children, list):
            a = []
            while children:
                if a and isinstance(children[0], Text) and isinstance(a[-1], Text):
                    a[-1].children.extend(children.pop(0).children)
                else:
                    a.append(children.pop(0))

        else:
            a = children
        return Block(a)

    def strong(self, children):
        if isinstance(children, list):
            a = children.pop(0)
            while children:
                a.children.extend(children.pop(0).children)
        else:
            a = children
        for i in a.children:
            i.type.add("strong")
        return a

    def block_quote(self, children):
        return Block(children, "quote")

    def list(self, children, ordered, level, start=None):
        for i in children:
            i.type = "ordered_list" if ordered else "list"
        return children

    def list_item(self, children, level):
        return [Block(i) if i.type != "p" else i for i in children]

    def task_list_item(self, children, level, checked):
        return Block(children, "checked" if checked else "blank")

    def _create_default_method(self, name):
        def __ast(children):
            return Block(children, name)

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
        ast = []
        for i in data:
            if isinstance(i, list):
                ast.extend(i)
            else:
                ast.append(i)
        return ast
