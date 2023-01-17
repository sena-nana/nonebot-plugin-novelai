from itertools import groupby


def unpack_version(s: str):
    return [
        int("".join(list(i))) if is_digit else "".join(list(i))
        for is_digit, i in groupby(s, key=lambda x: x.isdigit())
    ]
