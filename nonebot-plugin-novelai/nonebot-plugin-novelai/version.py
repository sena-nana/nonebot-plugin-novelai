from importlib.metadata import version
import asyncio
from .utils import check_last_version,sendtosuperuser
from nonebot.log import logger
import time

package="nonebot-plugin-novelai"
url="https://github.com/Mutsukibot/tree/nonebot-plugin-novelai"
try:
    __version__=version(package)
except:
    __version__="0.4.3"

lastcheck:float=0
async def check_update(isinit=True):
    global lastcheck
    if time.time()-lastcheck>80000:
        update=await check_last_version(package,__version__)
        if update:
            message=f"检测到新版本{update},当前版本{__version__},请使用pip install --upgrade {package}命令升级,查看项目获取更多信息:{url}"
            logger.info(message)
            if isinit:
                await sendtosuperuser("novelai插件"+message)
        else:
            logger.info(f"检查版本完成，当前为最新版本")
        lastcheck=time.time()
asyncio.run(check_update(False))