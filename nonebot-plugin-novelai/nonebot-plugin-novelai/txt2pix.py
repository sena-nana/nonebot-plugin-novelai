from nonebot import on_command, get_bot
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import MessageSegment, Message, GroupMessageEvent
from .data import *
import aiohttp
import base64
import time
from pathlib import Path
from .config import config
from nonebot.log import logger

path = Path("data/novelai/output").resolve()
txt2pix = on_command(".aidraw", aliases={"文本生图", "咏唱"})

cd = {}
gennerating = False
limit_list = []


@txt2pix.handle()
async def txt2pix_handle(event: GroupMessageEvent, args: Message = CommandArg()):
    global cd,limit_list,gennerating
    nowtime = time.time()
    if (nowtime-cd.get(event.user_id, 0)) < config.novelai_cd:
        await txt2pix.finish(f"你冲的太快啦，请休息一下吧")
    else:
        cd[event.user_id] = nowtime
    message_raw = args.extract_plain_text().replace("，", ",").split("-")
    map = [768, 512]
    input = ""
    seed_raw = None
    for i in message_raw:
        match i:
            case "square" | "s" | "S":
                map = [640, 640]
            case "portrait" | "p" | "P":
                map = [768, 512]
            case 'landscape' | "l" | "L":
                map = [512, 768]
            case _:
                if i.isdigit():
                    seed_raw = int(i)
                else:
                    input += i
    if not input:
        await txt2pix.finish(f"请描述你想要生成的角色特征(使用英文Tag,代码内已包含优化TAG)")
    seed = seed_raw or int(time.time())
    if config.novelai_limit:
        limit_list.append((event.group_id, event.user_id, map, seed, input))
        await txt2pix.send(f"排队中，你的前面还有{len(limit_list)-1}人")
        if not gennerating:
            await run_txt2pix(None)
    else:
        await run_txt2pix((event.group_id, event.user_id, map, seed, input))


async def run_txt2pix(x):
    global cd,limit_list,gennerating
    groupid, userid, map, seed, input = x or limit_list.pop(0)
    if x == None and not gennerating:
        gennerating = True
        logger.debug(f"novelai开始工作")
    bot = get_bot()
    logger.debug(f"novelai开始生成"+input+f",剩余{len(limit_list)}人")
    async with aiohttp.ClientSession("https://api.novelai.net/", headers=header) as session:
        async with session.post("/ai/generate-image", json=txt2pix_body(seed, input, map)) as resp:
            if resp.status != 201:
                await bot.call_api(
                    "send_group_msg", **{
                        "message": f"生成失败，错误代码为"+str(resp.status),
                        "group_id": groupid,
                    },
                )
            img = await resp.text()
            img_bytes = img.split("data:")[1]
            img = base64.b64decode(img_bytes)
            if len(input) > 100:
                input = input[:100]
            img_name = input+str(seed)+".png"
            path.mkdir(parents=True, exist_ok=True)
            with open(path/img_name, "wb") as f:
                f.write(img)
            message = MessageSegment.at(
                userid)+str(seed)+MessageSegment.image("base64://"+img_bytes)
            await bot.call_api(
                "send_group_msg", **{
                    "message": message,
                    "group_id": groupid,
                },
            )
            logger.debug(f"novelai生成完成"+input)
    if x == None:
        if len(limit_list)>0:
            await run_txt2pix(None)
        else:
            gennerating = False
            logger.debug(f"novelai开始休息")
