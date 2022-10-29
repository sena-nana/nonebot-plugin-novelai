from dataclasses import dataclass, field
from io import BytesIO
from PIL import Image
import base64
from .config import config
from nonebot import get_driver
from .data import lowQuality
header = {
    "authorization": "Bearer " + config.novelai_token,
    ":authority": config.novelai_api_domain,
    ":path": "/ai/generate-image",
    "content-type": "application/json",
    "referer": config.novelai_site_domain,
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
}

#自动切换模型
def set_model():
    if config.novelai_h:
        return "nai-diffusion"
    else:
        return "safe-diffusion"


@dataclass
class FIFO():
    """队列中的单个请求"""
    user_id: int
    tags: str
    seed: int
    group_id: int = 0
    scale: int = 11
    strength: float = 0.7
    samper: str = "k_euler_ancestral"
    count: int = 1
    model: str = field(default_factory=set_model)
    cost: int = 0
    steps: int = 28
    noise: float = 0.2
    uc: str = ""
    width: int = 512
    height: int = 512
    image: str = field(default=None, repr=False)

    def __post_init__(self):
        #数值合法检查
        if self.steps <= 0 or self.steps > 50:
            self.steps = 28
        self.uc = lowQuality+self.uc
        self.__image_check()
        #计算cost
        if config.novelai_paid == 1:
            anlas = 0
            if (self.width*self.height > 409600) or self.image or self.count > 1:
                anlas += round(self.width*self.height *
                               self.strength*self.count*self.steps/2293750)
            if self.user_id in get_driver().config.superusers:
                self.cost = 0
            else:
                self.cost = anlas
        else:
            self.cost = 0

    def __image_check(self):
        #根据图片重写长宽
        if self.image is not None:
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
            self.steps = 50

    def body(self):
        #获取请求体
        parameters = {
            "width": self.width,
            "height": self.height,
            "qualityToggle": False,
            "scale": self.scale,
            "sampler": self.samper,
            "steps": self.steps,
            "seed": self.seed,
            "n_samples": self.count,
            "ucPreset": 0,
            "uc": self.uc,
        }
        if self.image is not None:
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
        return ("seed","tags","uc","scale","strength","noise","samper","model","steps","width","height")
    def __getitem__(self,item):
        return getattr(self,item)
    def format(self):
        dict_self=dict(self)
        str=""
        for i,v in dict_self.items():
            str+=f"{i}={v}\n"
        return str