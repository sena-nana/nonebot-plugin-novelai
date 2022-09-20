from githubkit import UnauthAuthStrategy,Response,GitHub
from .. import link
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message,MessageSegment
from ...model import Repolink

@link.handle()
async def createlink(bot: Bot, event: GroupMessageEvent):
    owner,repo= event.message.extract_plain_text().replace('https://github.com/','').split('/')[:1]
    if await Repolink.exists().where(
        (Repolink.userid==event.group_id)&
        (Repolink.repo==repo)&
        (Repolink.owner==owner)):
        link.finish(f'当前群已经订阅{owner}/{repo}')
    else:
        async with GitHub(UnauthAuthStrategy()) as github:
            try:
                await github.rest.repos.async_get(owner=owner,repo=repo)
            except Exception as e:
                if e.response.status_code==404:
                    link.finish(f'404 forbidden\n请确保未输错地址/请确保Bot部署环境能正常访问Github')
                elif e.response.status_code==403:
                    link.finish(f'403 forbidden')
            else:
                await Repolink.insert(Repolink(
                    userid=event.group_id,
                    repo=repo,
                    owner=owner
                ))
                link.finish(f'{owner}/{repo}订阅完成')
