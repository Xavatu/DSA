class NativeCache:
    def __init__(self, sz: int):
        self._size = sz
        self._slots: list = [None] * self._size
        self._values: list = [None] * self._size
        self._hits: list[int] = [0] * self._size

    def hash_fun(self, key) -> int:
        return hash(key) % self._size

    @property
    def size(self) -> int:
        return self._size

    def _find_index(self, key) -> int | None:
        hash_key = self.hash_fun(key)
        for i in range(self._size):
            square_skip_index = (hash_key + i**2) % self.size
            serial_index = (hash_key + i) % self.size
            if (
                self._slots[square_skip_index] is not None
                and self._slots[square_skip_index] == key
            ):
                return square_skip_index
            if (
                self._slots[serial_index] is not None
                and self._slots[serial_index] == key
            ):
                return serial_index
        return None

    def _get_index_with_min_hits(self) -> int:
        return self._hits.index(min(self._hits))

    def _seek_slot(self, key) -> int:
        index = self._find_index(key)
        if index is not None:
            return index
        hash_key = self.hash_fun(key)
        for i in range(self.size):
            square_skip_index = (hash_key + i**2) % self.size
            serial_index = (hash_key + i) % self.size
            if self._slots[square_skip_index] is None:
                index = square_skip_index
                break
            if (self._slots[serial_index], index) == (None, None):
                index = serial_index
        if index is None:
            # overwrite key with min hits if cache is full
            index = self._get_index_with_min_hits()
        return index

    def put(self, key, value):
        index = self._seek_slot(key)
        self._slots[index] = key
        self._values[index] = value
        self._hits[index] = 0

    def get(self, key):
        index = self._find_index(key)
        if index is None:
            return None
        self._hits[index] += 1
        return self._values[index]

    def clear(self, sz: int = None):
        if sz:
            self._size = sz
        self._slots = [None] * self._size
        self._values: list = [None] * self._size
        self._hits: list[int] = [0] * self._size

    def __repr__(self):
        return str(
            {
                self._slots[i]: {
                    "value": self._values[i],
                    "hits": self._hits[i],
                }
                for i in range(self._size)
                if self._slots[i] is not None
            }
        )
