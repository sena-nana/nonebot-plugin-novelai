async def sendtosuperuser(message):
    # 将消息发送给superuser
    from nonebot import get_bot,get_driver
    import asyncio
    superusers=get_driver().config.superusers
    bot=get_bot()
    for superuser in superusers:
        await bot.call_api('send_msg', **{
            'message': message,
            'user_id': superuser,
        })
        await asyncio.sleep(5)

def is_contain_chinese(check_str:str):
    #检测字符串是否包含中文
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


async def translate_ZH2EN(input:str):
    #将中文翻译为英文
    import aiohttp
    async with aiohttp.ClientSession() as session:
        data = {
                'doctype': 'json',
                'type': 'ZH_CN2EN',
                'i': input
                }
        async with session.post("http://fanyi.youdao.com/translate",data=data) as requests:
            result = await requests.json()
            return result["translateResult"][0][0]["tgt"]

def file_name_check(input:str):
    #检查文件名是否包含可能导致保存失败的字符
    errorcode=["?","<",">","\\","/","*","|",":"]
    for i in errorcode:
        input.replace(i,"")
    return input
async def translate_bing(text:str,to:"str")->str:
    """
    en,jp,zh_Hans
    """
    import aiohttp
    header={
            "Ocp-Apim-Subscription-Key": key,
            "Content-Type": "application/json",
        }
    async with aiohttp.ClientSession() as session:
        body=[{'text': text}]
        params={
            "api-version":"3.0",
            "to":to,
        }
        async with session.post('https://api.cognitive.microsofttranslator.com/translate',json=body,params=params,headers=header) as resp:
            if resp.status!=200:
                return f"识别失败，错误代码为{resp.status}"
            jsonresult=await resp.json()
            return jsonresult[0]["translations"][0]["text"]
async def check_lan(text:str):
    header = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
    }
    async with aiohttp.ClientSession() as session:
        body = [{'text': text}]
        params = {
            "api-version": "3.0"
        }
        async with session.post('https://api.cognitive.microsofttranslator.com/detect', json=body, params=params, headers=header) as resp:
            if resp.status != 200:
                logger.error(f"Bing翻译接口调用失败,错误代码{resp.status},{await resp.text()}")
                return None
            jsonresult = await resp.json()
            return jsonresult[0]["language"]