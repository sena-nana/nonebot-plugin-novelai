from pydantic import BaseSettings, validator
from nonebot import get_driver
from nonebot.log import logger
from pydantic.fields import ModelField
from pathlib import Path
import aiofiles
import json
jsonpath = Path("data/novelai/config.json").resolve()

class Config(BaseSettings):#TODO修改为数据库
    novelai_token: str = ""
    novelai_tag: str = ""
    novelai_cd: int = 60
    novelai_limit: bool = True
    novelai_save_pic:bool = True
    novelai_api_domain: str = "https://api.novelai.net/"
    novelai_site_domain: str = "https://novelai.net/"
    novelai_mode:str = "novelai"
    novelai_paid:int = 0
    novelai_ban:list[int]=[]#TODO 修改为黑白名单
    novelai_h:bool = False
    novelai_oncemax:int = 3
    bing_key:str=None
    __arglist=["novelai_cd"]

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

    def check_mode(cls):# TODO 重写
        mode=cls.novelai_mode
        match mode:
            case "novelai":
                if cls.novelai_token:
                    cls.set_novelai()
                else:
                    logger.error(f"使用novelai模式但未检测到novelai token")
            case "naifu":
                if cls.novelai_api_domain == "https://api.novelai.net/" or cls.novelai_site_domain == "https://novelai.net/":
                    logger.error(f"请配置个人服务器api和site")
            case "webui":
                if cls.novelai_api_domain == "https://api.novelai.net/" or cls.novelai_site_domain == "https://novelai.net/":
                    logger.error(f"请配置个人服务器api和site")
            case _:
                if cls.novelai_token:
                    logger.error(f"请配置正确的运行模式，检测到token，自动切换至novelai模式")
                    cls.set_novelai()
                    cls.mode="novelai"
                else:
                    logger.error(f"请配置正确的运行模式")

    def set_novelai(cls):
        cls.novelai_api_domain: str = "https://api.novelai.net/"
        cls.novelai_site_domain: str = "https://novelai.net/"

    def set_enable(cls,groupid,enable):
        if groupid in cls.novelai_ban:
            if enable:
                cls.novelai_ban.remove(groupid)
                return f"aidraw开始运行"
            else:
                return f"aidraw已经处于关闭状态"
        else:
            if enable:
                return f"aidraw已经处于启动状态"
            else:
                cls.novelai_ban.append(groupid)
                return f"aidraw已关闭"
    class Config:
        extra = "ignore"
    async def __init_json(cls):
        if not jsonpath.exists():
            jsonpath.parent.mkdir(parents=True,exist_ok=True)
            async with aiofiles.open(jsonpath, "w+")as f:
                await f.write("{}")
    async def get_value(cls,group_id,arg):
        group_id=str(group_id)
        arg_="novelai_"+arg
        await cls.__init_json()
        async with aiofiles.open(jsonpath,"r") as f:
            jsonraw=await f.read()
            configdict:dict=json.loads(jsonraw)
            return configdict.get(group_id,{}).get(arg_,False)
    async def get_groupconfig(cls,group_id):
        group_id=str(group_id)
        await cls.__init_json()
        async with aiofiles.open(jsonpath,"r") as f:
            jsonraw=await f.read()
            configdict:dict=json.loads(jsonraw)
            groupdict:dict= configdict.get(group_id,{})
        baseconfig={}
        for i,v in cls.__dict__.items():
            if i in cls.__arglist:
                baseconfig[i]=v
        baseconfig.update(groupdict)
        return baseconfig
    async def set_value(cls,group_id,arg,value):
        group_id=str(group_id)
        arg_="novelai_"+arg
        if arg_ in cls.__arglist:
            await cls.__init_json()
            async with aiofiles.open(jsonpath,"r") as f:
                jsonraw=await f.read()
                configdict:dict=json.loads(jsonraw)
            groupdict=configdict.get(group_id,{})
            if value=="default":
                groupdict[arg_]=False
            else:
                groupdict[arg_]=value
            configdict[group_id]=groupdict
            async with aiofiles.open(jsonpath,"w") as f:
                jsonnew=json.dumps(configdict)
                await f.write(jsonnew)
            return True
        else:
            logger.error(f"不正确的赋值")
            return False

config = Config(**get_driver().config.dict())
logger.debug(f"加载config完成" + str(config))