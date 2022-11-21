from .config import config
count=0
if count:
    from .novelai.post import post,FIFO
else:
    from .naifu.post import post,FIFO