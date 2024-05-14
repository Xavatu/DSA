from collections import deque


def max_on_window(array: list[int], k: int):
    dq = deque()
    i = 0
    result = [0] * (len(array) - k + 1)
    while i < len(array):
        print(f"{i=}, {array[i]=}, {max(0, i - k + 1)=}, {dq=}")
        if dq and (i - dq[0][0] == k):
            popped = dq.popleft()
            print(f"popleft {popped}")
        while dq and dq[-1][1] < array[i]:
            popped = dq.pop()
            print(f"popright {popped}")
            continue
        print("append", array[i])
        dq.append((i, array[i]))
        i += 1
        if i >= k:
            result[i - k] = dq[0][1]
    return result


print(max_on_window([-1, 9, 2, 3, 7, 1, 4, 5, 8], 3))
# [-1, 9, 2, 3, 7, 1, 4, 5, 8] k = 3
# [9, 9, 7, 7, 7, 5, 8]
