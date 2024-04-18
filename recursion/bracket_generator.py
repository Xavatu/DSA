import datetime


def _insert_brackets(bracket_sequence: str, i: int) -> str:
    bracket_sequence = bracket_sequence[:i] + "()" + bracket_sequence[i:]
    return bracket_sequence


def _generate_bracket_sequences(i: int, _sequences: list[str]) -> list[str]:
    if i < 0:
        return _sequences
    if i == 0:
        _sequences.append("()")
        return _sequences
    _generate_bracket_sequences(i - 1, _sequences)
    for j in range(len(_sequences)):
        sequence = _sequences.pop(0)
        new1 = _insert_brackets(sequence, i)
        new2 = _insert_brackets(sequence, i + 1)
        _sequences.append(new1)
        _sequences.append(new2)
    return _sequences


def generate_bracket_sequences(n: int):
    return _generate_bracket_sequences(n - 1, [])


if __name__ == "__main__":
    print("N\ttime")
    for i in range(21):
        time1 = datetime.datetime.now()
        result = generate_bracket_sequences(i)
        time2 = datetime.datetime.now()
        print(f"{i}\t{str((time2 - time1).total_seconds()).replace(".", ",")}")
        # result.sort()
        # print(result)
        # result2 = [el.replace("(", "0").replace(")", "1") for el in result]
        # print(result2)
        # result3 = [int(el, 2) for el in result2]
        # print(result3)
        # for i in range(1, len(result3)):
        #     print(f"{result3[i]} - {result3[i-1]} = {result3[i]-result3[i-1]}")
