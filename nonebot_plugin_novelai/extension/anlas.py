from pathlib import Path
import json
import aiofiles
from nonebot.adapters.onebot.v11 import Bot,GroupMessageEvent, Message, MessageSegment
from nonebot.permission import SUPERUSER
from nonebot.params import CommandArg
from nonebot import on_command, get_driver

jsonpath = Path("data/novelai/anlas.json").resolve()
setanlas = on_command(".anlas")

@setanlas.handle()
async def anlas_handle(bot:Bot,event: GroupMessageEvent, args: Message = CommandArg()):
    atlist = []
    user_id = str(event.user_id)
    for seg in event.original_message["at"]:
        atlist.append(seg.data["qq"])
    messageraw = args.extract_plain_text().strip()
    if not messageraw or messageraw == "help":
        await setanlas.finish(f"点数计算方法(四舍五入):分辨率*数量*强度/45875\n.anlas+数字+@某人 将自己的点数分给对方\n.anlas check 查看自己的点数")
    elif messageraw == "check":
        if await SUPERUSER(bot,event):
            await setanlas.finish(f"Master不需要点数哦")
        else:
            anlas = await anlas_check(user_id)
            await setanlas.finish(f"你的剩余点数为{anlas}")
    if atlist:
        at = atlist[0]
        if messageraw.isdigit():
            anlas_change = int(messageraw)
            if anlas_change > 1000:
                await setanlas.finish(f"一次能给予的点数不超过1000")
            if await SUPERUSER(bot,event):
                _, result = await anlas_set(at, anlas_change)
                message = f"分配完成：" + \
                    MessageSegment.at(at)+f"的剩余点数为{result}"
            else:
                result, user_anlas = await anlas_set(user_id, -anlas_change)
                if result:
                    _, at_anlas = await anlas_set(at, anlas_change)
                    message = f"分配完成：\n"+MessageSegment.at(
                        user_id)+f"的剩余点数为{user_anlas}\n"+MessageSegment.at(at)+f"的剩余点数为{at_anlas}"
                    await setanlas.finish(message)
                else:
                    await setanlas.finish(f"分配失败：点数不足，你的剩余点数为{user_anlas}")
            await setanlas.finish(message)
        else:
            await setanlas.finish(f"请以正整数形式输入点数")
    else:
        await setanlas.finish(f"请@你希望给予点数的人")


async def anlas_check(user_id):
    if not jsonpath.exists():
        jsonpath.parent.mkdir(parents=True, exist_ok=True)
        async with aiofiles.open(jsonpath, "w+")as f:
            await f.write("{}")
    async with aiofiles.open(jsonpath, "r") as f:
        jsonraw = await f.read()
        anlasdict: dict = json.loads(jsonraw)
        anlas = anlasdict.get(user_id, 0)
        return anlas


async def anlas_set(user_id, change):
    oldanlas = await anlas_check(user_id)
    newanlas = oldanlas+change
    if newanlas < 0:
        return False, oldanlas
    anlasdict = {}
    async with aiofiles.open(jsonpath, "r") as f:
        jsonraw = await f.read()
        anlasdict: dict = json.loads(jsonraw)
    anlasdict[user_id] = newanlas
    async with aiofiles.open(jsonpath, "w+") as f:
        jsonnew = json.dumps(anlasdict)
        await f.write(jsonnew)
        return True, newanlas
