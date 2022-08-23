import time
from notion.block import TextBlock, PageBlock, DividerBlock, NumberedListBlock, ImageBlock
from datetime import datetime
import asyncio
from notion.client import NotionClient
from nonebot import get_driver
import urllib.request
import os
import imghdr

token = get_driver().config.token
client = NotionClient(token)
basepage = client.get_block(get_driver().config.log_database)
dirs = 'cache/magiadice'

if not os.path.exists(dirs):
    os.makedirs(dirs)

class Logger():

    colorlist = ['default', 'red', 'blue', 'green',
                 'purple', 'yellow', 'orange', 'pink']

    async def init(self, sender) -> None:
        if len(sender) < 30:
            self.player = {}
            self.createtime = time.time()
            self.page = await asyncio.to_thread(basepage.children.add_new, PageBlock, title=datetime.now().strftime(f"%Y%m%d%H%M%S"))
            await self.logon()
            await self.login(sender, 'KP')
        else:
            await self.logdown(sender)

    async def logon(self):
        await asyncio.to_thread(self.page.children.add_new, TextBlock, title='玩家信息:')
        await asyncio.to_thread(self.page.children.add_new, TextBlock, title='模组信息:')
        await asyncio.to_thread(self.page.children.add_new, DividerBlock)

    async def login(self, sender, name):
        if sender in self.player:
            return f'{sender}已经在游戏中了！'
        else:
            if self.colorlist:
                color = self.colorlist.pop()
            else:
                return '玩家人数超出最大值了喵！'
            self.player[sender] = [name, color]

            await asyncio.to_thread(self.page.children[0].children.add_new, TextBlock, title=f'{name}:{sender}', color=color)
            return f'{name}({sender})已加入游戏！'

    async def logup_text(self, sender, message):
        match message[0]:
            case '(':
                ot = True
            case '（':
                ot = True
            case '.':
                return False
            case _:
                ot = False
        if sender:
            text = '<'+self.player[sender][0]+'>'+message
            if ot:
                await asyncio.to_thread(self.page.children.add_new, TextBlock, title=text, color='gray')
            else:
                await asyncio.to_thread(self.page.children.add_new, TextBlock, title=text, color=self.player[sender][1])
        else:
            text = f'<BOT>'+message
            await asyncio.to_thread(self.page.children.add_new, TextBlock, title=text, color='brown')

    async def logup_image(self, url):
        filepath = dirs+str(time.time())
        await asyncio.to_thread(urllib.request.urlretrieve, url, filepath)
        type = imghdr.what(filepath)
        newpath = dirs+str(time.time())+'.'+type
        os.rename(filepath, newpath)
        image = await asyncio.to_thread(self.page.children.add_new, ImageBlock)
        await asyncio.to_thread(image.upload_file, newpath)
        os.remove(newpath)

    async def logdown(self, id):
        self.page = await asyncio.to_thread(client.get_block, id)
        self.player = {}
        for child in self.page.children[0].children:
            sender, name = child.title.split(':')
            color = child.color
            self.player[sender] = [name, color]
        self.createtime = time.time()

    async def intronew(self, data):
        await asyncio.to_thread(self.page.children[1].children.add_new, NumberedListBlock, title=data)

    async def introchange(self, id, data):
        if len(self.page.children[1].children) >= id:
            content = self.page.children[1].children[id].title
            self.page.children[1].children[id].title = data
            return f'模组介绍修改完成喵！原始内容为：'+content
        else:
            return f'模组介绍不存在第{id}条数据喵！'

    async def introdel(self, id):
        if len(self.page.children[1].children) >= int(id):
            content = self.page.children[1].children[id].title
            await asyncio.to_thread(self.page.children[1].children[id].remove)
            return f'模组介绍删除完成喵！删除内容为：'+content
        else:
            return f'模组介绍不存在第{id}条数据喵！'
