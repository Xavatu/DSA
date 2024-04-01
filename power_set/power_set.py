import ctypes


class Block:
    def __init__(self, capacity: int = 2**10):
        self._capacity = capacity
        self._count = 0
        self._array = self._make_array(self._capacity)

    @staticmethod
    def _make_array(new_capacity: int):
        return (new_capacity * ctypes.py_object)(
            *((None) for _ in range(new_capacity))
        )

    def __len__(self) -> int:
        return self._capacity

    def __getitem__(self, i: int):
        if i < 0 or i >= self._capacity:
            raise IndexError("Index is out of bounds")
        return self._array[i]

    def __setitem__(self, i: int, item):
        self.insert(i, item)

    @property
    def size(self) -> int:
        return self._capacity

    @property
    def empty_cells(self) -> int:
        return self._capacity - self._count

    @property
    def fullness(self) -> float:
        return self._count / self._capacity

    def insert(self, i, item):
        if i < 0 or i > self._capacity:
            raise IndexError("Index is out of bounds")
        if self._array[i] is None:
            self._count += 1
        if item is None:
            self._count -= 1
        self._array[i] = item


class RollingHash:
    def __init__(self, p: int = 31, m: int = 10**9 + 7):
        self._p = p
        self._m = m
        self._hash = 0
        self._length = 0

    def __call__(self, s: str) -> int:
        self._length = len(s)
        hash_so_far = 0
        p_pow = 1
        for i in range(self._length):
            hash_so_far = (
                hash_so_far + (1 + ord(s[i]) - ord("a")) * p_pow
            ) % self._m
            p_pow = (p_pow * self._p) % self._m
        self._hash = hash_so_far
        return self._hash


class HashTable:
    def __init__(self, _sz: int = 2**10):
        # storage size should be degree of 2
        self._storage = Block(_sz)
        self._hash1 = RollingHash(p=31, m=10**9 + 7)
        self._hash2 = RollingHash(p=37, m=10**9 + 9)

    def hash_fun(self, value: str) -> int:
        return self._hash1(value) % self._storage.size

    def _skip_fun(self, value: str) -> int:
        pre_hash = self._hash2(value) % (self._storage.size - 1)
        result_hash = pre_hash - (pre_hash - 1) % 2
        return result_hash

    def seek_slot(self, value: str) -> int | None:
        if not self._storage.empty_cells:
            return None
        result_index = None
        for i in range(self._storage.size):
            skip_index = (
                self.hash_fun(value) + i * self._skip_fun(value)
            ) % self._storage.size
            if self._storage[skip_index] is None:
                result_index = skip_index
                break
        return result_index

    def _resize_storage(self, new_size: int):
        old_storage = self._storage
        new_storage = Block(new_size)
        self._storage = new_storage
        # refill storage
        for i in range(old_storage.size):
            value = self._storage[i]
            if value is None:
                continue
            new_index = self.seek_slot(value)
            if new_index is None:
                break
            new_storage.insert(new_index, value)

    def put(self, value: str) -> int:
        index = self.seek_slot(value)
        if not index:  # storage is full
            self._resize_storage(new_size=self._storage.size * 2)
            index = self.seek_slot(value)
        self._storage.insert(index, value)
        return index

    def find(self, value: str) -> int | None:
        result_index = None
        for i in range(self._storage.size):
            skip_index = (
                self.hash_fun(value) + i * self._skip_fun(value)
            ) % self._storage.size
            if self._storage[skip_index] == value:
                result_index = skip_index
                break
        return result_index

    def remove(self, value: str):
        index = self.find(value)
        if not index:
            return
        self._storage.insert(index, None)
        if self._storage.fullness < 0.15:
            self._resize_storage(self._storage.size // 2)
