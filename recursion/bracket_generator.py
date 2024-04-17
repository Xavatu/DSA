def _generate_bracket_sequences(
    i: int, _sequences: list[str] = []
) -> list[str]:
    print(i)
    if i == 0:
        _sequences.append(f"(0)1")
        return _sequences
    _generate_bracket_sequences(i - 1, _sequences)
    for j in range(len(_sequences)):
        print(f"{_sequences[j]=} replace={i-1}")
        _sequences[j] = _sequences[j].replace(str(i - 1), f"({i}){i}")
        print("y", _sequences[j])
    return _sequences


print(_generate_bracket_sequences(3))

# (a)b
#
# ()(b)c
# ((a))c
#
# ()((b))d
# ()()(c)d
# (((a)))d
# (())(c)d
#
# ()(((b)))e
# ()(())(d)e
# ()()((c))e
# ()()()(d)e
# ((((a))))e
# ((()))(d)e
# (())((c))e
# (())()(d)e
#
# ()
# 01
#
# ()()
# 0101
# (())
# 0011
#
# ()(())
# 010011
# ()()()
# 010101
# ((()))
# 000111
# (())()
# 001101
