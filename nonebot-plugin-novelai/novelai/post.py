import base64
from io import BytesIO

import aiohttp
from nonebot.log import logger
from ..config import config
from .fifo import FIFO, header
from ..utils import png2jpg


async def post(fifo: FIFO):
    # novelai请求交互
    img_bytes = []
    async with aiohttp.ClientSession(headers=header) as session:
        for i in range(fifo.count):
            # 向novelai服务器发送请求
            async with session.post(
                    config.novelai_api_domain + "ai/generate-image", json=fifo.body(i)
            ) as resp:
                if resp.status != 201:
                    return f"与novelai服务器沟通时发生{resp.status}错误"
                img = await resp.text()
                img = img.split("data:")[1]
                logger.debug(f"获取到novelai返回图片，正在处理")

                # 将图片转化为jpg(BytesIO)
                image = BytesIO(base64.b64decode(img))
                image_new = await png2jpg(image)
                img_bytes.append(image_new)
    return img_bytes
