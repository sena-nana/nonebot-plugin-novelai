from dataclasses import dataclass
from io import BytesIO
from PIL import Image
import base64
from .config import config
from nonebot import get_driver

@dataclass()
class IMG():
    width: int=512
    height: int=512
    image: str=None

    def __post_init__(self):
        if self.image:
            tmpfile = BytesIO(self.image)
            image = Image.open(tmpfile)
            width, height = image.size
            if width >= height:
                self.width = round(width/height*8)*64
                self.height = 512
            else:
                self.height = round(height/width*8)*64
                self.width = 512
            self.image = str(base64.b64encode(self.image), "utf-8")

@dataclass
class FIFO():
    user_id: int
    tags: str
    seed: int
    data: list[IMG]
    group_id: int = 0
    strength: float = 0.7
    count: int = 1
    cost: int = 0
    def __post_init__(self):
        if config.novelai_paid == 1:
            anlas=0
            for i in self.data:
                anlas += round(i.width*i.height*self.strength*self.count/45875)
            if self.user_id in get_driver().config.superusers:
                self.cost = 0
            else:
                self.cost = anlas
        else:
            self.cost = 0
