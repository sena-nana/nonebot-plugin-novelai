from ..config import config

if config.novelai_mode == "novelai":
    from .novelai import Draw
elif config.novelai_mode == "naifu":
    from .naifu import Draw
elif config.novelai_mode == "sd":
    from .sd import Draw
else:
    raise RuntimeError(f"错误的mode设置，支持的字符串为'novelai','naifu','sd'")
