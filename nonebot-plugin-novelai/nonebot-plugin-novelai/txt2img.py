import base64
import time
from pathlib import Path
import aiofiles

import aiohttp
from nonebot import get_bot, on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from nonebot.log import logger
from nonebot.params import CommandArg
import re

from .config import config
from .data import txt2img_body,header,htags,img2img_body
from .utils import is_contain_chinese,translate_ZH2EN,file_name_check
from .version import check_update

path = Path("data/novelai").resolve()
txt2img = on_command(".aidraw", aliases={"文本生图", "咏唱"})

cd = {}
gennerating = False
limit_list = []

@txt2img.handle()
async def txt2img_handle(event: GroupMessageEvent, args: Message = CommandArg()):
    message_raw = args.extract_plain_text().replace("，", ",").split("-")
    count=1
    #以图生图预处理
    img_url=[]
    for seg in event.message['image']:
        img_url.append(seg.data["url"])
    imgbytes:list[str]=[]
    if img_url:
        if config.novelai_paid:
            async with aiohttp.ClientSession() as session:
                logger.info(f"正在获取图片")
                for i in img_url:
                    async with session.get(i) as resp:
                        imgbytes.append(await resp.read())
        else:
            await txt2img.finish(f"以图生图功能已禁用")
    if len(imgbytes)>config.novelai_oncemax:
        await txt2img.finish(f"最大只能同时生成{config.novelai_oncemax}张")

    #功能开关
    match message_raw[0]:
        case "off":
            result=config.set_enable(event.group_id,False)
            logger.info(result)
            txt2img.finish(result)
        case "on":
            result=config.set_enable(event.group_id,True)
            logger.info(result)
            txt2img.finish(result)

    #判断是否禁用，若没禁用，进入处理流程
    if event.group_id not in config.novelai_ban:

        # 判断cd
        nowtime = time.time()
        if (nowtime - cd.get(event.user_id, 0)) < config.novelai_cd:
            await txt2img.finish(f"你冲的太快啦，请休息一下吧")
        else:
            cd[event.user_id] = nowtime

        map = [768, 512]  # h*w
        input = ""
        seed_raw = None
        nopre=False

        #提取参数
        for i in message_raw:
            match i:
                case "square" | "s":
                    map = [640, 640]
                case "portrait" | "p":
                    map = [768, 512]
                case "landscape" | "l":
                    map = [512, 768]
                case "nopre"|"np":
                    nopre=True
                case _:
                    if i.isdigit():
                        seed_raw = int(i)
                    else:
                        input += i

        if not input:
            await txt2img.finish(f"请描述你想要生成的角色特征(使用英文Tag,代码内已包含优化TAG)")

        # 检测是否有18+词条
        if config.novelai_h:
            for i in htags:
                if i in input.lower():
                    await txt2img.finish("H是不行的!")

        # 处理奇奇怪怪的输入
        input=re.sub("\s","",input)
        input=file_name_check(input)

        #生成种子
        seed = seed_raw or int(time.time())

        #检测中文
        if is_contain_chinese(input):
            input=await translate_ZH2EN(input)
            logger.info(f"检测到中文，机翻结果为{input}")

        if config.novelai_limit:
            messagepack = (event.group_id, event.user_id, map, seed, input,imgbytes)
            list_len = get_wait_num()
            await txt2img.send(
                f"排队中，你的前面还有{list_len}人" if list_len > 0 else "请稍等，图片生成中"
            )
            limit_list.append(messagepack)
            await run_txt2img()

        else:
            await txt2img.send(f"请稍等，图片生成中")
            messagepack = (event.group_id, event.user_id, map, seed, input,imgbytes)
            await run_txt2img(messagepack)


def get_wait_num():
    list_len = len(limit_list)
    if gennerating:
        list_len += 1
    return list_len



async def run_txt2img(messagepack=None):
    global gennerating
    bot = get_bot()

    async def generate(messagepack):
        group, user, map, seed, input ,imgbytes= messagepack

        logger.info(f"队列剩余{get_wait_num()}人 | 开始生成：{group},{user},{input}")
        try:
            if imgbytes:
                im = await _run_img2img(map, seed, input,imgbytes)
            else:
                im = await _run_txt2img(map, seed, input)
        except:
            logger.exception("生成失败")
            im = "生成失败，请联系BOT主排查原因"
        else:
            logger.info(f"队列剩余{get_wait_num()}人 | 生成完毕：{messagepack}")

        await bot.send_group_msg(
            message=MessageSegment.at(user) + im,
            group_id=group,
        )

    if messagepack:
        await generate(messagepack)

    if not gennerating:
        logger.info("队列开始")
        gennerating = True

        while len(limit_list) > 0:
            messagepack = limit_list.pop(0)
            try:
                await generate(messagepack)
            except:
                logger.exception("生成中断")

        gennerating = False
        logger.info("队列结束")
        await check_update()


async def _run_txt2img(map, seed, input):
    async with aiohttp.ClientSession(
        config.novelai_api_domain, headers=header
    ) as session:
        async with session.post(
            "/ai/generate-image", json=txt2img_body(seed, input, map)
        ) as resp:
            if resp.status != 201:
                return f"生成失败，错误代码为{resp.status}"

            img = await resp.text()

        img_bytes = img.split("data:")[1]

        await save_img(seed, input, img_bytes)
        return f"Seed: {seed}" + MessageSegment.image(f"base64://{img_bytes}")

async def _run_img2img(map, seed, input,rawimg):
    img_byteslist=[]
    async with aiohttp.ClientSession(
        config.novelai_api_domain, headers=header
    ) as session:
        for i in rawimg:
            async with session.post(
                "/ai/generate-image", json=img2img_body(seed, input,i)
            ) as resp:
                if resp.status != 201:
                    return f"生成失败，错误代码为{resp.status}"
                img = await resp.text()
                img_bytes=img.split("data:")[1]
            img_byteslist.append(img_bytes)
            await save_img(seed, input, img_bytes)
    message=f"Seed: {seed}"
    for img_bytes in img_byteslist:
        message += MessageSegment.image(f"base64://{img_bytes}")
    return  message


async def save_img(seed, input, img_bytes):
    if config.novelai_save_pic:
        if not path.exists():
            path.mkdir(parents=True)
        img = base64.b64decode(img_bytes)
        async with aiofiles.open(
                str(path/"output"/f"{seed} {input[:100]}.png"), "wb"
            ) as f:
            await f.write(img)