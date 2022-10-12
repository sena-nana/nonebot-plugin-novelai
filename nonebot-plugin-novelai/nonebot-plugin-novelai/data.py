import urllib.parse
from .config import config

lowQuality = "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, "
basetag = "{masterpiece}, extremely detailed 8k wallpaper, best quality, an extremely delicate and beautiful, "
token = config.novelai_token
header = {
    "authorization": "Bearer " + token,
    ":authority": urllib.parse.urlparse(config.novelai_api_domain).hostname,
    ":path": "/ai/generate-image",
    "content-type": "application/json",
    "referer": config.novelai_site_domain,
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
}


def txt2pix_body(seed, input, map):
    return {
        "input": input + basetag + config.novelai_tag,
        "model": "safe-diffusion",
        "parameters": {
            "width": map[1],
            "height": map[0],
            "scale": 11,
            "sampler": "k_euler_ancestral",
            "steps": 28,
            "seed": seed,
            "n_samples": 1,
            "ucPreset": 0,
            "uc": lowQuality,
        },
    }

