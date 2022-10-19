import aiohttp
from ..config import config
from nonebot.log import logger

async def translate(text: str, to: str):
    if to == "zh":
        to="zh-Hans"
    result=await translate_bing(text,to) or await translate_youdao(text,to)
    if result:
        return result
    else:
        logger.error(f"未找到可用的翻译引擎！")
        return text

async def translate_bing(text: str, to: str) -> str | None:
    """
    en,jp,zh_Hans
    """
    key = config.bing_key
    header = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
    }
    async with aiohttp.ClientSession() as session:
        body = [{'text': text}]
        params = {
            "api-version": "3.0",
            "to": to,
        }
        async with session.post('https://api.cognitive.microsofttranslator.com/translate', json=body, params=params, headers=header) as resp:
            if resp.status != 200:
                logger.error(f"Bing翻译接口调用失败,错误代码{resp.status},{await resp.text()}")
                return None
            jsonresult = await resp.json()
            return jsonresult[0]["translations"][0]["text"]


async def translate_youdao(input: str, type: str = "auto") -> str | None:
    """
    默认auto
    ZH_CH2EN 中译英
    EN2ZH_CN 英译汉
    """
    async with aiohttp.ClientSession() as session:
        data = {
            'doctype': 'json',
            'type': type,
            'i': input
        }
        async with session.post("http://fanyi.youdao.com/translate", data=data) as resp:
            if resp.status != 200:
                logger.error(f"有道翻译接口调用失败,错误代码{resp.status},{await resp.text()}")
                return None
            result = await resp.json()
            return result["translateResult"][0][0]["tgt"]
