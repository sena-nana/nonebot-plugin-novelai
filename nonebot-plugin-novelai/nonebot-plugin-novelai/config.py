from pydantic import BaseSettings, validator
from nonebot import get_driver
from nonebot.log import logger
from pydantic.fields import ModelField


class Config(BaseSettings):
    novelai_token: str
    novelai_tag: str = ""
    novelai_cd: int = 60
    novelai_limit: bool = True
    novelai_save_pic:bool = True
    novelai_api_domain: str = "https://api.novelai.net/"
    novelai_site_domain: str = "https://novelai.net/"

    @validator("novelai_cd")
    def non_negative(cls, v: int, field: ModelField):
        if v < 1:
            return field.default
        return v

    class Config:
        extra = "ignore"


config = Config(**get_driver().config.dict())
logger.debug(f"加载config完成" + str(config))
