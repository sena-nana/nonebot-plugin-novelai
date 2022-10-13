from nonebot import on_command
from nonebot.plugin import get_loaded_plugins
from nonebot.log import logger
boton=on_command(".bot on")
@boton.handle()
async def boton_handle():
    plugins=get_loaded_plugins()
    for i in plugins:
        logger.debug(i.matcher)