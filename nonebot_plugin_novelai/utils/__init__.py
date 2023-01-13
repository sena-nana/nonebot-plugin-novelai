import base64
import re
from io import BytesIO

import aiohttp
from PIL import Image


async def check_last_version(package: str):
    # 检查包的最新版本
    async with aiohttp.ClientSession() as session:
        async with session.get("https://pypi.org/simple/" + package) as resp:
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
    import asyncio

    from nonebot import get_bot, get_driver

    superusers = get_driver().config.superusers
    bot = get_bot()
    for superuser in superusers:
        await bot.call_api(
            "send_msg",
            **{
                "message": message,
                "user_id": superuser,
            }
        )
        await asyncio.sleep(5)


async def png2jpg(raw: bytes):
    raw: BytesIO = BytesIO(base64.b64decode(raw))
    img_PIL = Image.open(raw)
    img_PIL.convert("RGB")
    image_new = BytesIO()
    img_PIL.save(image_new, format="JPEG", quality=95)
    image_new = image_new.getvalue()
    return image_new
