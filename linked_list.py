class Node:

    def __init__(self, v):
        self.value = v
        self.next = None


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

    def find_all(self, val) -> list[Node] | None:
        return []

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
        pass  # здесь будет ваш код

    def len(self) -> int:
        return 0  # здесь будет ваш код

    def insert(self, afterNode, newNode):
        pass  # здесь будет ваш код
