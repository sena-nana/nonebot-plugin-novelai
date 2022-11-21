import base64
from io import BytesIO
import time
from PIL import Image
from nonebot import get_driver
from ..utils.data import shapemap
from ..config import config
import random


class FIFO_BASE():
    model: str = ""
    sampler: str = ""

    def __init__(self,
                 user_id: str,
                 group_id: str,
                 tags: list[str] = [],
                 seed: int = None,
                 scale: int = None,
                 strength: float = None,
                 steps: int = None,
                 count: int = None,
                 noise: float = None,
                 ntags: list[str] = [],
                 shape: str = "p",
                 width: int = None,
                 height: int = None,
                 **kwargs):
        self.time = time.strftime("%Y-%m-%d %H:%M:%S")
        self.user_id: str = user_id
        self.tags: str = "".join([i+" " for i in tags])
        self.seed: list[int] = [seed or random.randint(0, 4294967295)]
        self.group_id: str = group_id
        self.scale: int = int(scale or 11)
        self.strength: float = strength or 0.7
        self.count: int = count or 1
        self.steps: int = steps or 28
        self.noise: float = noise or 0.2
        self.ntags: str = "".join([i+" " for i in ntags])
        self.img2img: bool = False
        self.image: str = None
        if width and height:
            self.shape_set(width,height)
        else:
            self.width, self.height = shapemap.get(shape or "p")
        # 数值合法检查
        if self.steps <= 0 or self.steps > 50:
            self.steps = 28
        # 多图时随机填充剩余seed
        for i in range(self.count-1):
            self.seed.append(random.randint(0, 4294967295))
        # 计算cost
        self.update_cost()

    def update_cost(self):
        if config.novelai_paid == 1:
            anlas = 0
            if (self.width * self.height > 409600) or self.image or self.count > 1:
                anlas += round(self.width * self.height *
                               self.strength * self.count * self.steps / 2293750)
            if self.user_id in get_driver().config.superusers:
                self.cost = 0
            else:
                self.cost = anlas
        elif config.novelai_paid == 2:
            anlas += round(self.width * self.height *
                           self.strength * self.count * self.steps / 2293750)
            if self.user_id in get_driver().config.superusers:
                self.cost = 0
            else:
                self.cost = anlas
        else:
            self.cost = 0

    def add_image(self, image):
        # 根据图片重写长宽
        tmpfile = BytesIO(image)
        image = Image.open(tmpfile)
        width, height = image.size
        self.shape_set(width, height)
        self.image = str(base64.b64encode(self.image), "utf-8")
        self.steps = 50
        self.img2img = True
        self.update_cost()

    def shape_set(self, width, height):
        base = round(min(width,height)/64)
        if base>16:
            base=16
        if width >= height:
            self.width = round(width / height * base) * 64
            self.height = 64*base
        else:
            self.height = round(height / width * base) * 64
            self.width = 64*base

    def body(self):
        pass

    def keys(self):
        return (
            "seed","scale", "strength", "noise", "sampler", "model", "steps", "width", "height", "img2img")

    def __getitem__(self, item):
        return getattr(self, item)

    def format(self):
        dict_self = dict(self)
        list=[]
        str = ""
        for i, v in dict_self.items():
            str += f"{i}={v}\n"
        list.append(str)
        list.append(f"tags={dict_self['tags']}\n")
        list.append(f"ntags={dict_self['ntags']}")
        return list
    def __repr__(self):
        return f"time={self.time}\nuser_id={self.user_id}\ngroup_id={self.group_id}\ncost={self.cost}\ncount={self.count}\n"+"".join(self.format())

    def __str__(self):
        return self.__repr__().replace("\n", ";")
