# 基础优化tag

BASE_TAG = "masterpiece, best quality,"

# 基础排除tag
LOW_QUALITY = "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, pubic hair,long neck,blurry"

# 屏蔽词
HTAGS = "[, ][^a-zA-Z]*nsfw|nude|naked|nipple|blood|censored|vagina|gag|gokkun|hairjob|tentacle|oral|fellatio|areolae|lactation|paizuri|piercing|sex|footjob|masturbation|hips|penis|testicles|ejaculation|cum|tamakeri|pussy|pubic|clitoris|mons|cameltoe|grinding|crotch|cervix|cunnilingus|insertion|penetration|fisting|fingering|peeing|ass|buttjob|spanked|anus|anal|anilingus|enema|x-ray|wakamezake|humiliation|tally|futa|incest|twincest|pegging|femdom|ganguro|bestiality|gangbang|3P|tribadism|molestation|voyeurism|exhibitionism|rape|spitroast|cock|69|doggystyle|missionary|virgin|shibari|bondage|bdsm|rope|pillory|stocks|bound|hogtie|frogtie|suspension|anal|dildo|vibrator|hitachi|nyotaimori|vore|amputee|transformation|bloody|pornhub[^a-zA-Z]"
# 中文指令开始词
CHINESE_COMMAND = {"绘画", "咏唱", "召唤", "约稿"}

SHAPE_MAP = {
    "square": [640, 640],
    "s": [640, 640],
    "方": [640, 640],
    "portrait": [512, 768],
    "p": [512, 768],
    "高": [512, 768],
    "landscape": [768, 512],
    "l": [768, 512],
    "宽": [768, 512],
}


def aliases(*args):
    from itertools import product

    return {"".join(i) for i in product(CHINESE_COMMAND, args)}


def cs(cmd: str = "aidraw"):
    from nonebot import get_bot

    command_start = get_bot().config.command_start

    return "." + cmd if "" in command_start else cmd


async def sendtosuperuser(message):
    # 将消息发送给superuser
    import asyncio

    from nonebot import get_bot, get_driver

    superusers = get_driver().config.superusers
    bot = get_bot()
    for superuser in superusers:
        await bot.call_api(
            "send_msg",
            **{
                "message": message,
                "user_id": superuser,
            },
        )
        await asyncio.sleep(5)


from nonebot import CommandGroup

C = CommandGroup(
    cs("aidraw"),
    block=True,
)
