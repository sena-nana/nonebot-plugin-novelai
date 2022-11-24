from collections import deque


class FIFO():
    gennerating: dict={}
    queue: deque = deque([])

    @classmethod
    def len(cls):
        return len(cls.queue)+1 if cls.gennerating else len(cls.queue)

    @classmethod
    async def add(cls, aidraw):
        cls.queue.append(aidraw)
        await cls.gennerate()

    @classmethod
    async def gennerate(cls):
        pass
