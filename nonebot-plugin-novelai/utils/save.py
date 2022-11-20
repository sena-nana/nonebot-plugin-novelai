from io import BytesIO
from ..config import config
from pathlib import Path
import hashlib
import aiofiles
path = Path("data/novelai/output").resolve()
async def save_img(fifo, img_bytes: BytesIO, extra: str = "unknown"):
    # 存储图片
    if config.novelai_save_pic:
        path_ = path / extra
        path_.mkdir(parents=True, exist_ok=True)
        hash = hashlib.md5(img_bytes.getvalue()).hexdigest()
        file = (path_ / hash).resolve()
        async with aiofiles.open(str(file) + ".jpg", "wb") as f:
            await f.write(img_bytes.getvalue())
        async with aiofiles.open(str(file) + ".txt", "w") as f:
            await f.write(repr(fifo))
