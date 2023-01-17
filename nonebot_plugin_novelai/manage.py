from nonebot import on_command
from nonebot.adapters.onebot.v11 import GROUP_ADMIN, GROUP_OWNER, Bot, GroupMessageEvent
from nonebot.log import logger
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from .utils import cs, aliases
from .config import config

# TODO
on = on_command(
    cs("on"),
    aliases=aliases("开启"),
    permission=SUPERUSER or GROUP_ADMIN or GROUP_OWNER,
    block=True,
)
off = on_command(
    cs("off"),
    aliases=aliases("关闭"),
    permission=SUPERUSER or GROUP_ADMIN or GROUP_OWNER,
    block=True,
)
set = on_command(
    cs("set"),
    aliases=aliases("设置"),
    permission=SUPERUSER or GROUP_ADMIN or GROUP_OWNER,
    block=True,
)


@set.handle()
async def set_(bot: Bot, event: GroupMessageEvent, args=CommandArg()):
    if args[0] and args[1]:
        key, value = args
        await set.finish(
            f"设置群聊{key}为{value}完成"
            if await config.set_value(event.group_id, key, value)
            else f"不正确的赋值"
        )
    else:
        group_config = await config.get_groupconfig(event.group_id)
        message = "当前群的设置为\n"
        for i, v in group_config.items():
            message += f"{i}:{v}\n"
        await set.finish(message)


@on.handle()
async def on_(bot: Bot, event: GroupMessageEvent, args=CommandArg()):

    if args[0] in ["on", "开启"]:
        set = True
    else:
        set = False
    result = await config.set_enable(event.group_id, set)
    logger.info(result)
    await on.finish(result)
