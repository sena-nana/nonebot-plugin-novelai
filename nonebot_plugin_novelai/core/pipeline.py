import heapq
from typing import Callable, Type


class Processor:
    """加工器"""

    def run(self):
        ...


class PipelineMeta(type):
    def __new__(cls, name, bases, attrs):
        if "run" not in attrs:
            # 检查是否存在父类，并按继承顺序调用各个父类的run方法
            def run(self):
                for base in bases:
                    if hasattr(base, "run"):
                        getattr(base, "run")(self)

            attrs["run"] = run
        return super().__new__(cls, name, bases, attrs)


class Pipeline(Processor, metaclass=PipelineMeta):
    """
    流水线基类，不包含处理加工器的流程，除非要自己实现，否则应继承子类
    流水线本身也是一个加工器，只是流水线的工作方式不同
    """

    Pipelines = []

    def _register(self, Pipeline, priority, block):
        heapq.heappush(self.Pipelines, (priority, block, Pipeline))

    async def preprocess(self):
        """预处理"""
        ...

    async def on_preprocess(self, func):
        ...

    async def postprocess(self):
        ...

    async def on_postprocess(self, func):
        ...

    def handle(
        self, priority: int, block: bool
    ) -> Callable[[Callable | Type["Processor"]], Type["Processor"]]:
        """通过该函数将函数注册为加工器"""

        def wrapper(subPipeline: Callable | Type["Processor"]) -> Type["Processor"]:
            if isinstance(subPipeline, Callable):
                sub = type(subPipeline.__name__, (Processor,), {})  # TODO
                return sub
            else:
                self._register(subPipeline, priority, block)
                return subPipeline

        return wrapper


class LinearPipeline(Pipeline):
    ...


class ParallelPipeline(Pipeline):
    ...


class SelectivePipeline(Pipeline):
    ...


class Context:
    """事件，只保存数据在各个Pipeline之间传递"""
