from collections import namedtuple

TextState = namedtuple(
    "TextState",
    [
        "classname",
        "bold",
        "italic",
        "color",
        "lang",
    ],
    defaults=[None, None, None, None, None],
)
