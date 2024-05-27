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
        :param order: traversal order ("inorder", "postorder", "levels")
        """
        self._start: SimpleTreeNode = start
        orders = {
            "inorder": self._inorder(self._start),
            "postorder": self._postorder(self._start),
            "levels": self._node_levels(self._start, 0),
        }
        if order not in orders.keys():
            raise ValueError(
                "param 'order' should be in ('inorder', 'postorder', 'levels')"
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

    def __next__(self):
        return next(self._generator)


class SimpleTree:
    def __init__(self, root: SimpleTreeNode | None):
        self.Root: SimpleTreeNode | None = root

    def inorder(self) -> Generator[SimpleTreeNode, Any, None]:
        yield from SimpleTreeIterator(self.Root, "inorder")

    def postorder(self) -> Generator[SimpleTreeNode, Any, None]:
        yield from SimpleTreeIterator(self.Root, "postorder")

    def node_levels(self) -> List[Tuple[SimpleTreeNode, int]]:
        return [el for el in SimpleTreeIterator(self.Root, "levels")]

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
