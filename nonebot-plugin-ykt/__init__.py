from . import ykt
from nonebot.plugin import PluginMetadata
class Setup():
    name='nonebot-plugin-ykt'
    description='一个基于nonebot的雨课堂自动签到插件'
    version='0.1.4'
    isreleased=False
    updatedate='20220918'
    keywords=['nonebot']
    install_requires=['']

__plugin_meta__= PluginMetadata(
    name=Setup.name,
    description=Setup.description,
    usage='',
)