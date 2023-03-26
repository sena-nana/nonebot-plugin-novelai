import aiohttp
from ..config import config
from nonebot.log import logger


async def translate(text: str, to: str):
    # en,jp,zh
    result = await translate_deepl(text, to) or await translate_bing(text, to) or await translate_google_proxy(text, to) or await translate_youdao(text, to)
    if result:
        return result
    else:
        logger.error(f"未找到可用的翻译引擎！")
        return text


async def translate_bing(text: str, to: str):
    """
    en,jp,zh_Hans
    """
    if to == "zh":
        to = "zh-Hans"
    key = config.bing_key
    if not key:
        return None
    header = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
    }
    async with aiohttp.ClientSession() as session:
        body = [{'text': text}]
        params = {
            "api-version": "3.0",
            "to": to,
            "profanityAction": "Deleted",
        }
        async with session.post('https://api.cognitive.microsofttranslator.com/translate', json=body, params=params, headers=header) as resp:
            if resp.status != 200:
                logger.error(f"Bing翻译接口调用失败,错误代码{resp.status},{await resp.text()}")
                return None
            jsonresult = await resp.json()
            result=jsonresult[0]["translations"][0]["text"]
            logger.debug(f"Bing翻译启动，获取到{text},翻译后{result}")
            return result


async def translate_deepl(text: str, to: str):
    """
    EN,JA,ZH
    """
    to = to.upper()
    key = config.deepl_key
    if not key:
        return None
    async with aiohttp.ClientSession() as session:
        params = {
            "auth_key":key,
            "text": text,
            "target_lang": to,
        }
        async with session.get('https://api-free.deepl.com/v2/translate', params=params) as resp:
            if resp.status != 200:
                logger.error(f"DeepL翻译接口调用失败,错误代码{resp.status},{await resp.text()}")
                return None
            jsonresult = await resp.json()
            result=jsonresult["translations"][0]["text"]
            logger.debug(f"DeepL翻译启动，获取到{text},翻译后{result}")
            return result


async def translate_youdao(input: str, type: str):
    """
    默认auto
    ZH_CH2EN 中译英
    EN2ZH_CN 英译汉
    """
    if type == "zh":
        type = "EN2ZH_CN"
    elif type == "en":
        type = "ZH_CH2EN"
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
            result=result["translateResult"][0][0]["tgt"]
            logger.debug(f"有道翻译启动，获取到{input},翻译后{result}")
            return result


async def translate_google_proxy(input: str, to: str):
    """
    en,jp,zh 需要来源语言
    """
    if to == "zh":
        from_ = "en"
    else:
        from_="zh"
    async with aiohttp.ClientSession()as session:
        data = {"data": [input, from_, to]}
        async with session.post("https://hf.space/embed/mikeee/gradio-gtr/+/api/predict", json=data)as resp:
            if resp.status != 200:
                logger.error(f"谷歌代理翻译接口调用失败,错误代码{resp.status},{await resp.text()}")
                return None
            result = await resp.json()
            result=result["data"][0]
            logger.debug(f"谷歌代理翻译启动，获取到{input},翻译后{result}")
            return result
