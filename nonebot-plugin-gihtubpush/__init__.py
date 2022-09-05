from githubkit import UnauthAuthStrategy,Response,GitHub
import os
import json
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message,MessageSegment
from nonebot.params import CommandArg

data={}
datapath = 'data\githubpush.json'

if not os.path.exists(datapath):
    with open(datapath, 'w+') as f:
        f.writelines(r'{}')
    data={}
else:
    with open(datapath, 'r+') as f:
        data = json.load(f)

link= on_command('.link',priority=5)


async def linkpre(link):
    return link.replace('https://github.com/','').split('/')[:1]
    
async def writeconfig():
    with open(datapath, 'w+') as f:
        json.dump(data, f)

async def main():
    async with GitHub(UnauthAuthStrategy()) as github:
        commit=await github.rest.repos.async_list_commits(owner='sena-nana',repo='sena-nana.github.io')
        repo=commit.parsed_data
        print(repo[0].commit.message)