import re
from . import file_name_check, is_contain_chinese
from ..extension.translation import translate
from ..config import config
from .data import htags


async def prepocess_tags(tags: str):
    # 处理奇奇怪怪的输入
    tags = re.sub("[\f\n\r\t\v]", "", tags)
    tags = file_name_check(tags)

    # 检测中文
    taglist = tags.split(",")
    tagzh = ""
    tags_ = ""
    for i in taglist:
        if is_contain_chinese(tags):
            tagzh += f"{i},"
        else:
            tags_ += f"{i},"
    if tagzh:
        tags_en = await translate(tagzh, "en")
        if tags_en == tagzh:
            return f"检测到中文，翻译失败，生成终止，请联系BOT主查看后台"
        else:
            tags_ += tags_en

    # 检测是否有18+词条
    if not config.novelai_h:
        pattern = re.compile(f"(\s|,|^)({htags})(\s|,|$)")
        if (re.search(pattern, tags) is not None):
            return "H是不行的!"

    tags = tags_
