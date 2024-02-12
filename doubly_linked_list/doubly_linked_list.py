class Node:
    def __init__(self, v):
        self.value = v
        self.prev = None
        self.next = None

    def __repr__(self):
        return (f"Node(hash={self.__hash__()}, "
                f"value={self.value}, "
                f"prev={self.prev.__hash__() if self.prev else None}, "
                f"next={self.next.__hash__() if self.next else None})")


class LinkedList2:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_in_tail(self, item):
        if self.head is None:
            self.head = item
            item.prev = None
            item.next = None
        else:
            self.tail.next = item
            item.prev = self.tail
        self.tail = item

    def find(self, val) -> Node | None:
        for node in self:
            if node.value == val:
                return node
        return None

    def find_all(self, val):
        return [node for node in self if node.value == val]

    def delete(self, val, all=False):
        node = self.head
        while node is not None:
            if node.value == val:
                if self.head == node:  # if first (head)
                    self.head = node.next
                    if node.next:
                        node.next.prev = None
                if self.tail == node:  # if last (tail)
                    self.tail = node.prev
                if node.prev is not None:
                    node.prev.next = node.next
                    if node.next is not None:
                        node.next.prev = node.prev
                tmp_node = node
                node = tmp_node.next
                del tmp_node
                if not all:  # continue if we should delete all matches
                    return
            else:
                node = node.next

    def clean(self):
        for node in self:
            del node
        self.head = None
        self.tail = None

    def len(self):
        return len([node for node in self])

    def insert(self, afterNode, newNode):
        if afterNode is None:
            if self.tail is None:
                self.head = newNode
                self.tail = newNode
            else:
                self.tail.next = newNode
                newNode.prev = self.tail
                self.tail = newNode
            return
        newNode.next = afterNode.next
        if afterNode.next is not None:
            afterNode.next.prev = newNode
        newNode.prev = afterNode
        afterNode.next = newNode
        if self.tail == afterNode:
            self.tail = newNode

    def add_in_head(self, newNode):
        if self.head:
            newNode.next = self.head
            self.head.prev = newNode
        self.head = newNode

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next

    def _get_nodes(self) -> list[Node]:
        return [node for node in self]
