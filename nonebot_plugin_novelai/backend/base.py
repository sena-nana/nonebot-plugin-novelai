import base64
from io import BytesIO
import time
from PIL import Image
from nonebot import get_driver
from ..utils.data import shapemap
from ..config import config
import random
import aiohttp
from nonebot.log import logger
from ..utils import png2jpg


class AIDRAW_BASE():
    model: str = ""
    sampler: str = "k_euler_ancestral"
    max_resolution: int = 16

    def __init__(self,
                 user_id: str,
                 group_id: str,
                 tags: str = "",
                 seed: int = None,
                 scale: int = None,
                 strength: float = None,
                 steps: int = None,
                 batch: int = None,
                 noise: float = None,
                 ntags: str = "",
                 shape: str = "p",
                 **kwargs):
        self.time = time.strftime("%Y-%m-%d %H:%M:%S")
        self.user_id: str = user_id
        self.tags: str = tags
        self.seed: list[int] = [seed or random.randint(0, 4294967295)]
        self.group_id: str = group_id
        self.scale: int = int(scale or 11)
        self.strength: float = strength or 0.7
        self.batch: int = batch or 1
        self.steps: int = steps or 28
        self.noise: float = noise or 0.2
        self.ntags: str = ntags
        self.img2img: bool = False
        self.image: str = None
        self.width, self.height = self.extract_shape(shape)
        # 数值合法检查
        if self.steps <= 0 or self.steps > (50 if config.novelai_paid else 28):
            self.steps = 28
        if self.strength < 0 or self.strength > 1:
            self.strength = 0.7
        if self.noise < 0 or self.noise > 1:
            self.noise = 0.2
        if self.scale <= 0 or self.scale > 30:
            self.scale = 11
        # 多图时随机填充剩余seed
        for i in range(self.batch-1):
            self.seed.append(random.randint(0, 4294967295))
        # 计算cost
        self.update_cost()
        self.error: int = 0
        self.result: list = []

    def extract_shape(self, shape: str):
        if shape:
            if "x" in shape:
                width, height, *_ = shape.split("x")
                if width.isdigit() and height.isdigit():
                    return int(width), int(height)
                else:
                    return shapemap.get(shape)
            else:
                return shapemap.get(shape)
        else:
            return (512, 768)

    def update_cost(self):
        if config.novelai_paid == 1:
            anlas = 0
            if (self.width * self.height > 409600) or self.image or self.batch > 1:
                anlas = round(self.width * self.height *
                              self.strength * self.batch * self.steps / 2293750)
                if anlas < 2:
                    anlas = 2
            if self.user_id in get_driver().config.superusers:
                self.cost = 0
            else:
                self.cost = anlas
        elif config.novelai_paid == 2:
            anlas = round(self.width * self.height *
                          self.strength * self.batch * self.steps / 2293750)
            if anlas < 2:
                anlas = 2
            if self.user_id in get_driver().config.superusers:
                self.cost = 0
            else:
                self.cost = anlas
        else:
            self.cost = 0

    def add_image(self, image: bytes):
        # 根据图片重写长宽
        tmpfile = BytesIO(image)
        image_ = Image.open(tmpfile)
        width, height = image_.size
        self.shape_set(width, height)
        self.image = str(base64.b64encode(image), "utf-8")
        self.steps = 50
        self.img2img = True
        self.update_cost()

    def shape_set(self, width: int, height: int):
        limit = 1024 if config.paid else 640
        if width*height > pow(min(config.novelai_size, limit), 2):
            if width <= height:
                ratio = height/width
                width: float = config.novelai_size/pow(ratio, 0.5)
                height: float = width*ratio
            else:
                ratio = width/height
                height: float = config.novelai_size/pow(ratio, 0.5)
                width: float = height*ratio
        base = round(max(width, height)/64)
        if base > self.max_resolution:
            base = self.max_resolution
        if width <= height:
            self.width = round(width / height * base) * 64
            self.height = 64*base
        else:
            self.height = round(height / width * base) * 64
            self.width = 64*base

    # end def
    async def post_(self, header: dict, post_api: str, json: dict):
        # 请求交互
        async with aiohttp.ClientSession(headers=header) as session:
            # 向服务器发送请求
            async with session.post(post_api, json=json) as resp:
                if resp.status not in [200, 201]:
                    logger.error(await resp.text())
                    raise RuntimeError(f"与服务器沟通时发生{resp.status}错误")
                img = await self.fromresp(resp)
                logger.debug(f"获取到返回图片，正在处理")

                # 将图片转化为jpg
                image_new = await png2jpg(img)
        self.result.append(image_new)
        return image_new

    async def fromresp(self, resp):
        img: str = await resp.text()
        return img.split("data:")[1]

    def post(self):
        pass

    def keys(self):
        return (
            "seed", "scale", "strength", "noise", "sampler", "model", "steps", "width", "height", "img2img")

    def __getitem__(self, item):
        return getattr(self, item)

    def format(self):
        dict_self = dict(self)
        list = []
        str = ""
        for i, v in dict_self.items():
            str += f"{i}={v}\n"
        list.append(str)
        list.append(f"tags={self.tags}\n")
        list.append(f"ntags={self.ntags}")
        return list

    def __repr__(self):
        return f"time={self.time}\nuser_id={self.user_id}\ngroup_id={self.group_id}\ncost={self.cost}\nbatch={self.batch}\n"+"".join(self.format())

    def __str__(self):
        return self.__repr__().replace("\n", ";")
