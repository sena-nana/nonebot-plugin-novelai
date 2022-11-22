from ...config import config
from .fifo import FIFO
from ..base.post import post_base

header = {
    "authorization": "Bearer " + config.novelai_token,
    ":authority": "https://api.novelai.net",
    ":path": "/ai/generate-image",
    "content-type": "application/json",
    "referer": "https://novelai.net",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
}
post_api = "https://api.novelai.net/ai/generate-image"

async def post(fifo: FIFO):
    return await post_base(fifo, header, post_api)
