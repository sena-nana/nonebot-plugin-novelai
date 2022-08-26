import time
from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import Bot, Message, GroupMessageEvent, PrivateMessageEvent
from nonebot.params import CommandArg
import asyncio
from nonebot import get_driver
send = on_command('.send', priority=5)
notice = on_command('.notice', priority=5, permission=SUPERUSER)


@send.handle()
async def send_receive(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    args_in = args.extract_plain_text()
    name = event.sender.nickname
    group = await bot.call_api('get_group_info', **{
        'group_id': event.group_id,
    })
    group_name = group['group_name']
    superuser = get_driver().config.master
    timenow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    sendmsg = timenow+'\n群聊：'+group_name+'\n发送者：'+name+'\n'+args_in
    await bot.call_api('send_msg', **{
        'message': sendmsg,
        'user_id': superuser,
    })
    await send.finish(f'已经把意见传达给Master了喵！')


@notice.handle()
async def notice_receive(bot: Bot, event: PrivateMessageEvent):
    message = event.raw_message.replace('.notice', '', 1).strip().strip('\n')
    grouplist = await bot.call_api('get_group_list')
    await notice.send(f'通知正在传达喵！')
    for i in range(len(grouplist)):
        await bot.call_api('send_group_msg', **{
            'message': message,
            'group_id': grouplist[i]['group_id'],
        })
        await asyncio.sleep(5)
    await notice.finish(f'通知已经传达完毕了喵！')
