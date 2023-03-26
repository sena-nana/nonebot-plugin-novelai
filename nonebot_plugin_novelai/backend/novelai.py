from ..config import config
from .base import AIDRAW_BASE

class AIDRAW(AIDRAW_BASE):
    """队列中的单个请求"""
    model: str = "nai-diffusion" if config.novelai_h else "safe-diffusion"

    async def post(self):
        # 获取请求体
        header = {
            "authorization": "Bearer " + config.novelai_token,
            ":authority": "https://api.novelai.net",
            ":path": "/ai/generate-image",
            "content-type": "application/json",
            "referer": "https://novelai.net",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        }
        post_api = "https://api.novelai.net/ai/generate-image"
        for i in range(self.batch):
            parameters = {
                "width": self.width,
                "height": self.height,
                "qualityToggle": False,
                "scale": self.scale,
                "sampler": self.sampler,
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
            json= {
                "input": self.tags,
                "model": self.model,
                "parameters": parameters
            }
            await self.post_(header, post_api,json)
        return self.result