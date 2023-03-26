from .base import AIDRAW_BASE
from ..config import config
class AIDRAW(AIDRAW_BASE):
    """队列中的单个请求"""

    async def post(self):
        header = {
            "content-type": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        }
        site=config.novelai_site or "127.0.0.1:6969"
        post_api="http://"+site + "/generate-stream"
        for i in range(self.batch):
            parameters = {
                "prompt":self.tags,
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
            await self.post_(header, post_api,parameters)
        return self.result