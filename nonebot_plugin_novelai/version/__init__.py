import asyncio
import os
import sys
from pathlib import Path
from .version import Version
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent
from nonebot.permission import SUPERUSER
from nonebot.log import logger
from ..utils import cs, aliases

version = Version()
check = on_command(cs("version"), aliases=aliases("版本"), priority=5)
update = on_command(
    cs("update"), aliases=aliases("更新"), permission=SUPERUSER, priority=5
)
reboot = on_command(
    cs("reboot"), aliases=aliases("重启"), permission=SUPERUSER, priority=5
)


@check.handle()
async def check_handle(bot: Bot, event: MessageEvent):
    await version.check_update()
    if version.version == version.latest:
        await check.finish(f"当前nonebot-plugin-novelai版本为{version.version}\n已经是最新版本了~")
    await check.finish(version.push_txt)


async def install():
    proc = await asyncio.create_subprocess_exec(
        sys.executable,
        "-m",
        "pip",
        "install",
        "-U",
        version.package,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    _, error = await proc.communicate()
    return bool(error)


@reboot.handle()
async def reboot_handle():
    if sys.platform == "win32":
        path = Path("run.bat")
        if not path.exists():
            logger.debug("正在创建重启脚本")
            venvpath = Path(sys.executable)
            boot = (
                f"call {str(venvpath.parent)}/activate"
                if venvpath.parts[-3] == ".venv"
                else ""
            )
            with open(path, "w") as f:
                f.writelines([boot, "taskkill /f /im nb.exe", "nb run"])
        os.startfile("run.bat")
    else:
        path = Path("run.sh")
        if not path.exists():
            logger.debug("正在创建重启脚本")
            venvpath = Path(sys.executable)
            boot = (
                f"resource {str(venvpath.parent)}/activate"
                if venvpath.parts[-3] == ".venv"
                else ""
            )
            with open(path, "w") as f:
                f.writelines([boot, "pkill nb", "nb run"])
        os.startfile("run.sh")
