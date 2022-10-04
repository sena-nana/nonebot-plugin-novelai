from pathlib import Path
import nonebot
from nonebot.plugin import PluginMetadata
__plugin_meta__= PluginMetadata(
    name='梦月Bot',
    description='<记得起名>',
    usage='',
)
currentpath=Path(__file__).parent
for i in currentpath.iterdir():
    modulename=i.parts[-1]
    plugin=i/modulename
    if plugin.exists():
        nonebot.load_plugins(i)