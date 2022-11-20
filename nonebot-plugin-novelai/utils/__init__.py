from io import BytesIO
from PIL import Image
import re
import aiohttp


def is_contain_chinese(check_str: str):
    # 检查字符串是否包含汉字
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def file_name_check(input: str):
    # 检查文件名是否包含奇怪字符
    errorcode = ["?", "<", ">", "\\", "/", "*", "|", ":"]
    for i in errorcode:
        input.replace(i, "")
    return input


async def check_last_version(package: str):
    # 检查包的最新版本
    async with aiohttp.ClientSession() as session:
        async with session.get("https://pypi.org/simple/"+package) as resp:
            text = await resp.text()
            pattern = re.compile("-(\d.*?).tar.gz")
            pypiversion = re.findall(pattern, text)[-1]
    return pypiversion


async def compare_version(old: str, new: str):
    # 比较两个版本哪个最新
    oldlist = old.split(".")
    newlist = new.split(".")
    for i in range(len(oldlist)):
        if int(newlist[i]) > int(oldlist[i]):
            return True
    return False


async def sendtosuperuser(message):
    # 将消息发送给superuser
    from nonebot import get_bot, get_driver
    import asyncio
    superusers = get_driver().config.superusers
    bot = get_bot()
    for superuser in superusers:
        await bot.call_api('send_msg', **{
            'message': message,
            'user_id': superuser,
        })
        await asyncio.sleep(5)


async def png2jpg(raw: BytesIO):
    img_PIL = Image.open(raw)
    img_PIL.convert("RGB")
    image_new = BytesIO()
    img_PIL.save(image_new, format="JPEG", quality=95)
    return image_new

