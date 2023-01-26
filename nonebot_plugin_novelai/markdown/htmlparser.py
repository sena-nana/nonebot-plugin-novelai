from lxml import etree
import xmltodict
from block import Block, Image
from text import Text
import re
from renderer import WordRenderer
import mistune

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
    style = ""
    if div:
        if "@align" in ast:
            style = ast["@align"]
            del ast["@align"]
        block = Block([], style=style)
    for i, v in ast.items():
        if i == "br":
            if div:
                parser.append(block)
                block = Block([], style=style)
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
                        block.children.append(Text(k["@href"], "link"))
                    else:
                        parser.append(Block(Text(k["@href"], "link")))
        if i == "img":
            if div:
                block.children.append(_parse_img(v))
            else:
                parser.append(Block(_parse_img(k["img"])))
        if i in ["#text", "p"]:
            if div:
                parser.append(block)
                block = Block([], style=style)
            a = mistune.markdown(
                v,
                renderer=WordRenderer(),
                plugins=["task_lists", "strikethrough", "url"],
            )
            if style:
                for i in a:
                    if isinstance(i, Block):
                        i.style = style
            parser.extend(a)
    if div:
        parser.append(block)
    return parser


def mdparser(html):
    tree = etree.HTML(html)
    a = xmltodict.parse(etree.tostring(tree, encoding="utf-8").decode("utf-8"))
    return _mdparser(a["html"]["body"])


html = """
<div align="center">
  <a href="https://nb.novelai.dev"><img src="imgs/head.jpg" width="180" height="180" alt="NoneBot-plugin-novelai" style="border-radius:100%; overflow:hidden;"></a>
  <br>
</div>

# Nonebot-plugin-novelai

_✨ 中文输入、对接 webui、以及你能想到的大部分功能 ✨_


## 📖 功能介绍

- AI 绘画
  - 支持 CD 限速和绘画队列
  - 支持高级请求语法
  - 内置翻译 Api，自动翻译中文

> 123
> - 456
>   - 789
>   - 101112

## 💿 安装
请前往说明书查看[安装](https://nb.novelai.dev/main/install.html)一节



"""
import time
start=time.time()
print(mdparser(html))
print(time.time()-start)
