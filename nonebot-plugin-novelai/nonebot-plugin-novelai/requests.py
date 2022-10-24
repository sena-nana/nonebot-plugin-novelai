import urllib.parse
from .config import config
lowQuality = "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, pubic hair,long neck,blurry"
htags = "nsfw|nude|naked|nipple|blood|censored|vagina|gag|gokkun|hairjob|tentacle|oral|fellatio|areolae|lactation|paizuri|piercing|sex|footjob|masturbation|hips|penis|testicles|ejaculation|cum|tamakeri|pussy|pubic|clitoris|mons|cameltoe|grinding|crotch|cervix|cunnilingus|insertion|penetration|fisting|fingering|peeing|ass|buttjob|spanked|anus|anal|anilingus|enema|x-ray|wakamezake|humiliation|tally|futa|incest|twincest|pegging|femdom|ganguro|bestiality|gangbang|3P|tribadism|molestation|voyeurism|exhibitionism|rape|spitroast|cock|69|doggystyle|missionary|virgin|shibari|bondage|bdsm|rope|pillory|stocks|bound|hogtie|frogtie|suspension|anal|dildo|vibrator|hitachi|nyotaimori|vore|amputee|transformation"
basetag = "masterpiece, best quality,"
token = config.novelai_token
header = {
    "authorization": "Bearer " + token,
    ":authority": urllib.parse.urlparse(config.novelai_api_domain).hostname,
    ":path": "/ai/generate-image",
    "content-type": "application/json",
    "referer": config.novelai_site_domain,
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
}

async def body(seed,input,width,height,group_id,image=None):
    if config.novelai_h:
        model="nai-diffusion"
    else:
        model="safe-diffusion"
    uc = lowQuality
    parameters={
            "width": width,
            "height": height,
            "qualityToggle": True,
            "scale": 11,
            "sampler": "k_euler_ancestral",
            "steps": 50,
            "seed": seed,
            "n_samples": 1,
            "ucPreset": 0,
            "uc": uc,
        }
    if image:
        parameters.update({
            "image":image,
            "strength":0.7,
            "noise":0.2
        })
    return {
        "input": basetag + await config.get_value(group_id,"tag") + "," + input,
        "model": model,
        "parameters": parameters
    }
