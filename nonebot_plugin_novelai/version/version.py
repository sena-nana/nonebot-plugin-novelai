import re
import time
import sys
from importlib.metadata import version as vs
from itertools import zip_longest
import aiohttp
from githubkit import GitHub
from nonebot import get_bot
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.log import logger

from ..utils import sendtosuperuser
from .utils import unpack_version


class Version:
    version: str = ""
    lastcheck: float = 0  # 上次检查时间
    ispushed: bool = True  # 是否已经推送
    latest: str = "0.0.0"  # 最新版本
    package = "nonebot-plugin-novelai"
    url = "https://nb.novelai.dev"

    def __init__(self):
        if self.package in sys.modules:
            self.version = vs(self.package)
        else:
            self.version = "0.6.0"

    async def check_update(self):
        """检查更新，并推送"""
        # 每日检查
        if time.time() - self.lastcheck > 80000:
            await self._check()
        # 如果没有推送，则启动推送流程
        if not self.ispushed:
            bot = get_bot()
            await sendtosuperuser(await self.push_txt())
            self.ispushed = True

    async def _check(self):
        update = await self.check_last_version(self.package)
        if self.is_newer(update, self.latest):
            self.latest = update
            if self.is_newer(self.latest):
                self.ispushed = False
                logger.info("novelai插件检查到有新版本")
        self.lastcheck = time.time()

    async def check_last_version(self, package: str):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://pypi.org/simple/" + package) as resp:
                text = await resp.text()
                pattern = re.compile("-(\d.*?).tar.gz")
                pypiversion = re.findall(pattern, text)[-1]
        return pypiversion

    def is_newer(self, new_version: str, old_version: str = None):
        curr_version = old_version or self.version
        if new_version == curr_version:
            return False

        new_versions = unpack_version(new_version)
        curr_versions = unpack_version(curr_version)

        for new, curr in zip_longest(new_versions, curr_versions, fillvalue="0"):
            if new == curr:
                continue
            else:
                return new > curr
        return False

    async def get_changelog(self):
        async with GitHub() as github:
            resp = await github.rest.repos.async_list_releases(
                owner="sena-nana", repo="nonebot-plugin-novelai"
            )
            repo = resp.parsed_data
        message = MessageSegment.text("更新日志：")
        for i in filter(lambda x: self.is_newer(x.tag_name[1:]), repo):
            message += MessageSegment.text(f"# {i.tag_name}\n{i.body}")
        return message

    async def push_txt(self):
        # 获取推送文本
        logger.debug(self.__dict__)
        message = MessageSegment.node_custom(
            content=f"novelai插件检测到新版本{self.latest},当前版本{self.version},请使用nb plugin install -U {self.package}命令升级,说明书：{self.url}",
            user_id=get_bot().self_id,
            nickname=self.package,
        )
        return message
