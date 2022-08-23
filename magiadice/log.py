from nonebot import on_command, on_message
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message
from nonebot.params import CommandArg
from .logger import Logger
from nonebot import get_driver
import time
superuser = get_driver().config.master
sendtomaster = get_driver().config.trpgsendtomaster
loglist = {}  # FIXME 配置文件化+启动时自动载入

logger = on_message(priority=1, block=False)
log = on_command(".log")

async def loghelp():
    await log.finish(
        """魔法崩坏跑团log工具 喵
.log on <gameid> 开始记录(不传id）/使用id继续记录
.log in <charaname> 加入游戏(不传名字则使用昵称)
.log off 结束记录（记录十小时后自动停止）

记录完善指令
.log name [title] 设置记录的标题(默认为日期)
.log intro [data] 添加介绍（添加在LOG开始的模组介绍中）
.log change [x] [data] 修改第x条模组介绍（不传data为删除）"""
    )
# TODO 通过图片生成配置
# TODO 完善使用说明

@log.handle()
async def log_(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    list_str = args.extract_plain_text().strip().split()
    match len(list_str):
        case 0:
            await loghelp()
        case 1:
            match list_str[0]:
                case 'off':
                    if event.group_id in loglist:
                        id = loglist[event.group_id].page.id.replace("-", '')
                        loglist.pop(event.group_id)
                        await masteroff(bot, event, id)
                        await log.finish(f'记录完成喵！\n查看链接：https://www.notion.so/'+id+f'\n链接后缀为记录id，使用[.log on id]指令可以继续记录\n可自行保存为离线网页或打印为pdf')
                    else:
                        await log.finish(f'当前群没有正在记录的游戏喵')
                case 'on':
                    if event.group_id in loglist:
                        await log.finish(f'请先结束当前群正在记录的游戏喵')
                    else:
                        loglist[event.group_id] = Logger()
                        await loglist[event.group_id].init(event.sender.nickname)
                        await masteron(bot, event)
                        await log.finish(f'命运之书的文字逐渐浮现（开始记录）\n实时更新链接：https://www.notion.so/'+loglist[event.group_id].page.id.replace("-", '')+"\n- 只有玩家、KP的发言和BOT的掷骰结果会被记录喵\n- [.]开头的发言会被LOG忽略\n- (括号括起来的发言会被标记为灰色)\n- “角色说话请使用引号喵！”\n-KP发的图片会作为线索图被记录（表情包打咩）")
                case 'in':
                    if event.group_id in loglist:
                        error = await loglist[event.group_id].login(event.sender.nickname, event.sender.nickname)
                        if error:
                            await log.finish(error)
                    else:
                        await log.finish(f'当前群没有正在记录的游戏喵')
                case _:
                    await loghelp()
        case 2:
            match list_str[0]:
                case 'in':
                    if event.group_id in loglist:
                        error = await loglist[event.group_id].login(event.sender.nickname, list_str[1])
                        if error:
                            await log.finish(error)
                    else:
                        await log.finish(f'当前群没有正在记录的游戏喵')
                case 'on':
                    if event.group_id in loglist:
                        await log.finish(f'请先结束当前群正在记录的游戏喵')
                    else:
                        loglist[event.group_id] = Logger()
                        await loglist[event.group_id].init(list_str[1])
                        await masteron(bot, event)
                        await log.finish(f'{loglist[event.group_id].page.title}记录恢复完成！\n实时更新链接：https://www.notion.so/'+loglist[event.group_id].page.id.replace("-", ''))
                case 'intro':
                    if event.group_id in loglist:
                        await loglist[event.group_id].intronew(list_str[1])
                        await log.finish(f'模组介绍添加完成喵！')
                    else:
                        await log.finish(f'当前群没有正在记录的游戏喵')
                case 'change':
                    if event.group_id in loglist:
                        error = await loglist[event.group_id].introdel(list_str[1])
                        if error:
                            log.finish(error)
                    else:
                        await log.finish(f'当前群没有正在记录的游戏喵')
                case 'name':
                    if event.group_id in loglist:
                        loglist[event.group_id].page.title = list_str[1]
                        await log.finish(f'跑团记录的标题已经更新为：'+loglist[event.group_id].page.title)
                    else:
                        await log.finish(f'当前群没有正在记录的游戏喵')
                case _:
                    await loghelp()
        case 3:
            match list_str[0]:
                case 'change':
                    if event.group_id in loglist:
                        error = await loglist[event.group_id].introchange(list_str[1], list_str[2])
                        if error:
                            await log.finish(error)
                    else:
                        await log.finish(f'当前群没有正在记录的游戏喵')
        case _:
            await loghelp()


@logger.handle()
async def islogging(bot: Bot, event: GroupMessageEvent):
    if event.group_id in loglist:
        if time.time()-loglist[event.group_id].createtime > 36000:
            id = loglist[event.group_id].page.id.replace('-', '')
            loglist.pop(event.group_id)
            await masteroff(bot, event, id)
            await logger.finish(f'持续记录时间过久自动停止了喵！\n查看链接：https://www.notion.so/'+id+f'\n链接后缀为记录id，使用[.log on id]指令可以继续记录\n可自行保存为离线网页或打印为pdf')
        text = event.get_plaintext()
        if text:
            await loglist[event.group_id].logup_text(event.sender.nickname, text)
        if loglist[event.group_id].player[event.sender.nickname][0] == 'KP':
            for seg in event.message['image']:
                await loglist[event.group_id].logup_image(seg.data['url'])


async def botlog(groupid, message):
    if groupid in loglist:
        await loglist[groupid].logup_text(False, message)


async def masteron(bot, event):
    if sendtomaster:
        await bot.call_api('send_msg', **{
            'message': f'{event.group_id}开始记录数据：'+loglist[event.group_id].page.id.replace("-", ''),
            'user_id': superuser,
        })


async def masteroff(bot, event, id):
    if sendtomaster:
        await bot.call_api('send_msg', **{
            'message': f'{event.group_id}结束记录数据：{id}',
            'user_id': superuser,
        })
