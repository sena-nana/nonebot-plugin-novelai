def is_contain_chinese(check_str:str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

import aiohttp


def file_name_check(input:str):
    errorcode=["?","<",">","\\","/","*","|",":"]
    for i in errorcode:
        input.replace(i,"")
    return input

import re
async def check_last_version(package:str,version:str):
    pypiversion=""
    versionlist=version.split(".")
    async with aiohttp.ClientSession() as session:
        async with session.get("https://pypi.org/simple/"+package) as resp:
            text=await resp.text()
            pattern=re.compile("-(\d.*?).tar.gz")
            pypiversion=re.findall(pattern,text)[-1]
    pypilist:list[str]=pypiversion.split(".")
    for i in range(len(versionlist)):
        if int(pypilist[i])>int(versionlist[i]):
            return pypiversion
        elif int(pypilist[i])<int(versionlist[i]):
            return None
    return None

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
