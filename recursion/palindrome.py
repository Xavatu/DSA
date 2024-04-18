def recursive_is_palindrome(string: str, _i: int = 0) -> bool:
    if _i == len(string) // 2:
        return True
    if string[_i] != string[-(_i + 1)]:
        return False
    return recursive_is_palindrome(string, _i + 1)
