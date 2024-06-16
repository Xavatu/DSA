import pytest
from tree.heap import Heap


@pytest.mark.parametrize(
    "test_array, test_depth, expected_make_heap, expected_add",
    [
        ([], 0, [], [9]),
        (
            [9, 7, 6, 5, 4, 3, 2, 1],
            2,
            [9, 7, 6, 5, 4, 3, 2],
            [9, 5, 7, 2, 4, 3, 6],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7],
            3,
            [7, 6, 5, 3, 2, 1, 4, 0],
            [9, 6, 5, 3, 2, 1, 4, 0],
        ),
        (
            [11, 9, 4, 7, 8, 3, 1, 2, 5, 6],
            3,
            [11, 9, 4, 7, 8, 3, 1, 2, 5, 6],
            [9, 9, 4, 7, 8, 3, 1, 2, 5, 6],
        ),
    ],
)
def test_heap(test_array, test_depth, expected_make_heap, expected_add):
    heap_ = Heap()
    heap_.MakeHeap(test_array, test_depth)
    assert heap_.HeapArray == expected_make_heap
    assert heap_.GetMax() == max(test_array, default=-1)
    assert heap_.Add(9) == (len(heap_.HeapArray) <= (2 ** (test_depth + 1) - 1))
    assert heap_.HeapArray == expected_add
