from nonebot import on_command
from nonebot.matcher import Matcher
import random
from nonebot.params import ArgPlainText, CommandArg
import datetime

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
    '水晶',
    '阿波卡利斯'
]
@death.handle()
async def death_receive(matcher:Matcher,args=CommandArg()):
    message=args.extract_plain_text()
    if message.isdigit():
        matcher.set_arg(key='age',message=args)
    else:
        death.send(f'喵只认识数字哦')
@death.got('age',prompt='你的年龄是？')
async def _(args=ArgPlainText('age')):
    age=args
    if age.isdigit():
        age=int(age)
        if age>=100:
            await death.finish(f'喵发现了人类以外的种族！')
        elif age>=50:
            await death.finish(f'现在应该准备养老啦！')
        elif age>0:
            deathage=int(random.gauss(75,8))
        else:
            await death.finish(f'欸，难道是喵不知道的计算方式嘛')
    else:
        death.send(f'喵只认识数字哦')
    deathway=random.choice(way)
    deathyear = datetime.date.today().year-age+deathage
    uraraway=random.choice(urara)
    await death.finish(f'喵呜，让我看看……\n你在{deathyear}年会因为{deathway}被撕卡，{uraraway}如是说喵！')
