from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
import random
from nonebot.params import ArgPlainText, CommandArg
import datetime
import time

death=on_command('.death',priority=5, aliases={'查看命运'})
way=[
    '崩坏',
    '变成魔女', 
    '直面古神', 
    '融合战士手术失败', 
    '得了矿石病',
    '转生异世界'
    ]
urara=[
    '命运之书',
    '占星盘',
    '塔罗牌',
    '百度',
    '狐仙',
    '御神签',
    '水晶'
]
@death.handle()
async def death_receive(bot:Bot,event:GroupMessageEvent):
    args=event.message.extract_plain_text()
    if args:
        if args.isdigit():
            death.set_arg('age',args)
        else:
            bot.send(f'喵只认识数字哦')
async def deathckeck(age):
    deathage=random.gauss(75,8)
    if age>=deathage:
        return await deathckeck(age)
    else:
        return deathage
@death.got('age',prompt='你的年龄是？')
async def _(args=ArgPlainText('age')):
    age=args[0]
    if age.isdigit():
        age=int(age)
        if age>0 and age<=75:
            deathage=await deathckeck(age)
        elif age>80:
            await death.finish(f'现在应该养老啦！')
        elif age<=0:
            await death.finish(f'欸，难道是喵不知道的计算方式嘛')
    deathway=random.choice(way)
    deathyear = datetime.date.today().year+int(deathage)-age
    #start=time.mktime((deathyear,1,1,0,0,0,0,0,0))
    #end=time.mktime((deathyear,12,31,23,59,59,0,0,0))
    #deathtime=time.strftime("%Y年%m月%d日",time.localtime(random.randint(start,end)))
    uraraway=random.choice(urara)
    await death.finish(f'喵呜，让我看看……\n你在{deathyear}年会因为{deathway}而死，{uraraway}是这么说的喵！')
            
        
    
