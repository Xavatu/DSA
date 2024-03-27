class Primes:
    @staticmethod
    def primes_sieve(limit: int):
        a = bytearray(b'\x01') * limit
        a[0:2] = bytearray(b'\x00') * 2

        for (i, isprime) in enumerate(a):
            if isprime:
                yield i
                a[i * i:limit:i] = bytearray(b'\x00') * (-(-(limit - i * i) // i))
