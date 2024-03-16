class Node:
    def __init__(self, v):
        self.value = v
        self.prev: Node = None
        self.next: Node = None

    def __repr__(self):
        return (
            f"Node(hash={self.__hash__()}, "
            f"value={self.value}, "
            f"prev={self.prev.__hash__() if self.prev else None}, "
            f"next={self.next.__hash__() if self.next else None})"
        )


class DummyNode(Node):
    def __init__(self, v):
        super().__init__(v)
        self._dummy = True


class OrderedList:
    def __init__(self, asc: bool):
        self._dummy: Node = DummyNode(0)
        self.__ascending: bool = asc

    @property
    def head(self):
        return self._dummy.next

    @property
    def tail(self):
        return self._dummy.prev

    def compare(self, v1, v2):
        if v1 < v2:
            return -1
        elif v1 > v2:
            return 1
        return 0

    def add(self, value):
        next_node = self.head
        prev_node = self.tail

        while True:
            if next_node and self.compare(next_node.value, value) == (
                -1 if self.__ascending else 1
            ):
                next_node = next_node.next
            else:
                prev_node = next_node.prev if next_node else None
                break
            if prev_node and self.compare(prev_node.value, value) == (
                1 if self.__ascending else -1
            ):
                prev_node = prev_node.prev
            else:
                next_node = prev_node.next if prev_node else None
                break

        new_node = Node(value)
        new_node.next = next_node
        new_node.prev = prev_node
        if next_node:
            next_node.prev = new_node
        else:
            self._dummy.prev = new_node
        if prev_node:
            prev_node.next = new_node
        else:
            self._dummy.next = new_node

    def find(self, val) -> Node | None:
        next_node = self.head
        prev_node = self.tail

        while True:
            if next_node and self.compare(next_node.value, val) == (
                -1 if self.__ascending else 1
            ):
                next_node = next_node.next
            elif next_node and self.compare(next_node.value, val) == 0:
                return next_node
            else:
                return None
            if prev_node and self.compare(prev_node.value, val) == (
                1 if self.__ascending else -1
            ):
                prev_node = prev_node.prev
            elif prev_node and self.compare(prev_node.value, val) == 0:
                return prev_node
            else:
                return None

    def delete(self, val):
        left_node = self.head
        right_node = self.tail

        while True:
            if left_node and self.compare(left_node.value, val) == (
                -1 if self.__ascending else 1
            ):
                left_node = left_node.next
            elif left_node and self.compare(left_node.value, val) == 0:
                if left_node.prev:
                    left_node.prev.next = left_node.next
                else:
                    self._dummy.next = left_node.next
                if left_node.next:
                    left_node.next.prev = left_node.prev
                else:
                    self._dummy.prev = left_node.prev
                break
            else:
                return
            if right_node and self.compare(right_node.value, val) == (
                1 if self.__ascending else -1
            ):
                right_node = right_node.prev
            elif right_node and self.compare(right_node.value, val) == 0:
                if right_node.prev and not isinstance(
                    right_node.prev, DummyNode
                ):
                    if self.compare(right_node.prev.value, val) == 0:
                        right_node = right_node.prev
                    else:
                        if right_node.prev:
                            right_node.prev.next = right_node.next
                        else:
                            self._dummy.next = right_node.next
                        if right_node.next:
                            right_node.next.prev = right_node.prev
                        else:
                            self._dummy.prev = right_node.prev
                        break
            else:
                return

    def clean(self, asc):
        self.__ascending = asc
        self._dummy.next = None
        self._dummy.prev = None

    def len(self) -> int:
        return len(self.get_all())

    def get_all(self) -> list[Node]:
        return [node for node in self]

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next

    def __repr__(self):
        return str(self.get_all())


class OrderedStringList(OrderedList):
    def __init__(self, asc: bool):
        super(OrderedStringList, self).__init__(asc)

    def compare(self, v1: str, v2: str):
        v1 = v1.strip()
        v2 = v2.strip()
        if v1 < v2:
            return -1
        elif v1 > v2:
            return 1
        return 0
