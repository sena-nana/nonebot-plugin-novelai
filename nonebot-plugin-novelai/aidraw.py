import time
import random
from collections import deque
import aiohttp
from argparse import Namespace
from asyncio import get_running_loop
from nonebot import get_bot, on_shell_command

from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment, Bot
from nonebot.rule import ArgumentParser
from nonebot.log import logger
from nonebot.params import ShellCommandArgs

from .config import config, nickname
from .utils.data import lowQuality, basetag
from .novelai import post, FIFO
from .extension.anlas import anlas_check, anlas_set
from .utils.save import save_img
from .utils.prepocess import prepocess_tags
from .version import version
from .outofdate.explicit_api import check_safe_method

cd = {}
gennerating = False
limit_list = deque([])

aidraw_parser = ArgumentParser()
aidraw_parser.add_argument("tags", default=" ", nargs="*", help="标签")
aidraw_parser.add_argument("-p", "--shape", "-形状",
                           default="p", help="画布形状", dest="shape")
aidraw_parser.add_argument("-c", "--scale", "-规模",
                           type=float, help="规模", dest="scale")
aidraw_parser.add_argument(
    "-s", "--seed", "-种子", default=random.randint(0,4294967295), type=int, help="种子", dest="seed")
aidraw_parser.add_argument("-u", "--count", "-数量",
                           type=int, default=1, help="生成数量", dest="count")
aidraw_parser.add_argument("-t", "--steps", "-步数",
                           type=int, help="步数", dest="steps")
aidraw_parser.add_argument("-n", "--ntags", "-排除",
                           default=" ", nargs="*", help="负面标签", dest="ntags")
aidraw_parser.add_argument("-r", "--strength", "-强度",
                           type=float, help="修改强度", dest="strength")
aidraw_parser.add_argument("-o", "--noise", "-噪声",
                           type=float, help="修改噪声", dest="noise")
aidraw_parser.add_argument("--nopre", "-不优化",
                           action='store_true', help="不使用内置优化参数", dest="nopre")

aidraw = on_shell_command(
    ".aidraw",
    aliases={"绘画", "咏唱", "召唤"},
    parser=aidraw_parser,
    priority=5
)


@aidraw.handle()
async def aidraw_get(bot: Bot,
                     event: GroupMessageEvent,
                     args: Namespace = ShellCommandArgs()
                     ):
    user_id = str(event.user_id)
    group_id = str(event.group_id)
    # 判断是否禁用，若没禁用，进入处理流程
    if await config.get_value(group_id, "on"):
        # 判断最大生成数量
        if args.count>config.novelai_max:
            await aidraw.send(f"批量生成数量过多，自动修改为{config.novelai_max}")
            args.count=config.novelai_max
        # 判断cd
        nowtime = time.time()
        deltatime = nowtime - cd.get(user_id, 0)
        cd_ = int(await config.get_value(group_id, "cd"))
        if (deltatime) < cd_:
            await aidraw.finish(f"你冲的太快啦，请休息一下吧，剩余CD为{cd_ - int(deltatime)}s")
        else:
            cd[user_id] = nowtime

        # 初始化参数
        fifo = FIFO(user_id=user_id, group_id=group_id, args=args)
        error = await prepocess_tags(fifo.tags) or await prepocess_tags(fifo.ntags)
        if error:
            await aidraw.finish(error)
        if not args.nopre:
            fifo.tags = basetag + await config.get_value(group_id, "tags") + "," + fifo.tags
            fifo.ntags = lowQuality + fifo.ntags

        # 以图生图预处理
        img_url = ""
        reply = event.reply
        if reply:
            for seg in reply.message['image']:
                img_url = seg.data["url"]
        for seg in event.message['image']:
            img_url = seg.data["url"]
        if img_url:
            if config.novelai_paid:
                async with aiohttp.ClientSession() as session:
                    logger.info(f"检测到图片，自动切换到以图生图，正在获取图片")
                    async with session.get(img_url) as resp:
                        fifo.add_image(await resp.read())
            else:
                await aidraw.finish(f"以图生图功能已禁用")
        logger.debug(fifo)
        # 初始化队列
        if fifo.cost > 0:
            anlascost = fifo.cost
            hasanlas = await anlas_check(fifo.user_id)
            if hasanlas >= anlascost:
                await wait_fifo(fifo, anlascost, hasanlas - anlascost)
            else:
                await aidraw.finish(f"你的点数不足，你的剩余点数为{hasanlas}")
        else:
            await wait_fifo(fifo)


async def wait_fifo(fifo, anlascost=None, anlas=None):
    # 创建队列
    list_len = get_wait_num()
    has_wait = f"排队中，你的前面还有{list_len}人"
    no_wait = "请稍等，图片生成中"
    if anlas:
        has_wait += f"\n本次生成消耗点数{anlascost},你的剩余点数为{anlas}"
        no_wait += f"\n本次生成消耗点数{anlascost},你的剩余点数为{anlas}"
    if config.novelai_limit:
        await aidraw.send(has_wait if list_len > 0 else no_wait)
        limit_list.append(fifo)
        await fifo_gennerate()
    else:
        await aidraw.send(no_wait)
        await fifo_gennerate(fifo)


def get_wait_num():
    # 获取剩余队列长度
    list_len = len(limit_list)
    if gennerating:
        list_len += 1
    return list_len


async def fifo_gennerate(fifo: FIFO = None):
    # 队列处理
    global gennerating
    bot = get_bot()

    async def generate(fifo: FIFO):
        # 开始生成
        logger.info(
            f"队列剩余{get_wait_num()}人 | 开始生成：{fifo}")
        try:
            im = await _run_gennerate(fifo)
        except Exception as e:
            logger.exception("生成失败")
            message = f"生成失败，"
            for i in e.args:
                message += i
            await bot.send_group_msg(
                message=message,
                group_id=fifo.group_id
            )
        else:
            logger.info(f"队列剩余{get_wait_num()}人 | 生成完毕：{fifo}")
            if await config.get_value(fifo.group_id, "pure"):
                message = MessageSegment.at(fifo.user_id)
                for i in im["image"]:
                    message += i
                message_data = await bot.send_group_msg(
                    message=message,
                    group_id=fifo.group_id,
                )
            else:
                message = []
                for i in im:
                    message.append(MessageSegment.node_custom(
                        bot.self_id, nickname, i))
                message_data = await bot.send_group_forward_msg(
                    messages=message,
                    group_id=fifo.group_id,
                )
            revoke = await config.get_value(fifo.group_id, "revoke")
            if revoke:
                message_id = message_data["message_id"]
                loop = get_running_loop()
                loop.call_later(
                    revoke,
                    lambda: loop.create_task(
                        bot.delete_msg(message_id=message_id)),
                )

    if fifo:
        await generate(fifo)

    if not gennerating:
        logger.info("队列开始")
        gennerating = True

        while len(limit_list) > 0:
            fifo = limit_list.popleft()
            try:
                await generate(fifo)
            except:
                logger.exception("生成中断")

        gennerating = False
        logger.info("队列结束")
        await version.check_update()


async def _run_gennerate(fifo: FIFO):
    # 处理单个请求
    img_bytes = await post(fifo)
    if isinstance(img_bytes, str):
        raise RuntimeError(img_bytes)
    message = MessageSegment.text(fifo.format())

    # 若启用ai检定，取消注释下行代码，并将构造消息体部分注释
    # message = await check_safe_method(fifo, img_bytes, message)
    # 构造消息体并保存图片
    for i in img_bytes:
        await save_img(fifo, i, fifo.group_id)
        message += MessageSegment.image(i)
    # 扣除点数
    if fifo.cost > 0:
        await anlas_set(fifo.user_id, -fifo.cost)
    return message
