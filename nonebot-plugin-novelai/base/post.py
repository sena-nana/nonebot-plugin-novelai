import base64
from io import BytesIO

import aiohttp
from nonebot.log import logger
from .fifo import FIFO_BASE
from ..utils import png2jpg

async def post_base(fifo: FIFO_BASE, header, post_api):
    # 请求交互
    img_bytes = []
    async with aiohttp.ClientSession(headers=header) as session:
        for i in range(fifo.count):
            # 向服务器发送请求
            async with session.post(post_api, json=fifo.body(i)) as resp:
                if resp.status not in [200, 201]:
                    raise RuntimeError("与服务器沟通时发生{resp.status}错误")
                img = await resp.text()
                img = img.split("data:")[1]
                logger.debug(f"获取到返回图片，正在处理")

                # 将图片转化为jpg(BytesIO)
                image = BytesIO(base64.b64decode(img))
                image_new = await png2jpg(image)
                img_bytes.append(image_new)
    return img_bytes