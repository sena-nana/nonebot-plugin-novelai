from . import txt2img,config
from nonebot.plugin import PluginMetadata
from .utils.deepdanbooru import deepdanbooru
__plugin_meta__ = PluginMetadata(
    name="AI绘图",
    description="调用novelai进行二次元AI绘图",
    usage=f"基础用法:\n.aidraw[指令] [空格] loli,[参数]\n示例:.aidraw loli,cute,kawaii,\n项目地址:https://github.com/Mutsukibot/tree/nonebot-plugin-novelai\n说明书：https://sena-nana.github.io/MutsukiDocs/",
)

#TODO 黑白名单
#TODO 全年龄关闭时切换到FULL模型