class Stack:
    def __init__(self):
        self._stack: list = []

    def size(self):
        return len(self._stack)

    def pop(self):
        try:
            return self._stack.pop(0)
        except IndexError:
            return None

    def push(self, value):
        self._stack.insert(0, value)

    def peek(self):
        try:
            return self._stack[0]
        except IndexError:
            return None

    def __repr__(self):
        return str(self._stack)


def check_bracket_sequence(bracket_sequence: str):
    stack = Stack()
    for el in bracket_sequence:
        if stack.peek() == "(" and el == ")":
            stack.pop()
            continue
        stack.push(el)
    if stack.size() > 0:
        return False
    return True


def postfix(expression: str):
    s1 = Stack()
    s2 = Stack()
    for el in expression.split(" ")[::-1]:
        s1.push(el)
    result = None

    while el := s1.pop():
        match el:
            case "+":
                a = s2.pop()
                b = s2.pop()
                s2.push(a + b)
            case "*":
                a = s2.pop()
                b = s2.pop()
                s2.push(a * b)
            case "=":
                result = s2.pop()
            case _:
                try:
                    el = int(el)
                except ValueError:
                    raise
                s2.push(el)

    return result
