def recursive_is_palindrome(string: str) -> bool:
    if len(string) < 2:
        return True
    print(string)
    if string[0] == string[-1]:
        return recursive_is_palindrome(string[1:-1])
    return False
