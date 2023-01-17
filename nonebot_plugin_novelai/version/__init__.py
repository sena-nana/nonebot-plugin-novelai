import asyncio
import os
import sys
from importlib.metadata import version as vs
from pathlib import Path
from .version import Version
from nonebot import on_command, get_driver
from nonebot.permission import SUPERUSER
from nonebot.log import logger
from ..utils import cs, aliases, sendtosuperuser

ver = Version()
driver = get_driver()
nickname = driver.config.nickname.pop() if driver.config.nickname else ver.package

check = on_command(cs("version"), aliases=aliases("版本"), priority=5)
update = on_command(
    cs("update"), aliases=aliases("更新"), permission=SUPERUSER, priority=5
)
reboot = on_command(
    cs("reboot"), aliases=aliases("重启"), permission=SUPERUSER, priority=5
)


@check.handle()
async def check_handle():
    await ver.check_update()
    if ver.version == ver.latest:
        await check.finish(f"当前{ver.package}版本为{ver.version}\n已经是最新版本了~")
    else:
        await check.finish(f"当前{ver.package}版本为{ver.version}\n最新版本{ver.latest}~")


@update.handle()
async def update_handle():
    if ver.version == ver.latest:
        await update.finish("已经是最新版本了不需要更新哦~")
    else:
        if vs(ver.package) == ver.latest:
            await update.finish(f"插件已经更新过了，正在等待重启~\n请使用aidraw reboot命令重启{nickname}~")
        await update.send("正在更新中~")
        if await install():
            await update.send("更新失败，请手动更新~")
        else:
            await update.send(f"更新成功~请使用aidraw reboot命令重启{nickname}~")


async def install():
    proc = await asyncio.create_subprocess_exec(
        sys.executable,
        "-m",
        "pip",
        "install",
        "-U",
        ver.package,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    _, error = await proc.communicate()
    return bool(error)


@reboot.handle()
async def reboot_handle():
    await reboot.send(f"{nickname}正在重启中~")
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
    await reboot.send(f"{nickname}重启失败了！")


@driver.on_bot_connect
async def on_start():
    await sendtosuperuser(f"{nickname}启动完成")
