from .config import config

if config.novelai_mode=="novelai":
    from .novelai.post import post,FIFO
elif config.novelai_mode=="naifu":
    from .naifu.post import post,FIFO
elif config.novelai_mode=="sd":
    pass
else:
    raise RuntimeError(f"错误的mode设置，支持的字符串为'novelai','naifu','sd'")