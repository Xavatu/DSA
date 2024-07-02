from collections import deque
from collections.abc import Iterator
from typing import List, Generator, Any, Tuple


class SimpleTreeNode:
    def __init__(self, val: Any, parent):
        self.NodeValue = val
        self.Parent: SimpleTreeNode | None = parent
        self.Children: List[SimpleTreeNode] = []

    def __repr__(self):
        return str(
            {
                "id": self.__hash__(),
                "val": self.NodeValue,
                "parent": self.Parent.__hash__() if self.Parent else None,
                "children": [child.__hash__() for child in self.Children],
            }
        )


class SimpleTreeIterator(Iterator):
    def __init__(self, start: SimpleTreeNode, order: str):
        """
        :param start: start node for traversal
        :param order: traversal order ("inorder", "postorder", "levels", "bfs")
        """
        self._start: SimpleTreeNode = start
        orders = {
            "inorder": self._inorder(self._start),
            "postorder": self._postorder(self._start),
            "levels": self._node_levels(self._start, 0),
            "bfs": self._bfs(deque([self._start])),
        }
        if order not in orders.keys():
            raise ValueError(
                "param 'order' should be in ('inorder', 'postorder', 'levels', 'bfs')"
            )
        self._generator = orders[order]

    def __iter__(self):
        return self

    def _inorder(
        self, node: SimpleTreeNode
    ) -> Generator[SimpleTreeNode, Any, None]:
        yield node
        for child in node.Children:
            yield from self._inorder(child)

    def _postorder(
        self, node: SimpleTreeNode
    ) -> Generator[SimpleTreeNode, Any, None]:
        for child in node.Children:
            yield from self._postorder(child)
        yield node

    def _node_levels(
        self, node: SimpleTreeNode, level: int
    ) -> Generator[Tuple[SimpleTreeNode, int], Any, None]:
        for child in node.Children:
            yield from self._node_levels(child, level + 1)
        yield node, level

    def _bfs(
        self, queue: deque[SimpleTreeNode]
    ) -> Generator[SimpleTreeNode, Any, None]:
        if not queue:
            return
        node = queue.popleft()
        yield node
        for child in node.Children:
            queue.append(child)
        yield from self._bfs(queue)

    def __next__(self):
        return next(self._generator)


class SimpleTree:
    def __init__(self, root: SimpleTreeNode):
        self.Root: SimpleTreeNode = root

    def inorder(self) -> Generator[SimpleTreeNode, Any, None]:
        yield from SimpleTreeIterator(self.Root, "inorder")

    def postorder(self) -> Generator[SimpleTreeNode, Any, None]:
        yield from SimpleTreeIterator(self.Root, "postorder")

    def node_levels(self) -> List[Tuple[SimpleTreeNode, int]]:
        return [el for el in SimpleTreeIterator(self.Root, "levels")]

    def bfs(self) -> Generator[SimpleTreeNode, Any, None]:
        yield from SimpleTreeIterator(self.Root, "bfs")

    def AddChild(self, ParentNode: SimpleTreeNode, NewChild: SimpleTreeNode):
        NewChild.Parent = ParentNode
        ParentNode.Children.append(NewChild)

    def DeleteNode(self, NodeToDelete: SimpleTreeNode):
        parent_node = NodeToDelete.Parent
        if self.Root == NodeToDelete:
            self.Root = None
            return
        parent_node.Children.remove(NodeToDelete)

    def GetAllNodes(self) -> List[SimpleTreeNode]:
        return [el for el in self.inorder()]

    def FindNodesByValue(self, val: Any) -> List[SimpleTreeNode]:
        return [el for el in self.inorder() if el.NodeValue == val]

    def MoveNode(self, OriginalNode: SimpleTreeNode, NewParent: SimpleTreeNode):
        self.DeleteNode(OriginalNode)
        NewParent.Children.append(OriginalNode)

    def Count(self) -> int:
        return len(self.GetAllNodes())

    def LeafCount(self) -> int:
        return len([el for el in self.postorder() if not el.Children])

    def _subtree_size(
        self, node: SimpleTreeNode, result: dict[SimpleTreeNode, int]
    ) -> dict[SimpleTreeNode, int]:
        size = 1
        for child in node.Children:
            self._subtree_size(child, result)
            size += result[child]
        result.update({node: size})
        return result

    def _even_trees(
        self,
        queue: deque[tuple[SimpleTreeNode, bool]],
        subtree_size: dict[SimpleTreeNode, int],
        result: list[SimpleTreeNode],
    ) -> list[SimpleTreeNode]:
        if not queue:
            return result
        tmp_result = []
        node, parent_edge = queue.popleft()
        num_of_not_even_subtree = 0
        for child in node.Children:
            if subtree_size[child] % 2 == 1:
                num_of_not_even_subtree += 1
                queue.append((child, True))
                continue
            tmp_result.append(node)
            tmp_result.append(child)
            queue.append((child, False))
        if parent_edge or (
            num_of_not_even_subtree >= 1 and num_of_not_even_subtree % 2 == 1
        ):
            result.extend(tmp_result)
            self._even_trees(queue, subtree_size, result)
        return result

    def even_trees(self, node: SimpleTreeNode) -> list[SimpleTreeNode]:
        subtree_size = self._subtree_size(node, {})
        return self._even_trees(deque([(node, False)]), subtree_size, [])

    def EvenTrees(self) -> list[SimpleTreeNode]:
        return self.even_trees(self.Root)
