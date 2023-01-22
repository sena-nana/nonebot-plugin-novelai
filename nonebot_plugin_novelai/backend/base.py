import asyncio
import base64
import random
import time
from io import BytesIO

import aiohttp
from nonebot import get_driver
from nonebot.log import logger
from PIL import Image

from ..config import config
from ..utils import png2jpg
from ..utils.data import shapemap


class AIDRAW_BASE:
    max_resolution: int = 16
    sampler: str

    def __init__(
        self,
        user_id: str,
        group_id: str,
        tags: str = "",
        ntags: str = "",
        seed: int = None,
        scale: int = None,
        steps: int = None,
        batch: int = None,
        strength: float = None,
        noise: float = None,
        shape: str = "p",
        model: str = None,
        **kwargs,
    ):
        """
        AI绘画的核心部分,将与服务器通信的过程包装起来,并方便扩展服务器类型

        :user_id: 用户id,必须
        :group_id: 群聊id,如果是私聊则应置为0,必须
        :tags: 图像的标签
        :ntags: 图像的反面标签
        :seed: 生成的种子，不指定的情况下随机生成
        :scale: 标签的参考度，值越高越贴近于标签,但可能产生过度锐化。范围为0-30,默认11
        :steps: 训练步数。范围为1-50,默认28.以图生图时强制50
        :batch: 同时生成数量
        :strength: 以图生图时使用,变化的强度。范围为0-1,默认0.7
        :noise: 以图生图时使用,变化的噪音,数值越大细节越多,但可能产生伪影,不建议超过strength。范围0-1,默认0.2
        :shape: 图像的形状，支持"p""s""l"三种，同时支持以"x"分割宽高的指定分辨率。
                该值会被设置限制，并不会严格遵守输入
                类初始化后,该参数会被拆分为:width:和:height:
        :model: 指定的模型，模型名称在配置文件中手动设置。不指定模型则按照负载均衡自动选择

        AIDRAW还包含了以下几种内置的参数
        :status: 记录了AIDRAW的状态,默认为0等待中(处理中)
                非0的值为运行完成后的状态值,200和201为正常运行,其余值为产生错误
        :result: 当正常运行完成后,该参数为一个包含了生成图片bytes信息的数组
        :maxresolution: 一般不用管，用于限制不同服务器的最大分辨率
                如果你的SD经过了魔改支持更大分辨率可以修改该值并重新设置宽高
        :cost: 记录了本次生成需要花费多少点数，自动计算
        :signal: asyncio.Event类,可以作为信号使用。仅占位，需要自行实现相关方法
        """
        self.status: int = 0
        self.result: list = []
        self.signal: asyncio.Event = None
        self.model = model
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
        for i in range(self.batch - 1):
            self.seed.append(random.randint(0, 4294967295))
        # 计算cost
        self.update_cost()

    def extract_shape(self, shape: str):
        """
        将shape拆分为width和height
        """
        if shape:
            if "x" in shape:
                width, height, *_ = shape.split("x")
                if width.isdigit() and height.isdigit():
                    return self.shape_set(int(width), int(height))
                else:
                    return shapemap.get(shape)
            else:
                return shapemap.get(shape)
        else:
            return (512, 768)

    def update_cost(self):
        """
        更新cost
        """
        if config.novelai_paid == 1:
            anlas = 0
            if (self.width * self.height > 409600) or self.image or self.batch > 1:
                anlas = round(
                    self.width
                    * self.height
                    * self.strength
                    * self.batch
                    * self.steps
                    / 2293750
                )
                if anlas < 2:
                    anlas = 2
            if self.user_id in get_driver().config.superusers:
                self.cost = 0
            else:
                self.cost = anlas
        elif config.novelai_paid == 2:
            anlas = round(
                self.width
                * self.height
                * self.strength
                * self.batch
                * self.steps
                / 2293750
            )
            if anlas < 2:
                anlas = 2
            if self.user_id in get_driver().config.superusers:
                self.cost = 0
            else:
                self.cost = anlas
        else:
            self.cost = 0

    def add_image(self, image: bytes):
        """
        向类中添加图片，将其转化为以图生图模式
        也可用于修改类中已经存在的图片
        """
        # 根据图片重写长宽
        tmpfile = BytesIO(image)
        image_ = Image.open(tmpfile)
        width, height = image_.size
        self.width, self.height = self.shape_set(width, height)
        self.image = str(base64.b64encode(image), "utf-8")
        self.steps = 50
        self.img2img = True
        self.update_cost()

    def shape_set(self, width: int, height: int):
        """
        设置宽高
        """
        limit = 1024 if config.paid else 640
        if width * height > pow(min(config.novelai_size, limit), 2):
            if width <= height:
                ratio = height / width
                width: float = config.novelai_size / pow(ratio, 0.5)
                height: float = width * ratio
            else:
                ratio = width / height
                height: float = config.novelai_size / pow(ratio, 0.5)
                width: float = height * ratio
        base = round(max(width, height) / 64)
        if base > self.max_resolution:
            base = self.max_resolution
        if width <= height:
            return (round(width / height * base) * 64, 64 * base)
        else:
            return (64 * base, round(height / width * base) * 64)

    async def post_(self, header: dict, post_api: str, json: dict):
        """
        向服务器发送请求的核心函数，不要直接调用，请使用post函数
        :header: 请求头
        :post_api: 请求地址
        :json: 请求体
        """
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
                if config.novelai_save == 1:
                    image_new = await png2jpg(img)
                else:
                    image_new = base64.b64decode(img)
        self.result.append(image_new)
        return image_new

    async def fromresp(self, resp):
        """
        处理请求的返回内容，不要直接调用，请使用post函数
        """
        img: str = await resp.text()
        return img.split("data:")[1]

    def run(self):
        """
        运行核心函数，发送请求并处理
        """
        pass

    def keys(self):
        return (
            "seed",
            "scale",
            "strength",
            "noise",
            "sampler",
            "model",
            "steps",
            "width",
            "height",
            "img2img",
        )

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
        return (
            f"time={self.time}\nuser_id={self.user_id}\ngroup_id={self.group_id}\ncost={self.cost}\nbatch={self.batch}\n"
            + "".join(self.format())
        )

    def __str__(self):
        return self.__repr__().replace("\n", ";")
