from math import log
from collections.abc import Iterator, Generator
from collections import deque
from copy import deepcopy
from typing import Hashable, Any, TypeVar


TypeBSTNode = TypeVar("TypeBSTNode", bound="BSTNode")
TypeBST = TypeVar("TypeBST", bound="BST")


class BSTNode:
    def __init__(self, key: Hashable, val: Any, parent: TypeBSTNode | None):
        self.NodeKey = key
        self.NodeValue = val
        self.Parent = parent
        self.LeftChild: TypeBSTNode | None = None
        self.RightChild: TypeBSTNode | None = None

    def __repr__(self):
        return str(self.__dict__)


class BSTFind:
    def __init__(self):
        self.Node: BSTNode | None = None
        self.NodeHasKey = False
        self.ToLeft = False


class BSTIterator(Iterator):
    def __init__(self, start: BSTNode, order: str):
        """
        :param start: start node for traversal
        :param order: traversal order ("inorder", "postorder", "preorder", "bfs")
        """
        self._start = start
        orders = {
            "inorder": lambda: self._inorder(self._start),
            "postorder": lambda: self._postorder(self._start),
            "preorder": lambda: self._preorder(self._start),
            "bfs": lambda: self._bfs(deque([self._start]), self._start),
        }
        if order not in orders.keys():
            raise ValueError(
                "param 'order' should be in "
                "('inorder', 'postorder', 'preorder', 'bfs')"
            )
        self._generator = orders[order]()

    def __iter__(self):
        return self

    def _bfs(
        self, queue: deque[BSTNode], node: BSTNode
    ) -> Generator[BSTNode, Any, None]:
        if not queue or node is None:
            return
        node = queue.popleft()
        yield node
        if node.LeftChild is not None:
            queue.append(node.LeftChild)
        if node.RightChild is not None:
            queue.append(node.RightChild)
        yield from self._bfs(queue, node)

    def _inorder(self, node: BSTNode) -> Generator[BSTNode, Any, None]:
        if node is None:
            return
        yield from self._inorder(node.LeftChild)
        yield node
        yield from self._inorder(node.RightChild)

    def _postorder(self, node: BSTNode) -> Generator[BSTNode, Any, None]:
        if node is None:
            return
        yield from self._postorder(node.LeftChild)
        yield from self._postorder(node.RightChild)
        yield node

    def _preorder(self, node: BSTNode) -> Generator[BSTNode, Any, None]:
        if node is None:
            return
        yield node
        yield from self._preorder(node.LeftChild)
        yield from self._preorder(node.RightChild)

    def __next__(self):
        return next(self._generator)


class BST:
    def __init__(self, node: BSTNode | None):
        self.Root = node
        self._count = 0

    def _find_node(self, node: BSTNode, key: Hashable) -> BSTNode:
        if node.NodeKey == key:
            return node
        if node.NodeKey > key:
            return (
                self._find_node(node.LeftChild, key) if node.LeftChild else node
            )
        return (
            self._find_node(node.RightChild, key) if node.RightChild else node
        )

    def FindNodeByKey(self, key: Hashable) -> BSTFind:
        result = BSTFind()
        if self.Root is None:
            return result
        result.Node = self._find_node(self.Root, key)
        result.NodeHasKey = result.Node.NodeKey == key
        result.ToLeft = result.Node.NodeKey > key
        return result

    def AddKeyValue(self, key: Hashable, val: Any) -> bool:
        found = self.FindNodeByKey(key)
        if found.Node is None:
            self.Root = BSTNode(key, val, None)
            self._count += 1
            return True
        if found.NodeHasKey:
            return False
        self._count += 1
        if found.ToLeft:
            found.Node.LeftChild = BSTNode(key, val, found.Node)
            return True
        found.Node.RightChild = BSTNode(key, val, found.Node)
        return True

    @staticmethod
    def _find_min(node: BSTNode) -> BSTNode:
        while node.LeftChild is not None:
            node = node.LeftChild
        return node

    @staticmethod
    def _find_max(node: BSTNode) -> BSTNode:
        while node.RightChild is not None:
            node = node.RightChild
        return node

    def FinMinMax(self, FromNode: BSTNode, FindMax: bool) -> BSTNode:
        if FindMax:
            return self._find_max(FromNode)
        return self._find_min(FromNode)

    def _find_replacement(self, node: BSTNode):
        if node.RightChild is None:
            return None
        return self._find_min(node.RightChild)

    def _replace_node(self, node: BSTNode, new_node: BSTNode | None):
        if node.LeftChild:
            node.LeftChild.Parent = new_node
        if node.RightChild:
            node.RightChild.Parent = new_node
        if new_node is not None:
            new_node.Parent = node.Parent
            new_node.LeftChild = node.LeftChild
            new_node.RightChild = node.RightChild
        if node == self.Root:
            self.Root = new_node
            return
        if node.Parent.NodeKey > node.NodeKey:
            node.Parent.LeftChild = new_node
            return
        node.Parent.RightChild = new_node

    def DeleteNodeByKey(self, key: Hashable) -> bool:
        node = self.FindNodeByKey(key).Node
        if node is None:
            return False
        self._count -= 1
        candidate = self._find_replacement(node)
        if candidate is not None:
            self._replace_node(candidate, candidate.RightChild)
        self._replace_node(node, candidate)
        return True

    def Count(self) -> int:
        return self._count

    def WideAllNodes(self) -> tuple[BSTNode]:
        return tuple(BSTIterator(self.Root, "bfs"))

    def DeepAllNodes(self, order: int) -> tuple[BSTNode]:
        """
        :param order: {0: "inorder", 1: "postorder", 2: "preorder"}
        :return:
        """
        orders = {0: "inorder", 1: "postorder", 2: "preorder"}
        return tuple(BSTIterator(self.Root, orders[order]))

    @classmethod
    def mirror(cls, obj: TypeBST) -> TypeBST:
        new_tree = deepcopy(obj)
        for el in new_tree.DeepAllNodes(2):
            el.LeftChild, el.RightChild = el.RightChild, el.LeftChild
        return new_tree


class aBST:
    def __init__(self, depth):
        tree_size = pow(2, depth + 1) - 1
        self.Tree = [None] * tree_size
        self._depth = depth

    def _left_child_index(self, i: int) -> int:
        return 2 * i + 1

    def _right_child_index(self, i: int) -> int:
        return 2 * i + 2

    def FindKeyIndex(self, key: int) -> int | None:
        i = 0
        while log(i + 1, 2) < self._depth + 1:
            node = self.Tree[i]
            if node is None:
                i = -i
                break
            if node == key:
                break
            if node > key:
                i = self._left_child_index(i)
                continue
            i = self._right_child_index(i)
        return i if i < len(self.Tree) else None

    def AddKey(self, key: int) -> int:
        i = self.FindKeyIndex(key)
        if i is None:
            return -1
        if i < 0 or (i == 0 and self.Tree[0] is None):
            i = abs(i)
            self.Tree[i] = key
        return i
