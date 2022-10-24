import base64
import time
from pathlib import Path
import aiofiles

import aiohttp
from nonebot import get_bot, get_driver, on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment, Bot
from nonebot.log import logger
from nonebot.params import CommandArg
import re
import hashlib
from .config import config
from .requests import body, header, htags
from .utils import is_contain_chinese, file_name_check
from .utils.translation import translate
from .version import version
from .utils.anlas import anlas_check, anlas_set
from .fifo import IMG, FIFO
from nonebot.adapters.onebot.v11 import GROUP_ADMIN, GROUP_OWNER
path = Path("data/novelai/output").resolve()
txt2img = on_command(".aidraw", aliases={"绘画", "咏唱", "约稿", "召唤"})

cd = {}
gennerating = False
limit_list = []
nickname = ""
for i in get_driver().config.nickname:
    nickname = i


@txt2img.handle()
async def txt2img_handle(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    message_raw = args.extract_plain_text().replace("，", ",").split("-")
    user_id = str(event.user_id)
    count = 1
    # 以图生图预处理
    img_url = []
    for seg in event.message['image']:
        img_url.append(seg.data["url"])
    imgbytes = []
    if img_url:
        if config.novelai_paid:
            async with aiohttp.ClientSession() as session:
                logger.info(f"检测到图片，自动切换到以图生图，正在获取图片")
                for i in img_url:
                    async with session.get(i) as resp:
                        imgbytes.append(await resp.read())
        else:
            await txt2img.finish(f"以图生图功能已禁用")
    if len(imgbytes)*count > config.novelai_oncemax:
        await txt2img.finish(f"最大只能同时生成{config.novelai_oncemax}张")

    managetag = None
    managelist = message_raw[0].split()
    match managelist:
        case ["off"]:
            managetag = False
        case ["on"]:
            managetag = True
        case ["set"]:
            group_config = await config.get_groupconfig(event.group_id)
            message = "当前群的设置为\n"
            for i, v in group_config.items():
                message += f"{i}:{v}\n"
            await txt2img.finish(message)
        case ["set", arg, value]:
            if await GROUP_ADMIN(bot, event) or await GROUP_OWNER(bot, event):
                await txt2img.finish(f"设置群聊{arg}为{value}完成" if await config.set_value(event.group_id, arg, value) else f"不正确的赋值")
    if managetag is not None:
        if await GROUP_ADMIN(bot, event) or await GROUP_OWNER(bot, event):
            result = await config.set_enable(event.group_id, managetag)
            logger.info(result)
            await txt2img.finish(result)
        else:
            await txt2img.finish(f"只有管理员可以使用管理功能")
    # 判断是否禁用，若没禁用，进入处理流程
    if await config.get_value(event.group_id,"on") is not None:
        # 判断cd
        nowtime = time.time()
        deltatime = nowtime - cd.get(user_id, 0)
        cd_ = int(await config.get_value(event.group_id, "cd"))
        if (deltatime) < cd_:
            await txt2img.finish(f"你冲的太快啦，请休息一下吧，剩余CD为{cd_-int(deltatime)}s")
        else:
            cd[user_id] = nowtime

        width, height = [512, 768]  # w*h
        tags = ""
        seed_raw = None
        nopre = False

        # 提取参数
        for i in message_raw:
            i = i.strip()
            match i:
                case "square" | "s":
                    width, height = [640, 640]
                case "portrait" | "p":
                    width, height = [512, 768]
                case "landscape" | "l":
                    width, height = [768, 512]
                case "nopre" | "np":
                    nopre = True
                case _:
                    if i.isdigit():
                        seed_raw = int(i)
                    else:
                        tags += i

        # 处理奇奇怪怪的输入
        tags = re.sub("\s", "", tags)
        tags = file_name_check(tags)

        # 生成种子
        seed = seed_raw or int(time.time())

        # 检测中文
        taglist = tags.split(",")
        tagzh = ""
        tags_ = ""
        for i in taglist:
            if is_contain_chinese(tags):
                tagzh += f"{i},"
            else:
                tags_ += f"{i},"
        if tagzh:
            tags_en = await translate(tagzh, "en")
            if tags_en == tagzh:
                await txt2img.finish(f"检测到中文，翻译失败，生成终止，请联系BOT主查看后台")
            else:
                tags_ += tags_en
        logger.info(f"获取到词条{tags_}")
        tags=tags_

        # 检测是否有18+词条
        if not config.novelai_h:
            pattern=re.compile(f"(\s|,|^)({htags})(\s|,|$)")
            if(re.search(pattern,tags)is not None):
                await txt2img.finish("H是不行的!")

        if imgbytes:
            data_img = []
            for i in imgbytes:
                data_img.append(IMG(image=i))
            fifo = FIFO(user_id, tags, seed, data_img, event.group_id)
        else:
            data_txt = [IMG(width=width, height=height)]
            fifo = FIFO(user_id, tags, seed, data_txt, event.group_id)
        if fifo.cost > 0:
            anlascost = fifo.cost
            hasanlas = await anlas_check(fifo.user_id)
            if hasanlas >= anlascost:
                await wait_fifo(fifo, anlascost, hasanlas-anlascost)
            else:
                await txt2img.finish(f"你的点数不足，你的剩余点数为{hasanlas}")
        else:
            await wait_fifo(fifo)


async def wait_fifo(fifo, anlascost=None, anlas=None):
    list_len = get_wait_num()
    has_wait = f"排队中，你的前面还有{list_len}人"
    no_wait = "请稍等，图片生成中"
    if anlas:
        has_wait += f"\n本次生成消耗点数{anlascost},你的剩余点数为{anlas}"
        no_wait += f"\n本次生成消耗点数{anlascost},你的剩余点数为{anlas}"
    if config.novelai_limit:
        await txt2img.send(has_wait if list_len > 0 else no_wait)
        limit_list.append(fifo)
        await fifo_gennerate()
    else:
        await txt2img.send(no_wait)
        await fifo_gennerate(fifo)


def get_wait_num():
    list_len = len(limit_list)
    if gennerating:
        list_len += 1
    return list_len


async def fifo_gennerate(fifo: FIFO = None):
    global gennerating
    bot = get_bot()

    async def generate(fifo: FIFO):

        logger.info(
            f"队列剩余{get_wait_num()}人 | 开始生成：{fifo}")
        try:
            im = await _run_gennerate(fifo)
        except:
            logger.exception("生成失败")
            im = "生成失败，请联系BOT主排查原因"
        else:
            logger.info(f"队列剩余{get_wait_num()}人 | 生成完毕：{fifo}")

        await bot.send_group_msg(
            message=MessageSegment.at(fifo.user_id) + im,
            group_id=fifo.group_id,
        )

    if fifo:
        await generate(fifo)

    if not gennerating:
        logger.info("队列开始")
        gennerating = True

        while len(limit_list) > 0:
            fifo = limit_list.pop(0)
            try:
                await generate(fifo)
            except:
                logger.exception("生成中断")

        gennerating = False
        logger.info("队列结束")
        await version.check_update()


async def _run_gennerate(fifo: FIFO):
    img_bytes = []
    async with aiohttp.ClientSession(headers=header) as session:
        for i in fifo.data:
            async with session.post(
                config.novelai_api_domain+"ai/generate-image", json=await body(fifo.seed, fifo.tags, i.width, i.height, fifo.group_id, i.image)
            ) as resp:
                if resp.status != 201:
                    return f"生成失败，错误代码为{resp.status}"
                img = await resp.text()
                img_bytes.append(img.split("data:")[1])
    message = f"Seed: {fifo.seed}\nTags:{fifo.tags}\n"
    if config.novelai_h:
        for i in img_bytes:
            await save_img(fifo.seed, fifo.tags, i)
            message += MessageSegment.image(f"base64://{i}")
        if fifo.cost > 0:
            await anlas_set(fifo.user_id, -fifo.cost)
        return message
    else:
        nsfw_count = 0
        for i in img_bytes:
            try:
                label = await check_safe(i)
            except RuntimeError:
                logger.error(f"NSFWAPI调用失败，错误代码为{RuntimeError.args}")
                message += f"{nickname}无法判断图片是否合规(API调用失败)\n"
                label = "unknown"
                for j in img_bytes:
                    await save_img(fifo.seed, fifo.tags, j)
                    message += MessageSegment.image(f"base64://{j}")
                if fifo.cost > 0:
                    await anlas_set(fifo.user_id, -fifo.cost)
                return message
            if label == "safe" or label == "questionable":
                message += MessageSegment.image(f"base64://{i}")
            else:
                nsfw_count += 1
            await save_img(fifo.seed, fifo.tags, i, label)
        message += f"\n有{nsfw_count}张图片太涩了，{nickname}已经帮你吃掉了哦" if nsfw_count > 0 else f"\n"
        if fifo.cost > 0:
            await anlas_set(fifo.user_id, -fifo.cost)
        return message


async def save_img(seed, tags, img_bytes, extra: str = "unknown"):
    if config.novelai_save_pic:
        path_ = path/extra
        path_.mkdir(parents=True, exist_ok=True)
        img = base64.b64decode(img_bytes)
        hash = hashlib.md5(img).hexdigest()
        if len(tags) > 100:
            async with aiofiles.open(
                str(path_/f"{seed}_{hash}_{tags[:100]}.png"), "wb"
            ) as f:
                await f.write(img)
        else:
            async with aiofiles.open(
                str(path_/f"{seed}_{hash}_{tags}.png"), "wb"
            ) as f:
                await f.write(img)


async def check_safe(img_bytes):
    start = "data:image/jpeg;base64,"
    str0 = start+img_bytes
    async with aiohttp.ClientSession() as session:
        async with session.post('https://hf.space/embed/mayhug/rainchan-image-porn-detection/api/predict/', json={"data": [str0]}) as resp:
            if resp.status != 200:
                raise RuntimeError(resp.status)
            jsonresult = await resp.json()
            return jsonresult["data"][0]["label"]
