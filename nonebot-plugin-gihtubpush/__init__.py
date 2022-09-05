from githubkit import UnauthAuthStrategy,Response,GitHub
import os
import json
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message,MessageSegment
from nonebot.params import CommandArg
datalist={}
class Data():
    def __init__(self,groupid,owner,repo):
        self.__dict__={
            
        }
    
datapath = 'data\githubpush.json'

if not os.path.exists(datapath):
    with open(datapath, 'w+') as f:
        f.writelines(r'{}')
    data={}
else:
    with open(datapath, 'r+') as f:
        data = json.load(f)

link= on_command('.link',priority=5)

@link.handle()
async def createlink(bot: Bot, event: GroupMessageEvent):
    owner,repo= await linkpre(event.get_plaintext())
    if event.group_id in data:
        bot.finish(f'本群已经订阅了{owner}/{repo}喵！')
    else:
        pass

async def linkpre(link):
    return link.replace('https://github.com/','').split('/')[:1]
    
async def writeconfig():
    with open(datapath, 'w+') as f:
        json.dump(data, f)

async def getcommit():
    async with GitHub(UnauthAuthStrategy()) as github:
        commit=await github.rest.repos.async_list_commits(owner='sena-nana',repo='sena-nana.github.io')
        repo=commit.parsed_data
        commitstr=repo[0].commit.message