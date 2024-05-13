class BSTNode:
    def __init__(self, key, val, parent):
        self.NodeKey = key
        self.NodeValue = val
        self.Parent = parent
        self.LeftChild = None
        self.RightChild = None

    def __repr__(self):
        return str(self.__dict__)


class BSTFind:
    def __init__(self):
        self.Node: BSTNode | None = None
        self.NodeHasKey = False
        self.ToLeft = False


class BST:
    def __init__(self, node: BSTNode | None, _count=0):
        self.Root = node
        self._count = _count
        if node is not None and _count == 0:
            self._count = 1

    def _find_node(self, node: BSTNode, key) -> BSTNode:
        if node.NodeKey == key:
            return node
        if node.NodeKey > key:
            return (
                self._find_node(node.LeftChild, key) if node.LeftChild else node
            )
        return (
            self._find_node(node.RightChild, key) if node.RightChild else node
        )

    def FindNodeByKey(self, key) -> BSTFind:
        result = BSTFind()
        if self.Root is None:
            return result
        result.Node = self._find_node(self.Root, key)
        result.NodeHasKey = result.Node.NodeKey == key
        result.ToLeft = result.Node.NodeKey > key
        return result

    def AddKeyValue(self, key, val) -> bool:
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
    def _find_min(node: BSTNode):
        while node.LeftChild is not None:
            node = node.LeftChild
        return node

    @staticmethod
    def _find_max(node: BSTNode):
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

    def DeleteNodeByKey(self, key) -> bool:
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
