import ctypes


class DynArray:
    def __init__(self, size: int = 2**10):
        self._count = 0
        self._capacity = size
        self._array = self._make_array(self._capacity)

    @staticmethod
    def _make_array(new_capacity: int):
        return (new_capacity * ctypes.py_object)()

    def _resize(self, new_capacity: int):
        new_array = self._make_array(new_capacity)
        for i in range(self._count):
            new_array[i] = self._array[i]
        self._array = new_array
        self._capacity = new_capacity

    def append(self, item):
        if self._count == self._capacity:
            self._resize(self._capacity * 2)
        self._array[self._count] = item
        self._count += 1

    def insert(self, i, item):
        if i < 0 or i > self._count:
            raise IndexError("Index is out of bounds")
        if self._count == self._capacity:
            self._resize(self._capacity * 2)
        if self._count == i:
            self._array[i] = item
            self._count += 1
            return
        prev = self._array[i]
        for j in range(i + 1, self._count):
            self._array[j], prev = prev, self._array[j]
        self._array[self._count] = prev
        self._array[i] = item
        self._count += 1

    def delete(self, i):
        if i < 0 or i >= self._count:
            raise IndexError("Index is out of bounds")
        for j in range(i, self._count - 1):
            self._array[j] = self._array[j + 1]
        self._count -= 1
        if self._count < self._capacity / 2:
            self._resize(max(2**10, int(self._capacity / 1.5)))

    def __len__(self):
        return self._count

    def __getitem__(self, i):
        if i < 0 or i >= self._count:
            raise IndexError("Index is out of bounds")
        return self._array[i]
