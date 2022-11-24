from .base import AIDRAW_BASE
from ..config import config


class AIDRAW(AIDRAW_BASE):
    """队列中的单个请求"""
    sampler: str = "k_euler_ancestral"
    max_resolution: int = 32

    async def fromresp(self, resp):
        img: dict = await resp.json()
        return img["images"][0]

    async def post(self):
        site=config.novelai_site or "127.0.0.1:7860"
        header = {
            "content-type": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        }
        post_api = f"http://{site}/sdapi/v1/img2img" if self.img2img else f"http://{site}/sdapi/v1/txt2img"
        for i in range(self.batch):
            parameters = {
                "prompt": self.tags,
                "seed": self.seed[i],
                "steps": self.steps,
                "cfg_scale": self.scale,
                "width": self.width,
                "height": self.height,
                "negative_prompt": self.ntags,
            }
            if self.img2img:
                parameters.update({
                    "init_images": ["data:image/jpeg;base64,"+self.image],
                    "denoising_strength": self.strength,
                })
            await self.post_(header, post_api, parameters)
        return self.result
