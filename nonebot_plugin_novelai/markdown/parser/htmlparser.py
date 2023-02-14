import re

import mistune
import xmltodict
from lxml import etree

from .block import Block, Image
from .renderer import WordRenderer
from .text import Text

radius_re = re.compile(r"(?<=border-radius:)[ ]+(\d+)(px|%)(?=,)")


def _parse_img(img):
    img_ = Image(img.get("@src"))
    img_.width = int(img.get("@width", 0))
    img_.height = int(img.get("@height", 0))
    if a := img.get("@style"):
        if radius := re.search(radius_re, a):
            img_.radius = radius.groups()
    return img_


def _mdparser(ast, div: bool = False):
    parser = []
    align = ""
    if div:
        if "@align" in ast:
            align = ast["@align"]
            del ast["@align"]
        block = Block([], align=align)
    for i, v in ast.items():
        if i == "br":
            if div:
                parser.append(block)
                block = Block([], align=align)
            else:
                parser.append(Block([]))
        if i == "div":
            if div:
                block.children.extend(_mdparser(v, True))
            else:
                parser.extend(_mdparser(v, True))
        if i == "a":
            if isinstance(v, dict):
                v = [v]
            for k in v:
                if k.get("img"):
                    if div:
                        block.children.append(_parse_img(k["img"]))
                    else:
                        parser.append(Block(_parse_img(k["img"])))
                else:
                    if div:
                        block.children.append(Text(k["@href"], color="link"))
                    else:
                        parser.append(Block(Text(k["@href"], color="link")))
        if i == "img":
            if div:
                block.children.append(_parse_img(v))
            else:
                parser.append(Block(_parse_img(k["img"])))
        if i in ["#text", "p"]:
            if div:
                parser.append(block)
                block = Block([], align=align)
            a = mistune.markdown(
                v,
                renderer=WordRenderer(),
                plugins=["task_lists", "strikethrough", "url"],
            )
            if align:
                for i in a:
                    if isinstance(i, Block):
                        i.align = align
            parser.extend(a)
    if div:
        parser.append(block)
    return parser


def htmlparser(html):
    tree = etree.HTML(html)
    a = xmltodict.parse(etree.tostring(tree, encoding="utf-8").decode("utf-8"))
    return _mdparser(a["html"]["body"])
