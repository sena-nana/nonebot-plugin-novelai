import asyncio
import time

from .backend import AIDRAW


class MODEL:
    type: str
    site: str
    model: str
    queue: asyncio.Queue
    running: bool
    generating: bool

    def __init__(self):
        pass

    def reset(self):
        self.available = True
        self.queue = asyncio.Queue()
        self.running = False
        self.generating = False

    async def run_(self):
        if not self.running:
            aidraw: AIDRAW = await self.queue.get()
            self.generating = True
            try:
                await aidraw.run()
            except:
                pass
            aidraw.signal.set()
            self.generating = False
            self.queue.task_done()

    async def run(self, aidraw: AIDRAW):
        signal = asyncio.Event()
        aidraw.signal = signal
        await self.queue.put(aidraw)
        await self.run_()
        await signal.wait()
        return aidraw

    def __len__(self):
        if self.generating:
            return self.queue.qsize() + 1
        else:
            return self.queue.qsize()


class FIFO:
    backends: dict[str, bool]
    all_backends: dict[str, MODEL]

    def __init__(self, novelai_config):
        for i, v in novelai_config:
            if i[0] == "/":
                private = True
        pass

    def min_backend(self, backend):
        i, v = backend
        if v:
            return len(self.all_backends[i])
        else:
            return 999

    async def run(self, aidraw: AIDRAW):
        if aidraw.model:
            pass
        else:
            minback = min(self.backends, key=self.min_backend())
            try:
                return await minback.run(aidraw)
            except:
                queue = minback.queue
                index = self.backends.index(minback)
                # calllater self.backends.insert(index,minback)
                # self.backends.remove(minback)
                pass

    async def run(self, aidraw: AIDRAW, model):
        pass

    async def get_models(self):
        return str(self.backends)

    async def reset(self):
        for i in self.backends:
            i.reset()

    def __len__(self):
        length = 0
        for i in self.backends:
            length += len(i)
        return length
