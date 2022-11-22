from ...config import config
from ..base.fifo import FIFO_BASE

class FIFO(FIFO_BASE):
    """队列中的单个请求"""
    model: str = "nai-diffusion" if config.novelai_h else "safe-diffusion"
    sampler: str = "k_euler_ancestral"

    def body(self, i=0):
        # 获取请求体
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
        return {
            "input": self.tags,
            "model": self.model,
            "parameters": parameters
        }