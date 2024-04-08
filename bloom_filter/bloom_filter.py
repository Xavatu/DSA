class BloomFilter:
    def __init__(self, f_len: int = 32):
        self._filter_len = f_len
        self._bitarray: int = 0

    def _set_off_bit(self, i: int):
        if i < 0 or i > self._filter_len:
            raise IndexError("index out of bounds")
        self._bitarray &= ~(2**i)

    def _set_on_bit(self, i: int):
        if i < 0 or i > self._filter_len:
            raise IndexError("index out of bounds")
        self._bitarray |= 2**i

    def hash1(self, str1: str) -> int:
        result = 0
        for c in str1:
            code = ord(c)
            result = (result * 17 + code) % self._filter_len
        return result

    def hash2(self, str1: str) -> int:
        result = 0
        for c in str1:
            code = ord(c)
            result = (result * 223 + code) % self._filter_len
        return result

    def add(self, str1: str):
        self._set_on_bit(self.hash1(str1))
        self._set_on_bit(self.hash2(str1))

    def is_value(self, str1: str) -> bool:
        return bool(
            self._bitarray & (2 ** self.hash1(str1) + 2 ** self.hash2(str1))
        )
