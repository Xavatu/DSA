def recursive_digits_sum(n: int) -> int:
    if n < 0:
        return recursive_digits_sum(-n)
    if n < 10:
        return n
    return n % 10 + recursive_digits_sum(n // 10)
