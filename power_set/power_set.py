import ctypes


class Block:
    def __init__(self, capacity: int = 2**6):
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
    def __init__(self, _sz: int = 2**6):
        # storage size should be degree of 2
        self._storage = Block(_sz)

    @property
    def size(self) -> int:
        return self._storage.size - self._storage.empty_cells

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
            if (
                self._storage[skip_index] is None
                or self._storage[skip_index] == obj
            ):
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
            self._resize_storage(max(2**6, self._storage.size // 2))

    def __getitem__(self, index: int):
        return self._storage[index]

    def __iter__(self):
        return (
            self._storage[i]
            for i in range(self._storage.size)
            if self._storage[i] is not None
        )

    def __repr__(self):
        return str([el for el in self])


class DictItem:
    def __init__(self, key, value):
        self._key = key
        self._value = value

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    def __hash__(self):
        return hash(self._key)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._key == other.key


class Dict:
    def __init__(self):
        self._items: HashTable = HashTable()

    @property
    def size(self) -> int:
        return self._items.size

    def is_key(self, key):
        return self._items.find(DictItem(key=key, value=None)) is not None

    def put(self, key, value):
        item = self.get(key)
        if item:
            item.value = value
            return
        item = DictItem(key=key, value=value)
        self._items.put(item)

    def get(self, key):
        index = self._items.find(DictItem(key=key, value=None))
        if index is not None:
            return self._items[index].value
        return None

    def remove(self, key):
        obj = DictItem(key=key, value=None)
        self._items.remove(obj)

    def values(self):
        return (item.value for item in self._items)

    def _as_dict(self) -> dict:
        return {item.key: item.value for item in self._items}


class PowerSet:
    def __init__(self):
        # "type" : storage
        self._type_storage: Dict = Dict()

    def size(self):
        size = 0
        for el in self._type_storage.values():
            size += el.size
        return size

    def put(self, value):
        type_ = str(type(value))
        storage: HashTable = self._type_storage.get(type_)
        if storage is None:
            storage = HashTable(2**6)
            self._type_storage.put(key=type_, value=storage)
        storage.put(value)

    def get(self, value):
        type_ = str(type(value))
        storage = self._type_storage.get(type_)
        if storage is None or storage.find(value) is None:
            return False
        return True

    def remove(self, value):
        type_ = str(type(value))
        storage: HashTable = self._type_storage.get(type_)
        if storage is None or storage.find(value) is None:
            return False
        storage.remove(value)
        return True

    def intersection(self, set2) -> "PowerSet":
        new_ps = PowerSet()
        for el in self:
            if not set2.get(el):
                continue
            new_ps.put(el)
        if new_ps.size():
            return new_ps
        return None

    def union(self, set2):
        new_ps = PowerSet()
        for el in self:
            new_ps.put(el)
        for el in set2:
            new_ps.put(el)
        if new_ps.size():
            return new_ps
        return None

    def difference(self, set2):
        new_ps = PowerSet()
        for el in self:
            if set2.get(el):
                continue
            new_ps.put(el)
        if new_ps.size():
            return new_ps
        return None

    def issubset(self, set2):
        for el in set2:
            if not self.get(el):
                return False
        return True

    def __iter__(self):
        for hash_table in self._type_storage.values():
            for el in hash_table:
                yield el
