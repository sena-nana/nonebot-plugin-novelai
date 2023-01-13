import time
from importlib.metadata import version
from nonebot import on_command
from nonebot.log import logger
import asyncio
import sys
from .utils import check_last_version, compare_version, sendtosuperuser

check = on_command("check", aliases={"检查更新", "更新", "check"}, priority=5)
update = on_command("update", aliases={"更新", "update"}, priority=5)


class Version:
    version: str  # 当前版本
    lastcheck: float = 0  # 上次检查时间
    ispushed: bool = True  # 是否已经推送
    latest: str = "0.0.0"  # 最新版本
    package = "nonebot-plugin-novelai"
    url = "https://nb.novelai.dev"

    def __init__(self):
        # 初始化当前版本
        try:
            self.version = version(self.package)
        except:
            self.version = "0.6.0"

    async def check_update(self):
        """检查更新，并推送"""
        # 每日检查
        if time.time() - self.lastcheck > 80000:
            update = await check_last_version(self.package)
            # 判断是否重复检查
            if await compare_version(self.latest, update):
                self.latest = update
                # 判断是否是新版本
                if await compare_version(self.version, self.latest):
                    logger.info(self.push_txt())
                    self.ispushed = False
                else:
                    logger.info(f"novelai插件检查版本完成，当前版本{self.version}，最新版本{self.latest}")
            else:
                logger.info(f"novelai插件检查版本完成，当前版本{self.version}，最新版本{self.latest}")
            self.lastcheck = time.time()
        # 如果没有推送，则启动推送流程
        if not self.ispushed:
            await sendtosuperuser(self.push_txt())
            self.ispushed = True

    @property
    def push_txt(self):
        # 获取推送文本
        logger.debug(self.__dict__)
        return f"novelai插件检测到新版本{self.latest},当前版本{self.version},请使用pip install --upgrade {self.package}命令升级,更新日志：{self.url}"

    async def update():
        proc = await asyncio.create_subprocess_exec(
            sys.executable,
            "-m",
            "pip",
            "install",
            "-U",
            "nb-cli",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _, b = await proc.communicate()
        return b.decode()

    async def get_update_log():
        pass


version = Version()
