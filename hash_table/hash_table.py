class RollingHash:
    def __init__(self, p: int = 31, m: int = 10 ** 9 + 7):
        self._p = p
        self._m = m
        self._hash = 0
        self._length = 0

    def __call__(self, s: str) -> int:
        self._length = len(s)
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

        empty_first = None  # first empty slot index after hash-index

        for i in range(self.size):
            index = (self.hash_fun(value) + i * self.step) % self.size
            if self.slots[index] is None:
                return index
            if self.slots[i] is None and empty_first is None:
                empty_first = i
            if i > index and self.slots[i] is None and (empty_first is None or empty_first < index):
                empty_first = i
        return empty_first

    def put(self, value: str) -> int | None:
        index = self.seek_slot(value)
        if index is None:
            return None
        self.slots[index] = value
        self._empty_slots -= 1
        return index

    def find(self, value: str) -> int | None:
        if self._empty_slots == self.size:
            return None
        for i in range(self.size):
            index = (self.hash_fun(value) + i * self.step) % self.size
            if self.slots[index] is not None and self.slots[index] == value:
                return index
            if self.slots[i] is not None and self.slots[i] == value:
                return i
        return None
