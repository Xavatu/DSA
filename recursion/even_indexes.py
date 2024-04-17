def recursive_print_even_index_elements(list_: list[int], _i: int = 0):
    if _i >= len(list_):
        return
    print(list_[_i])
    recursive_print_even_index_elements(list_, _i + 2)
