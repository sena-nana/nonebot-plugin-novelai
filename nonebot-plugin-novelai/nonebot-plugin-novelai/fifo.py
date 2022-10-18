from dataclasses import dataclass
from io import BytesIO
from PIL import Image
import base64
from .config import config


@dataclass()
class TXT2IMG():
    width: int
    height: int
    image:None=None


@dataclass()
class IMG2IMG(TXT2IMG):
    image: str

    def __init__(self, img_b64):
        tmpfile = BytesIO(img_b64)
        image = Image.open(tmpfile)
        width, height = image.size
        if width >= height:
            self.width = round(width/height*8)*64
            self.height = 512
        else:
            self.height = round(height/width*8)*64
            self.width = 512
        self.image = str(base64.b64encode(img_b64), "utf-8")


@dataclass
class FIFO_TXT():
    user_id: int
    tags: str
    seed: int
    data: TXT2IMG
    group_id: int = 0
    strength: float = 0.7
    count: int = 1
    cost:None=None



@dataclass
class FIFO_IMG(FIFO_TXT):
    data: list[IMG2IMG]
    cost: int = 0
    def __post_init__(self):
        if config.novelai_paid == 1:
            anlas = 0
            for i in self.data:
                width = i.width
                height = i.height
                anlas += round(width*height*self.strength*self.count/45875)
            self.cost = anlas
        else:
            self.cost = 0
