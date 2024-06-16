class Heap:
    def __init__(self):
        self.HeapArray: list[int] = []
        self._size = 0

    def MakeHeap(self, a: list[int], depth: int):
        self._size = 2 ** (depth + 1) - 1
        for i in range(min(len(a), self._size)):
            self.Add(a[i])

    def GetMax(self):
        if not self.HeapArray:
            return -1
        max_ = self.HeapArray[0]
        tmp = self.HeapArray.pop()
        if len(self.HeapArray) == 0:
            return max_
        self.HeapArray[0] = tmp
        i = 0
        while 0 <= i < len(self.HeapArray):
            if (
                self._good_parent(i)
                and self._good_left(i)
                and self._good_right(i)
            ):
                break
            max_child_index = self._max_children_index(i)
            if max_child_index is None:
                break
            self.HeapArray[max_child_index], self.HeapArray[i] = sorted(
                (self.HeapArray[i], self.HeapArray[max_child_index])
            )
            i = max_child_index
        return max_

    def _max_children_index(self, i):
        left_index = 2 * i + 1
        right_index = 2 * i + 2
        if left_index >= len(self.HeapArray):
            return None
        if right_index >= len(self.HeapArray):
            return left_index
        return (left_index, right_index)[
            self.HeapArray[left_index] < self.HeapArray[right_index]
        ]

    def _good_parent(self, i):
        parent_index = int(0.5 * (i - 1 - (i + 1) % 2))
        return (
            self.HeapArray[i] <= self.HeapArray[parent_index]
            if parent_index >= 0
            else True
        )

    def _good_left(self, i):
        left_index = 2 * i + 1
        return (
            self.HeapArray[i] >= self.HeapArray[left_index]
            if left_index < len(self.HeapArray)
            else True
        )

    def _good_right(self, i):
        right_index = 2 * i + 2
        return (
            self.HeapArray[i] >= self.HeapArray[right_index]
            if right_index < len(self.HeapArray)
            else True
        )

    def Add(self, key: int):
        if self._size == len(self.HeapArray):
            return False  # overflow
        self.HeapArray.append(key)
        i = len(self.HeapArray) - 1
        while 0 <= i < len(self.HeapArray):
            parent_index = int(0.5 * (i - 1 - (i + 1) % 2))
            if (
                self._good_parent(i)
                and self._good_left(i)
                and self._good_right(i)
            ):
                break
            self.HeapArray[i], self.HeapArray[parent_index] = sorted(
                (self.HeapArray[i], self.HeapArray[parent_index]),
            )
            i = parent_index
        return True
