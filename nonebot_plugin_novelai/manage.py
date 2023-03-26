from nonebot.adapters.onebot.v11 import GROUP_ADMIN, GROUP_OWNER
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot
from nonebot.permission import SUPERUSER
from nonebot.params import RegexGroup
from nonebot import on_regex
from nonebot.log import logger
from .config import config
on = on_regex(f"(?:^\.aidraw|^绘画|^aidraw)[ ]*(on$|off$|开启$|关闭$)",
              priority=4, block=True)
set = on_regex(
    "(?:^\.aidraw set|^绘画设置|^aidraw set)[ ]*([a-z]*)[ ]*(.*)", priority=4, block=True)


@set.handle()
async def set_(bot: Bot, event: GroupMessageEvent, args= RegexGroup()):
    if await GROUP_ADMIN(bot, event) or await GROUP_OWNER(bot, event) or await SUPERUSER(bot, event):
        if args[0] and args[1]:
            key, value = args
            await set.finish(f"设置群聊{key}为{value}完成" if await config.set_value(event.group_id, key,
                                                                        value) else f"不正确的赋值")
        else:
            group_config = await config.get_groupconfig(event.group_id)
            message = "当前群的设置为\n"
            for i, v in group_config.items():
                message += f"{i}:{v}\n"
            await set.finish(message)
    else:
        await set.send(f"权限不足！")


@on.handle()
async def on_(bot: Bot, event: GroupMessageEvent, args=RegexGroup()):
    if await GROUP_ADMIN(bot, event) or await GROUP_OWNER(bot, event) or await SUPERUSER(bot, event):
        if args[0] in ["on", "开启"]:
            set = True
        else:
            set = False
        result = await config.set_enable(event.group_id, set)
        logger.info(result)
        await on.finish(result)
    else:
        await on.send(f"权限不足！")
