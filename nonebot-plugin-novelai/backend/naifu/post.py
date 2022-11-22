from ...config import config
from .fifo import FIFO
from ..base.post import post_base

header = {
    "content-type": "application/json",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
}
post_api="http://"+config.novelai_site + "/generate-stream"

async def post(fifo: FIFO):
    return await post_base(fifo, header, post_api)
