from importlib.metadata import version
from .utils import check_last_version, sendtosuperuser
from nonebot.log import logger
import time
class Version():
    version:str
    lastcheck: float = 0
    ispushed:bool =True
    latest:str
    package="nonebot-plugin-novelai"
    url="https://sena-nana.github.io/MutsukiDocs/update/novelai/"

    def __init__(self):
        try:
            self.version = version(self.package)
        except:
            self.version = "0.4.6"

    async def check_update(self):
        if time.time()-self.lastcheck > 80000:
            update = await check_last_version(self.package,self.version)
            if update:
                self.latest=update
                logger.info(self.push_txt())
                self.ispushed=False
            else:
                self.latest=self.version
                logger.info(f"novelai插件检查版本完成，当前为最新版本")
            self.lastcheck = time.time()
        if not self.ispushed:
            await sendtosuperuser(self.push_txt())
            self.ispushed=True

    def push_txt(self):
        logger.debug(self.__dict__)
        return f"novelai插件检测到新版本{self.latest},当前版本{self.version},请使用pip install --upgrade {self.package}命令升级,更新日志：{self.url}"

version=Version()