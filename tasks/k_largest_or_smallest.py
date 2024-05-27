import heapq


class MinHeap:
    def __init__(self):
        self._storage = []

    def push(self, value):
        heapq.heappush(self._storage, value)

    def pop(self):
        return heapq.heappop(self._storage)

    def peek(self):
        return self._storage[0]


class MaxHeap:
    def __init__(self):
        self._storage = []

    def push(self, value):
        heapq.heappush(self._storage, -value)

    def pop(self):
        return -heapq.heappop(self._storage)

    def peek(self):
        return -self._storage[0]


def k_largest(array: list, k: int):
    max_heap = MaxHeap()
    for i in range(len(array)):
        max_heap.push(array[i])
    return [max_heap.pop() for _ in range(k)]


def k_smallest(array: list, k: int):
    min_heap = MinHeap()
    for i in range(len(array)):
        min_heap.push(array[i])
    return [min_heap.pop() for _ in range(k)]


if __name__ == "__main__":
    arr = [11, 3, 2, 1, 15, 5, 4, 45, 96, 0, 45]
    print(arr)
    print(f"5 largest: {k_largest(arr, 5)}")
    print(f"5 smallest: {k_smallest(arr, 5)}")
