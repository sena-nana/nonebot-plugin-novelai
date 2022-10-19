from pydantic import BaseSettings, validator
from nonebot import get_driver
from nonebot.log import logger
from pydantic.fields import ModelField
import asyncio

class Config(BaseSettings):
    novelai_token: str = ""
    novelai_tag: str = ""
    novelai_cd: int = 60
    novelai_limit: bool = True
    novelai_save_pic:bool = True
    novelai_api_domain: str = "https://api.novelai.net/"
    novelai_site_domain: str = "https://novelai.net/"
    novelai_mode:str = "novelai"
    novelai_paid:int = 0
    novelai_ban:list[int]=[]
    novelai_h:bool = False
    novelai_oncemax:int = 3
    bing_key:str=None

    @validator("novelai_cd","novelai_oncemax")
    def non_negative(cls, v: int, field: ModelField):
        if v < 1:
            return field.default
        return v
    @validator("novelai_paid")
    def paid(cls, v: int, field: ModelField):
        if v < 0:
            return field.default
        elif v > 2:
            return field.default
        return v

    def check_mode(cls):
        mode=cls.novelai_mode
        match mode:
            case "novelai":
                if cls.novelai_token:
                    cls.set_novelai()
                else:
                    logger.error(f"使用novelai模式但未检测到novelai token，已切换至public_naifu模式，该模式下运行不稳定")
                    asyncio.run(cls.setup_naifu())
                    cls.mode="public_naifu"
            case "public_naifu":
                asyncio.run(cls.setup_naifu())
                logger.info(f"正在使用public_naifu模式，该模式下运行不稳定")
            case "public_webui":
                asyncio.run(cls.setup_webui())
                logger.info(f"正在使用webui模式，该模式下运行不稳定")
            case "mix":
                logger.info(f"正在使用mix(public_naifu+public_naifu)模式，该模式下运行不稳定")
            case "naifu":
                if cls.novelai_api_domain == "https://api.novelai.net/" or cls.novelai_site_domain == "https://novelai.net/":
                    logger.error(f"请配置个人服务器api和site，已切换至public_naifu模式，该模式下运行不稳定")
                    cls.mode="public_naifu"
            case "webui":
                if cls.novelai_api_domain == "https://api.novelai.net/" or cls.novelai_site_domain == "https://novelai.net/":
                    logger.error(f"请配置个人服务器api和site，已切换至public_webui模式，该模式下运行不稳定")
                    cls.mode="public_webui"
            case _:
                if cls.novelai_token:
                    logger.error(f"请配置正确的运行模式，检测到token，自动切换至novelai模式")
                    cls.set_novelai()
                    cls.mode="novelai"
                else:
                    logger.error(f"请配置正确的运行模式，自动切换至public_naifu模式，该模式下运行不稳定")
                    cls.mode="public_naifu"

    def set_novelai(cls):
        cls.novelai_api_domain: str = "https://api.novelai.net/"
        cls.novelai_site_domain: str = "https://novelai.net/"
    async def setup_naifu():
        pass
    def get_api():
        pass

    def set_enable(cls,enable,groupid):
        if groupid in cls.novelai_ban:
            if enable:
                return f"aidraw已经处于启动状态"
            else:
                cls.novelai_ban.pop(groupid)
                return f"aidraw已关闭"
        else:
            if enable:
                cls.novelai_ban.append(groupid)
                return f"aidraw开始运行"
            else:
                return f"aidraw已经处于关闭状态"
    class Config:
        extra = "ignore"

config = Config(**get_driver().config.dict())
config.check_mode()
logger.debug(f"加载config完成" + str(config))
