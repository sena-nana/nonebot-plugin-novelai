from ..config import config, nickname
from ..utils.save import save_img
from io import BytesIO
import base64
import aiohttp
import asyncio
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.log import logger


async def check_safe_method(fifo, img_bytes, message):
    if config.novelai_h:
        for i in img_bytes:
            await save_img(fifo, i)
            message += MessageSegment.image(i)
    else:
        nsfw_count = 0
        for i in img_bytes:
            try:
                label = await check_safe(i)
            except RuntimeError as e:
                logger.error(f"NSFWAPI调用失败，错误代码为{e.args}")
                label = "unknown"
            if label != "explicit":
                message += MessageSegment.image(i)
            else:
                nsfw_count += 1
            await save_img(fifo, i, label)
        if nsfw_count > 0:
            message += f"\n有{nsfw_count}张图片太涩了，{nickname}已经帮你吃掉了哦"
    return message


async def check_safe(img_bytes: BytesIO):
    # 检查图片是否安全
    start = "data:image/jpeg;base64,"
    image = img_bytes.getvalue()
    image = str(base64.b64encode(image), "utf-8")
    str0 = start + image
    # 重试三次
    for i in range(3):
        async with aiohttp.ClientSession() as session:
            # 调用API
            async with session.post('https://hf.space/embed/mayhug/rainchan-image-porn-detection/api/predict/',
                                    json={"data": [str0]}) as resp:
                if resp.status == 200:
                    jsonresult = await resp.json()
                    break
                else:
                    await asyncio.sleep(2)
                    error = resp.status
    else:
        raise RuntimeError(error)
    return jsonresult["data"][0]["label"]
