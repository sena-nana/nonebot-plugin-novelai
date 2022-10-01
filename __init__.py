from pathlib import Path
import nonebot
_sub_plugins = set()
currentpath=Path.cwd()
for i in currentpath.iterdir():
    modulename=i.parts[-1]
    plugin=i/modulename
    if plugin.exists():
        _sub_plugins |= nonebot.load_plugin(plugin.resolve())