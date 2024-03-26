class RollingHash:
    def __init__(self, p: int = 31, m: int = 10 ** 9 + 7):
        self._p = p
        self._m = m
        self._hash = 0
        self._length = 0

    def __call__(self, s: str) -> int:
        self._length = 0
        hash_so_far = 0
        p_pow = 1
        for i in range(self._length):
            hash_so_far = (hash_so_far + (1 + ord(s[i]) - ord('a')) * p_pow) % self._m
            p_pow = (p_pow * self._p) % self._m
        self._hash = hash_so_far
        return self._hash


class HashTable:
    def __init__(self, sz: int, stp: int):
        self.size = sz
        self.step = stp
        self.slots = [None] * self.size
        self._hash_fun = RollingHash()
        self._empty_slots = self.size

    def hash_fun(self, value: str) -> int:
        return self._hash_fun(value) % self.size

    def seek_slot(self, value: str) -> int | None:
        if not self._empty_slots:
            return None

        indexes = set()
        for i in range(self.size):
            index = (self.hash_fun(value) + i * self.step) % self.size
            if index in indexes:
                break
            if not self.slots[index]:
                return index
            indexes.add(index)

        if len(indexes) == self.size:
            return None

        for i in (set(range(self.size)) - indexes):
            if not self.slots[i]:
                return i

        return None

    def put(self, value: str) -> int | None:
        index = self.seek_slot(value)
        if index is None:
            return None
        self.slots[index] = value
        self._empty_slots -= 1
        return index

    def find(self, value: str) -> int | None:
        index = self.seek_slot(value)
        if not self.seek_slot(value):
            return None
        return index
