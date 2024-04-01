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


class HashTable:
    def __init__(self, _sz: int = 2**10):
        # storage size should be degree of 2
        self._storage = Block(_sz)

    def hash_fun(self, obj) -> int:
        return hash(obj) % self._storage.size

    def _skip_fun(self, obj) -> int:
        pre_hash = hash(str(obj)) % (self._storage.size - 1)
        result_hash = pre_hash - (pre_hash - 1) % 2
        return result_hash

    def seek_slot(self, obj) -> int | None:
        if not self._storage.empty_cells:
            return None
        result_index = None
        h1 = self.hash_fun(obj)
        h2 = self._skip_fun(obj)
        for i in range(self._storage.size):
            skip_index = (h1 + i * h2) % self._storage.size
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
            obj = old_storage[i]
            if obj is None:
                continue
            new_index = self.seek_slot(obj)
            if new_index is None:
                break
            new_storage.insert(new_index, obj)

    def put(self, obj) -> int:
        index = self.seek_slot(obj)
        if index is None:  # storage is full
            self._resize_storage(new_size=self._storage.size * 2)
            index = self.seek_slot(obj)
        self._storage.insert(index, obj)
        return index

    def find(self, obj) -> int | None:
        result_index = None
        h1 = self.hash_fun(obj)
        h2 = self._skip_fun(obj)
        for i in range(self._storage.size):
            skip_index = (h1 + i * h2) % self._storage.size
            if self._storage[skip_index] == obj:
                result_index = skip_index
                break
        return result_index

    def remove(self, obj):
        index = self.find(obj)
        if index is None:
            return
        self._storage.insert(index, None)
        if self._storage.fullness < 0.15:
            self._resize_storage(max(2**8, self._storage.size // 2))
