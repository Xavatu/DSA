class Queue:
    def __init__(self):
        self._queue: list = []

    def __len__(self) -> int:
        return len(self._queue)

    def __repr__(self) -> str:
        return str([el for el in self._queue])

    def enqueue(self, item):
        self._queue.append(item)

    def dequeue(self):
        if len(self) == 0:
            return None
        return self._queue.pop(0)

    def size(self) -> int:
        return len(self)


def queue_cyclic_shift(queue: Queue, n: int):
    for i in range(n % len(queue)):
        queue.enqueue(queue.dequeue())


class Stack:
    def __init__(self):
        self._stack: list = []

    def __repr__(self) -> str:
        return str(self._stack)

    def __len__(self) -> int:
        return len(self._stack)

    def __getitem__(self, i):
        if i < 0 or i >= self.size():
            raise IndexError("Index is out of bounds")
        return self._stack[i]

    def size(self) -> int:
        return len(self)

    def pop(self):
        if len(self) == 0:
            return None
        return self._stack.pop(0)

    def push(self, value):
        self._stack.insert(0, value)

    def peek(self):
        if len(self) == 0:
            return None
        return self._stack[0]


class QueueOnStack:
    def __init__(self):
        self._s1: Stack = Stack()
        self._s2: Stack = Stack()

    def __len__(self) -> int:
        return self.size()

    def __repr__(self) -> str:
        return str([el for el in self._s1] + [el for el in self._s2][::-1])

    def enqueue(self, item):
        self._s1.push(item)

    def dequeue(self):
        if not self._s2:
            while self._s1:
                self._s2.push(self._s1.pop())
        return self._s2.pop()

    def size(self) -> int:
        return self._s1.size() + self._s2.size()
