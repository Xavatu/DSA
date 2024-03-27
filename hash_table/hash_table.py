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

        result_index = None

        for i in range(self.size):
            skip_index = (self.hash_fun(value) + i * self.step) % self.size
            serial_index = (self.hash_fun(value) + i) % self.size

            if self.slots[skip_index] is None:
                result_index = skip_index
                break
            if (self.slots[serial_index], result_index) == (None, None):
                result_index = serial_index

        return result_index

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
            skip_index = (self.hash_fun(value) + i * self.step) % self.size
            serial_index = (self.hash_fun(value) + i) % self.size

            if self.slots[skip_index] is not None and self.slots[skip_index] == value:
                return skip_index
            if self.slots[serial_index] is not None and self.slots[serial_index] == value:
                return serial_index
        return None
