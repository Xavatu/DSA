class Block:
    def __init__(self, capacity: int = 2**5):
        self._capacity: int = capacity
        self._empty_lists: int = capacity
        self._total_elements: int = 0
        self._list_of_lists: list[list] = self._make_array(self._capacity)

    @staticmethod
    def _make_array(new_capacity: int) -> list[list]:
        return [[] for _ in range(new_capacity)]

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def empty_slots(self) -> int:
        return self._empty_lists

    @property
    def size(self) -> int:
        return self._total_elements

    @property
    def fullness(self) -> float:
        return self.size / self.capacity

    def insert(self, i: int, item):
        if i < 0 or i > self._capacity:
            raise IndexError("Index is out of bounds")
        if item in self._list_of_lists[i]:
            return
        if not self._list_of_lists[i]:
            self._empty_lists -= 1
        self._list_of_lists[i].append(item)
        self._total_elements += 1

    def remove(self, i: int, item):
        if i < 0 or i > self._capacity:
            raise IndexError("Index is out of bounds")
        if item in self._list_of_lists[i]:
            self._list_of_lists[i].remove(item)
            if not self._list_of_lists[i]:
                self._empty_lists += 1
            self._total_elements -= 1

    def is_present(self, i: int, item) -> bool:
        return item in self._list_of_lists[i]

    def get_all(self) -> list:
        list_ = []
        for el in self._list_of_lists:
            list_.extend(el)
        return list_


class HashTable:
    def __init__(self, _sz: int = 2**5):
        # storage size should be degree of 2
        self._storage = Block(_sz)

    @property
    def capacity(self) -> int:
        return self._storage.capacity

    @property
    def size(self) -> int:
        return self._storage.size

    def hash_fun(self, obj) -> int:
        return hash(obj) % self.capacity

    def _resize_storage(self, new_size: int):
        old_storage = self._storage
        new_storage = Block(new_size)
        self._storage = new_storage
        # refill storage
        for obj in old_storage.get_all():
            new_index = self.hash_fun(obj)
            new_storage.insert(new_index, obj)

    def put(self, obj) -> int:
        index = self.hash_fun(obj)
        if self._storage.fullness >= 1:
            self._resize_storage(new_size=self._storage.capacity * 2)
            index = self.hash_fun(obj)
        self._storage.insert(index, obj)
        return index

    def find(self, obj) -> int | None:
        index = self.hash_fun(obj)
        if self._storage.is_present(index, obj):
            return index
        return None

    def remove(self, obj):
        index = self.find(obj)
        if index is None:
            return
        self._storage.remove(index, obj)
        if self._storage.fullness < 0.15:
            self._resize_storage(max(2**5, self._storage.size // 2))

    def get_all(self) -> list:
        return self._storage.get_all()


class PowerSet:
    def __init__(self):
        # "type" : storage
        self._type_storage: dict[str, HashTable] = {}
        self._size: int = 0

    def size(self) -> int:
        return self._size

    def _capacity(self):
        size = 0
        for el in self._type_storage.values():
            size += el.capacity
        return size

    def put(self, value):
        type_ = str(type(value))
        storage: HashTable = self._type_storage.get(type_, None)
        if storage is None:
            storage = HashTable(2**5)
            self._type_storage.update({type_: storage})
        prev_storage_size = storage.size
        storage.put(value)
        self._size += storage.size - prev_storage_size

    def get(self, value) -> bool:
        type_ = str(type(value))
        storage: HashTable = self._type_storage.get(type_, None)
        if storage is None or storage.find(value) is None:
            return False
        return True

    def remove(self, value):
        type_ = str(type(value))
        storage: HashTable = self._type_storage.get(type_, None)
        if storage is None or storage.find(value) is None:
            return False
        prev_storage_size = storage.size
        storage.remove(value)
        self._size += storage.size - prev_storage_size
        return True

    def intersection(self, set2) -> "PowerSet":
        new_ps = PowerSet()
        s1, s2 = self, set2
        if self.size() < set2.size():
            s1, s2 = set2, self
        for el in s1:
            if not s2.get(el):
                continue
            new_ps.put(el)
        if new_ps.size():
            return new_ps
        return None

    def union(self, set2) -> "PowerSet":
        new_ps = PowerSet()
        for el in self:
            new_ps.put(el)
        for el in set2:
            new_ps.put(el)
        if new_ps.size():
            return new_ps
        return None

    def difference(self, set2) -> "PowerSet":
        new_ps = PowerSet()
        for el in self:
            if set2.get(el):
                continue
            new_ps.put(el)
        if new_ps.size():
            return new_ps
        return None

    def issubset(self, set2) -> bool:
        for el in set2:
            if not self.get(el):
                return False
        return True

    def get_all(self) -> list:
        list_ = []
        for el in self._type_storage.values():
            list_.extend(el.get_all())
        return list_

    def __iter__(self):
        for ht in self._type_storage.values():
            for el in ht.get_all():
                yield el

    def __repr__(self):
        return "{" + ", ".join(str(el) for el in self.get_all()) + "}"
