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


class NativeDictionary:
    def __init__(self, sz: int):
        self.size = sz
        self.slots = [None] * self.size
        self.values = [None] * self.size
        self._hash1 = RollingHash(p=31, m=10**9 + 7)
        self._hash2 = RollingHash(p=37, m=10**9 + 9)

    def _hash_fun(self, key: str) -> int:
        # the probability of a collision is 10^(-9) * 10^(-9) = 10^(-18)
        return int(f"{self._hash1(key)}{self._hash2(key)}")

    def hash_fun(self, key: str) -> int:
        return self._hash_fun(key) % self.size

    def _find_index(self, key: str) -> int | None:
        for i in range(self.size):
            square_skip_index = (self.hash_fun(key) + i**2) % self.size
            serial_index = (self.hash_fun(key) + i) % self.size
            if (
                self.slots[square_skip_index] is not None
                and self.slots[square_skip_index] == key
            ):
                return square_skip_index
            if (
                self.slots[serial_index] is not None
                and self.slots[serial_index] == key
            ):
                return serial_index
        return None

    def _seek_slot(self, key: str) -> int:
        index = self._find_index(key)
        if index is not None:
            return index
        for i in range(self.size):
            square_skip_index = (self.hash_fun(key) + i**2) % self.size
            serial_index = (self.hash_fun(key) + i) % self.size
            if self.slots[square_skip_index] is None:
                index = square_skip_index
                break
            if (self.slots[serial_index], index) == (None, None):
                index = serial_index
        if index is None:
            index = self.hash_fun(
                key
            )  # overwrite slot with new key if slots is full
        return index

    def is_key(self, key: str) -> bool:
        return bool(self._find_index(key))

    def put(self, key: str, value):
        index = self._seek_slot(key)
        self.slots[index] = key
        self.values[index] = value

    def get(self, key: str):
        index = self._find_index(key)
        return None if index is None else self.values[index]
