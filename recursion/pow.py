from typing import TypeVar

Number = TypeVar("Number", int, float)


def recursive_pow(n: Number, m: int) -> Number:
    if m < 0:
        return 1 / (n * recursive_pow(n, -(m + 1)))
    if m == 0:
        return 1
    return n * recursive_pow(n, m - 1)
