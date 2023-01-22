import mistune
from .renderer import WordRenderer
class Mdparser:
    def __init__(self, text: str) -> None:
        self.children = mistune.markdown(
            text,
            renderer=WordRenderer(),
            plugins=["task_lists", "strikethrough", "url"],
        )

    def __repr__(self) -> str:
        a = "".join([repr(i) + "," for i in self.children])
        return f"Mdparser({a})"

    def __str__(self) -> str:
        return "".join(map(str, self.children))
