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

    def _find_node(self, node: BSTNode, key) -> BSTNode:
        if node.NodeKey == key:
            return node
        if node.NodeKey > key and node.LeftChild:
            return self._find_node(node.LeftChild, key)
        if node.RightChild:
            return self._find_node(node.RightChild, key)
        return node

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

    def FinMinMax(self, FromNode: BSTNode, FindMax: bool) -> BSTNode:
        pass

    def DeleteNodeByKey(self, key) -> bool:
        pass

    def Count(self) -> int:
        return self._count


def find_node(node: BSTNode, key) -> BSTNode | None:
    if node is None:
        return
    if node.NodeKey > key and node.LeftChild:
        return find_node(node.LeftChild, key)
    if node.RightChild:
        return find_node(node.RightChild, key)
    return node
