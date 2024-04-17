from typing import TypeVar

Number = TypeVar("Number", int, float)


def max_(numbers: list[Number], _max: int = 0, _i: int = 0) -> Number | None:
    if _i == len(numbers):
        return _max
    _max = max_(numbers, _max, _i + 1)
    if _max is None or numbers[_i] > _max:
        _max = numbers[_i]
    return _max


def _second_max(
    numbers: list[Number],
    _second: int = None,
    _max: int = None,
    _i: int = 0,
) -> tuple[Number | None, Number | None]:
    if _i == len(numbers):
        return _second, _max
    _second, _max = _second_max(numbers, _second, _max, _i + 1)
    if _max is None or numbers[_i] >= _max:
        _second = _max
        _max = numbers[_i]
    if _max > numbers[_i] and (_second is None or numbers[_i] > _second):
        _second = numbers[_i]
    return _second, _max


def second_max(numbers: list[Number]) -> Number | None:
    return _second_max(numbers)[0]
