
from nonebot import get_driver
from .config import config
lowQuality = 'lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry,nsfw,'
basetag="masterpiece,extremely detailed,best quality,"
token=get_driver().config.novelai_token
header={
        "authorization":'Bearer '+token,
        ":authority": 'api.novelai.net',
        ":path":'/ai/generate-image',
        'content-type': 'application/json',
        "referer":'https://novelai.net/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    }
def txt2pix_body(seed,input,map):
    return {
            "input":input+basetag+config.novelai_tag,
            "model":"safe-diffusion",
            "parameters":{
                "width":map[1],
                "height":map[0],
                "scale":11,
                "sampler":"k_euler_ancestral",
                "steps":28,
                "seed":seed,
                "n_samples":1,
                "ucPreset":0,
                "uc":lowQuality,
                }
        }