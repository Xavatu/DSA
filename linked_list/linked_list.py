class Node:

    def __init__(self, v):
        self.value = v
        self.next = None

    def __repr__(self):
        return (f"Node(hash={self.__hash__()}, "
                f"value={self.value}, "
                f"next={self.next.__hash__() if self.next else None})")

    # def __del__(self):
    #     print(f"{self} was deleted")


class LinkedList:

    def __init__(self):
        self.head = None
        self.tail = None

    def add_in_tail(self, item):
        if self.head is None:
            self.head = item
        else:
            self.tail.next = item
        self.tail = item

    def print_all_nodes(self):
        node = self.head
        while node is not None:
            print(node.value)
            node = node.next

    def find(self, val) -> Node | None:
        node = self.head
        while node is not None:
            if node.value == val:
                return node
            node = node.next
        return None

    def find_all(self, val) -> list[Node]:
        return [node for node in self if node.value == val]

    def delete(self, val, all=False):
        node = self.head
        previous_node = None
        while node is not None:
            if node.value == val:
                if self.head == node:  # if first (head)
                    self.head = node.next
                if self.tail == node:  # if last (tail)
                    self.tail = previous_node
                tmp_node = node
                node = tmp_node.next
                if previous_node is not None:  # if not first (previous exists)
                    previous_node.next = node
                del tmp_node
                if not all:  # continue if we should delete all matches
                    return
            else:
                previous_node = node
                node = node.next

    def clean(self):
        node = self.head
        while node is not None:
            tmp_node = node
            node = tmp_node.next
            del tmp_node
        self.head = None
        self.tail = None

    def len(self) -> int:
        len_ = 0
        for _ in self:
            len_ += 1
        return len_

    def insert(self, afterNode: Node | None, newNode: Node):
        if afterNode is None:
            if self.head is None:
                self.head = newNode
            else:
                newNode.next = self.head.next
                self.head = newNode
            if self.tail is None:
                self.tail = newNode
            return
        newNode.next = afterNode.next
        afterNode.next = newNode
        if self.tail == afterNode:
            self.tail = newNode

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next