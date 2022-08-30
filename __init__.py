import nonebot
from pathlib import Path

currentpath=Path.cwd().absolute()
pluginlist=[
    'nonebot-plugin-ykt',
    'nonebot-plugin-send',
    'nonebot-plugin-omikuji',
    'nonebot-plugin-magiadice'
    ]

for plugin in pluginlist:
    path=str(currentpath/plugin/plugin).replace('\\','/')
    nonebot.load_plugin(path)