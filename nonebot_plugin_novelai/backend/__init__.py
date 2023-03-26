from ..config import config
"""def AIDRAW():
    if config.novelai_mode=="novelai":
        from .novelai import AIDRAW
    elif config.novelai_mode=="naifu":
        from .naifu import AIDRAW
    elif config.novelai_mode=="sd":
        from .sd import AIDRAW
    else:
        raise RuntimeError(f"错误的mode设置，支持的字符串为'novelai','naifu','sd'")
    return AIDRAW()"""

if config.novelai_mode=="novelai":
    from .novelai import AIDRAW
elif config.novelai_mode=="naifu":
    from .naifu import AIDRAW
elif config.novelai_mode=="sd":
    from .sd import AIDRAW
else:
    raise RuntimeError(f"错误的mode设置，支持的字符串为'novelai','naifu','sd'")