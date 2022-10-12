import base64
import time
from pathlib import Path
import aiofiles

import aiohttp
from nonebot import get_bot, on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from nonebot.log import logger
from nonebot.params import CommandArg

from .config import config
from .data import *

path = Path("data/novelai/output").resolve()
txt2pix = on_command(".aidraw", aliases={"文本生图", "咏唱"})

cd = {}
gennerating = False
limit_list = []


@txt2pix.handle()
async def txt2pix_handle(event: GroupMessageEvent, args: Message = CommandArg()):
    nowtime = time.time()
    if (nowtime - cd.get(event.user_id, 0)) < config.novelai_cd:
        await txt2pix.finish(f"你冲的太快啦，请休息一下吧")
    else:
        cd[event.user_id] = nowtime

    message_raw = args.extract_plain_text().replace("，", ",").split(" -")
    map = [768, 512]  # h*w
    input = ""
    seed_raw = None

    for i in message_raw:
        match i:
            case "square" | "s" | "S":
                map = [640, 640]
            case "portrait" | "p" | "P":
                map = [768, 512]
            case "landscape" | "l" | "L":
                map = [512, 768]
            case _:
                if i.isdigit():
                    seed_raw = int(i)
                else:
                    input += i

    if not input:
        await txt2pix.finish(f"请描述你想要生成的角色特征(使用英文Tag,代码内已包含优化TAG)")

    if "nsfw" in input.lower():
        await txt2pix.finish("你想干嘛？生成NSFW涩图的爬一边去，这可是关乎账号的存亡啊")

    seed = seed_raw or int(time.time())
    x = (event.group_id, event.user_id, map, seed, input)

    if config.novelai_limit:
        list_len = get_wait_num()
        await txt2pix.send(
            f"排队中，你的前面还有{list_len}人，请稍安勿躁，坐和放宽～" if list_len > 0 else "请稍等，图片生成中"
        )

        limit_list.append(x)
        await run_txt2pix()

    else:
        await txt2pix.send(f"请稍等，图片生成中")
        await run_txt2pix(x)


def get_wait_num():
    list_len = len(limit_list)
    if gennerating:
        list_len += 1
    return list_len


async def run_txt2pix(x=None):
    global gennerating
    bot = get_bot()

    async def generate(y):
        group, user, map, seed, input = y

        logger.info(f"队列剩余{get_wait_num()}人 | 开始生成：{y}")
        try:
            im = await _run_txt2pix(map, seed, input)
        except:
            logger.exception("请求NovelAI接口失败")
            im = "请求NovelAI接口失败，请稍后重试"
        else:
            logger.info(f"队列剩余{get_wait_num()}人 | 生成完毕：{y}")

        await bot.send_group_msg(
            message=MessageSegment.at(user) + im,
            group_id=group,
        )

    if x:
        await generate(x)

    if not gennerating:
        logger.info("队列开始")
        gennerating = True

        while len(limit_list) > 0:
            x = limit_list.pop(0)
            await generate(x)

        gennerating = False
        logger.info("队列结束")


async def _run_txt2pix(map, seed, input):
    async with aiohttp.ClientSession(
        config.novelai_api_domain, headers=header
    ) as session:
        async with session.post(
            "/ai/generate-image", json=txt2pix_body(seed, input, map)
        ) as resp:
            if resp.status != 201:
                return f"生成失败，错误代码为{resp.status}"

            img = await resp.text()

        img_bytes = img.split("data:")[1]

        if config.novelai_save_pic:
            if not path.exists():
                path.mkdir(parents=True)

            img = base64.b64decode(img_bytes)
            async with aiofiles.open(str(path / f"{seed} {input[:100]}", "wb")) as f:
                await f.write(img)

        return f"Seed: {seed}" + MessageSegment.image(f"base64://{img_bytes}")
