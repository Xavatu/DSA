# [-5, -3, 1, 2]
# [1, 4, 9, 25
# [-7, -2, 0, 1, 3, 5]
# [0, 1, 4, 9, 25, 49]
#
# [-7, -2, 0, 1, 3, 5]
# [-7, -2] [5, 3, 1, 0]
import datetime
from collections import deque


def absort(array: list[int]) -> list[int]:
    if len(array) == 0:
        return array
    result = deque()
    i, j, k = 0, 1, 0
    while array[i] < 0 <= array[-j]:
        if -array[i] > array[-j]:
            result.appendleft(array[i])
            i += 1
        else:
            result.appendleft(array[-j])
            j += 1
    while j != len(array) - i + 1:
        result.appendleft(array[-j])
        j += 1
    return list(result)


def bench_test():
    print("N\tsorted\tabsort")
    for i in range(0, 10000000, 10000):
        left = int(0.10 * i)
        right = int(0.90 * i)
        test_array = [el for el in range(-left, right)]
        t1 = datetime.datetime.now()
        r1 = sorted(test_array, key=abs)  # timsort
        t2 = datetime.datetime.now()
        r2 = absort(test_array)
        t3 = datetime.datetime.now()
        print(
            f"{len(test_array)}\t{(t2-t1).total_seconds():.6f}\t{(t3-t2).total_seconds():.6f}".replace(
                ".", ","
            )
        )
        assert r1 == r2


bench_test()
