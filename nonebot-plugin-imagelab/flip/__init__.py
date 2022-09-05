from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message
from nonebot.params import CommandArg
import numpy
from PIL import Image
from nonebot import on_command
from io import BytesIO
import asyncio
import imghdr
import urllib.request
from func import *

flip= on_command('.flip',aliases={'对称'},priority=5)
flip.help=f'flip.help'

async def getimage(bot:Bot,event:GroupMessageEvent, arg=CommandArg()):
    imgurl=[]
    if event.reply:
        for seg in event.reply.message['image']:
            imgurl.append(seg.data['url'])
    else:
        await bot.finish(f'请’回复‘你想要处理的图片，在回复中输入指令')
    cache=BytesIO()
    for img in imgurl:
        await asyncio.to_thread(urllib.request.urlretrieve,img,cache)
        type = imghdr.what(cache)
        if type not in ['png','jpeg']:
            bot.finish(f'仅支持jpg或png格式图片')
    match arg:
        case '上':
            dst=flipUp(img)
        case '下':
            dst=flipDown(img)
        case '左':
            dst=flipLeft(img)
        case '右':
            dst=flipRight(img)
        case '右上':
            dst=flipRightUp(img)
        case '右下':
            dst=flipRightDown(img)
        case '左上':
            dst=flipLeftUp(img)
        case '左下':
            dst=flipLeftDown(img)
        case _:
            await bot.finish(flip.help)