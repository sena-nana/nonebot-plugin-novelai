from nonebot import get_bot,get_driver
import asyncio
async def sendtosuperuser(message):
    superusers=get_driver().config.superusers
    bot=get_bot()
    for superuser in superusers:
        await bot.call_api('send_msg', **{
            'message': message,
            'user_id': superuser,
        })
        await asyncio.sleep(5)
