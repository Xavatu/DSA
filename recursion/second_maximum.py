from typing import TypeVar

Number = TypeVar("Number", int, float)


def _second_max(
    numbers: list[Number],
    _second: int,
    _max: int,
    _i: int,
) -> tuple[Number, Number]:
    if _i == len(numbers):
        return _second, _max
    _second, _max = _second_max(numbers, _second, _max, _i + 1)
    if numbers[_i] >= _max:
        _second = _max
        _max = numbers[_i]
    if _max > numbers[_i] > _second:
        _second = numbers[_i]
    return _second, _max


def second_max(numbers: list[Number]) -> Number | None:
    if len(numbers) < 2:
        return None
    second = min(numbers[0], numbers[1])
    max_ = max(numbers[0], numbers[1])
    return _second_max(numbers, second, max_, 0)[0]
