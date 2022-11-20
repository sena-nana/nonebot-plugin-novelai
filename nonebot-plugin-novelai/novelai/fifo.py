import base64
from io import BytesIO
import datetime
from PIL import Image
from nonebot import get_driver
from ..utils.data import shapemap
from ..config import config
import random
header = {
    "authorization": "Bearer " + config.novelai_token,
    ":authority": config.novelai_api_domain,
    ":path": "/ai/generate-image",
    "content-type": "application/json",
    "referer": config.novelai_site_domain,
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
}

# 自动切换模型


class FIFO():
    """队列中的单个请求"""
    model: str = "nai-diffusion" if config.novelai_h else "safe-diffusion"
    samper: str = "k_euler_ancestral"

    def __init__(self, user_id, group_id, args):
        self.time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.user_id: str = user_id
        self.tags: str = "".join([i+" " for i in args.tags])
        self.seed: list[int] = [args.seed]
        self.group_id: str = group_id
        self.scale: int = int(args.scale or 11)
        self.strength: float = args.strength or 0.7
        self.count: int = args.count
        self.steps: int = args.steps or 28
        self.noise: float = args.noise or 0.2
        self.ntags: str = args.ntags or " "
        self.img2img: bool = False
        self.image: str = None
        self.width, self.height = shapemap.get(args.shape, [512, 768])
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
        else:
            self.cost = 0

    def add_image(self, image):
        # 根据图片重写长宽
        tmpfile = BytesIO(image)
        image = Image.open(tmpfile)
        width, height = image.size
        if width >= height:
            self.width = round(width / height * 8) * 64
            self.height = 512
        else:
            self.height = round(height / width * 8) * 64
            self.width = 512
        self.image = str(base64.b64encode(self.image), "utf-8")
        self.steps = 50
        self.img2img = True
        self.update_cost()

    def body(self, i=0):
        # 获取请求体
        parameters = {
            "width": self.width,
            "height": self.height,
            "qualityToggle": False,
            "scale": self.scale,
            "sampler": self.samper,
            "steps": self.steps,
            "seed": self.seed[i],
            "n_samples": 1,
            "ucPreset": 0,
            "uc": self.ntags,
        }
        if self.img2img:
            parameters.update({
                "image": self.image,
                "strength": self.strength,
                "noise": self.noise
            })
        return {
            "input": self.tags,
            "model": self.model,
            "parameters": parameters
        }

    def keys(self):
        return (
            "seed", "tags", "ntags", "scale", "strength", "noise", "samper", "model", "steps", "width", "height", "img2img")

    def __getitem__(self, item):
        return getattr(self, item)

    def format(self):
        dict_self = dict(self)
        str = ""
        for i, v in dict_self.items():
            str += f"{i}={v}\n"
        return str

    def __repr__(self):
        return f"time={self.time}\nuser_id={self.user_id}\ngroup_id={self.group_id}\ncost={self.cost}\ncount={self.count}\n"+self.format()

    def __str__(self):
        return self.__repr__().replace("\n", ";")
