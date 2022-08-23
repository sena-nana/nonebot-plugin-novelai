from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from numpy import random
from data.omikuji.dailydata import data

omikuji = on_command('抽签',priority=5)
luckylist = {'大凶':0.1,'凶':0.2,'小吉':0.3,'吉':0.3,'大吉':0.1}

def checkluck(data):
    sum=0
    for keys, values in luckylist.items():
        if data<=(values+sum)*100:
            return keys
        sum+=values

@omikuji.handle()
async def handle_receive(bot: Bot, event: GroupMessageEvent):
    send_type=event.message_type
    if send_type =='group':
        id=event.group_id
    else:
        id= event.user_id
    name = event.user_id
    if name not in data:
        data.append(name)
        luckypoint=random.randint(1,100)
        lucky_type=checkluck(luckypoint)
        # image=r"data/omikuji/"+lucky_type
        # omikuji.send(f'[CQ:at,qq={id}]既然如此就勉为其难为你抽一签nya[CQ:image,file={image}]')
        message = f'[CQ:at,qq={name}]既然如此就勉为其难为主人抽一签喵\n今天的运势是{lucky_type}喵！\n幸运数字是{luckypoint}喵！'
    else:
        message = f'[CQ:at,qq={name}]今天主人已经抽过签了喵!'
    await bot.call_api('send_'+send_type+'_msg', **{
            'message': message,
            "user_id" if send_type == "private" else "group_id": id,
        })
    with open('data\omikuji\dailydata.py', 'w') as f:
        f.write(f'data = {data}')
