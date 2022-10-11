from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import MessageSegment,Message
from .data import *
import aiohttp
import base64
import time
from pathlib import Path
path=Path("data/novelai/output").resolve()
txt2pix=on_command(".aidraw",aliases={"文本生图","咏唱"})

@txt2pix.handle()
async def txt2pix_handle(args: Message = CommandArg()):
    map=[640,640]
    input=""
    seed_raw=None
    message_raw=args.extract_plain_text().replace("，",",").split("-")
    for i in message_raw:
        match i:
            case "square"|"s"|"S":
                map=[640,640]
            case "portrait"|"p"|"P":
                map=[768,512]
            case 'landscape'|"l"|"L":
                map=[768,512]
            case _:
                if i.isdigit():
                    seed_raw=int(i)
                else:
                    input+=i
    if not input:
        await txt2pix.finish(f"请描述你想要生成的角色特征(使用英文Tag,代码内已包含优化TAG)")
    seed=seed_raw or int(time.time())
    async with aiohttp.ClientSession("https://api.novelai.net/",headers=header) as session:
        async with session.post("/ai/generate-image",json=txt2pix_body(seed,input,map)) as resp:
            if resp.status != 201:
                await txt2pix.finish(f"生成失败，错误代码为"+str(resp.status))
            img=await resp.text()
            img_bytes=img.split("data:")[1]
            img=base64.b64decode(img_bytes)
            img_name=input+str(seed)+".png"
            path.mkdir(parents=True, exist_ok=True)
            with open(path/img_name, "wb") as f:
                    f.write(img)
            message=MessageSegment.image("base64://"+img_bytes)
            await txt2pix.finish(message)