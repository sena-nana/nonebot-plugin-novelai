import aiohttp
import base64
from .utils import png2jpg
from io import BytesIO
from .fifo import FIFO,header
from .config import config
async def post(fifo:FIFO):
    #novelai请求交互
    img_bytes = []
    async with aiohttp.ClientSession(headers=header) as session:
        #向novelai服务器发送请求
        async with session.post(
            config.novelai_api_domain+"ai/generate-image", json=fifo.body()
        ) as resp:
            if resp.status != 201:
                return f"生成失败，错误代码为{resp.status}"
            img = await resp.text()
            img=img.split("data:")[1]

            #将图片转化为jpg(BytesIO)
            image=BytesIO(base64.b64decode(img))
            image_new=await png2jpg(image)
            img_bytes.append(image_new)
    return img_bytes
