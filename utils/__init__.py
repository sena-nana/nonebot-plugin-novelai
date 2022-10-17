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