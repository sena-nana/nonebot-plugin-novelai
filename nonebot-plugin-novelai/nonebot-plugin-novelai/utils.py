def is_contain_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

import aiohttp
async def translate_ZH2EN(input):
    async with aiohttp.ClientSession() as session:
        data = {
                'doctype': 'json',
                'type': 'ZH_CN2EN',
                'i': input
                }
        async with session.post("http://fanyi.youdao.com/translate",data=data) as requests:
            result = await requests.json()
            return result["translateResult"][0][0]["tgt"]