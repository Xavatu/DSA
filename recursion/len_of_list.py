def recursive_len_of_list(list_: list) -> int:
    if not list_:
        return 0
    list_.pop(0)
    return 1 + recursive_len_of_list(list_)
