class Node:
    def __init__(self, v):
        self.value = v
        self.prev = None
        self.next = None

    def __repr__(self):
        return (
            f"Node(hash={self.__hash__()}, "
            f"value={self.value}, "
            f"prev={self.prev.__hash__() if self.prev else None}, "
            f"next={self.next.__hash__() if self.next else None})"
        )


class Deque:
    def __init__(self):
        # like DoublyLinkedList
        self._head: Node | None = None
        self._tail: Node | None = None
        self._size: int = 0

    def addFront(self, item):
        new_node = Node(item)
        if self._head is None:
            self._head = new_node
            self._tail = new_node
        else:
            new_node.next = self._head
            self._head.prev = new_node
        self._head = new_node
        self._size += 1

    def addTail(self, item):
        new_node = Node(item)
        if self._tail is None:
            self._tail = new_node
            self._head = new_node
        else:
            self._tail.next = new_node
            new_node.prev = self._tail
        self._tail = new_node
        self._size += 1

    def removeFront(self):
        if self._head is None:
            return None
        removed_node = self._head
        self._head = self._head.next
        if self._head:
            self._head.prev = None
        else:
            self._tail = None
        self._size -= 1
        return removed_node.value

    def removeTail(self):
        if self._tail is None:
            return None
        removed_node = self._tail
        self._tail = self._tail.prev
        if self._tail:
            self._tail.next = None
        else:
            self._head = None
        self._size -= 1
        return removed_node.value

    def size(self) -> int:
        return self._size

    def __iter__(self):
        node = self._head
        while node is not None:
            yield node
            node = node.next

    def __repr__(self):
        return str([node for node in self])


def is_palindrome(string: str):
    d = Deque()
    for symbol in string:
        d.addTail(symbol)
    for i in range(d.size() // 2):
        if d.removeFront() == d.removeTail():
            continue
        else:
            return False
    return True
