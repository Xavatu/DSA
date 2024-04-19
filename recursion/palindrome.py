def _recursive_is_palindrome(string: str, _i: int) -> bool:
    if _i == len(string) // 2:
        return True
    if string[_i] != string[-(_i + 1)]:
        return False
    return _recursive_is_palindrome(string, _i + 1)


def is_palindrome(string: str) -> bool:
    return _recursive_is_palindrome(string, 0)
