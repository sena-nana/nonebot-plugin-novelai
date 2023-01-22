import re
from ..extension.translation import translate


async def prepocess_tags(tags: list[str]):
    tags: str = "".join([i+" " for i in tags if isinstance(i,str)])
    # 去除CQ码
    tags = re.sub("\[CQ[^\s]*?]", "", tags)
    # 检测中文
    taglist = tags.split(",")
    tagzh = ""
    tags_ = ""
    for i in taglist:
        if re.search('[\u4e00-\u9fa5]', tags):
            tagzh += f"{i},"
        else:
            tags_ += f"{i},"
    if tagzh:
        tags_en = await translate(tagzh, "en")
        if tags_en == tagzh:
            return ""
        else:
            tags_ += tags_en
    return tags_
