from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message,MessageSegment
from nonebot.params import CommandArg
from numpy import random
import json
from .log import botlog
import os
shuxing = on_command(".magia", priority=5)
help = on_command(".mhelp", priority=5)
sc = on_command(".msc", priority=5)
rd = on_command(".rd", priority=5)
ra = on_command(".ra", priority=5)

datapath = 'data\magia\dailycd.json'


def rd_for(dice, num):
    sum = 0
    for i in range(dice):
        sum += random.randint(1, num+1)
    return sum


def rd_(str):
    if(str.find('d') != -1):
        dice = int(str.split('d')[0])
        num = str.split('d')[1]
        if(num.find('+') != -1):
            num_1 = int(num.split('+')[0])
            plus = int(num.split('+')[1])
            return rd_for(dice, num_1)+plus
        else:
            return rd_for(dice, int(num))
    else:
        return rd_for(1, int(str))


def ra_(skill):
    skill = int(skill)
    dice = random.randint(1, 100)
    if dice <= 4:
        result = str(dice) + f"\n哇，是大成功喵！"
    elif dice == 100:
        result = str(dice) + f"\n哇，是大失败喵！"
    elif(dice <= int(skill/5)):
        result = str(dice) + f"\n极难成功喵！"
    elif (dice <= int(skill/2)):
        result = str(dice) + f"\n困难成功喵！"
    elif dice <= skill:
        result = str(dice) + f"\n成功了喵"
    else:
        result = str(dice) + f"\n失败了喵"
    return(dice, result)


async def magia_random():
    magia = {'属性合计': 0}
    dict = {'力量': '3d6', '体质': '3d6', '智力': '2d6+6', '因果': '3d6',
            '感情': '3d6', '记忆': '3d6', '幸运': '3d6', '外貌': '3d6', '体型': '3d6'}
    for key, value in dict.items():
        magia[key] = rd_(value)*5
        magia['属性合计'] += magia[key]
    magia['武器攻击'] = rd_('2d6+6')
    magia['武器重量'] = rd_('1d20')
    magia['攻击距离/坚韧'] = rd_('3d6')
    return magia


@shuxing.handle()
async def handle_receive(event: GroupMessageEvent):
    name = event.user_id
    if not os.path.exists(datapath):
        with open(datapath, 'w+') as f:
            f.writelines(r'{}')
        data={}
    else:
        with open(datapath, 'r+') as f:
            data = json.load(f)
        if name in data.keys():
            if data[name] >= 3:
                message = f"主人要对自己的魔法少女负责喵！\n(SL当日次数过多)"
                await shuxing.finish(MessageSegment.at(name)+message)
            else:
                data[name] += 1
        else:
            data[name] = 0
    with open(datapath, 'w+') as f:
        json.dump(data, f)
    magia = await magia_random()
    message = f"的魔法少女属性为"
    for key, value in magia.items():
        message = f'{message}\n{key}:{value}'
    await shuxing.finish(MessageSegment.at(name)+message)


@help.handle()
async def help_receive():
    await help.finish(f"《魔法崩坏》规则跑团Bot指令列表\n快速车卡  .magia\nSC检定    .msc 情感值 成功rd 失败rd\n基础指令：\n.ra x x为技能值\n.rd xdy+z x为骰子个数，y为骰子面数，z为固定值，支持省略写法.rdy")# TODO 添加游戏规则地址
    #TODO 将帮助指令提取为全局插件


@sc.handle()
async def handle_sc(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    list_str = args.extract_plain_text().strip().split()
    try:
        emo, fail, success = list_str[:3]
    except:
        await sc.finish(f'参数找不到了喵！')
    dice = ra_(emo)[0]
    if(dice<=emo):
        result = rd_(success)
        str = f'SC检定失败,掷骰结果为'+str(dice)
    else:
        result = rd_(fail)
        str = f'SC检定成功,掷骰结果为'+str(dice)
    str += f'，魔法少女的SAN值损失{result}点'
    if(result >= 5):
        list = ['偏执', '痛觉屏蔽', '恐惧', '孤僻', '狂躁', '迷茫', '幻觉', '混乱', '愤怒']
        mad = random.choice(list)
        str += f'，并陷入了{mad}状态'
    name = event.get_user_id()
    await bot.call_api('send_msg', **{
        'message': str,
        'user_id': name
    })
    await botlog(event.group_id, f'<暗骰>'+str)
    await sc.finish(f'SC检定结果已私发给主持人了喵')


@rd.handle()
async def rd_receive(event: GroupMessageEvent, args: Message = CommandArg()):
    if args:
        args = args.extract_plain_text()
    else:
        await rd.finish(f"骰子去哪里了喵?")
    tmp = rd_(args)
    name = event.get_user_id()
    str = f"的掷骰结果为{tmp}"
    await botlog(event.group_id, name+str)#TODO QQ号改为昵称
    await rd.finish(MessageSegment.at(name)+str)


@ra.handle()
async def ra_receive(event: GroupMessageEvent, args: Message = CommandArg()):
    if args:
        args = args.extract_plain_text()
    else:
        await rd.finish(f"只有知道主人的技能值，月月才能计算出来喵！")
    _, result = ra_(args)
    name = event.get_user_id()
    message = f'的检定结果是：'+result
    await botlog(event.group_id, name+message)
    await ra.finish(MessageSegment.at(name)+message)
#TODO 彻底重写dice模块
#TODO 加入coc基本指令支持
#TODO 加入dnd基本指令支持
#TODO 加入st基本指令支持
#TODO 加入属性值支持