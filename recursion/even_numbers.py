def recursive_print_even_numbers(list_: list[int], _i: int):
    if _i == len(list_):
        return
    if list_[_i] % 2 == 0:
        print(list_[_i])
    recursive_print_even_numbers(list_, _i + 1)
