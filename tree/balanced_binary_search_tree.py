from collections import deque
from typing import TypeVar


def _gen_bbst_tree(array, queue):
    result = []
    max_depth = 0
    while queue:
        node_index, left, right, depth = queue.popleft()
        if node_index is None:
            result.append(None)
            continue
        result.append(array[node_index])
        if left <= node_index - 1:
            max_depth = depth + 1
            queue.append(
                (
                    left + (node_index - left) // 2,
                    left,
                    node_index - 1,
                    max_depth,
                )
            )
        elif depth < max_depth:
            queue.append((None,) * 4)
        if node_index + 1 <= right:
            max_depth = depth + 1
            queue.append(
                (
                    node_index + (right - node_index) // 2 + 1,
                    node_index + 1,
                    right,
                    max_depth,
                )
            )
        elif depth < max_depth:
            queue.append((None,) * 4)
    return result


def GenerateBBSTArray(a: list[int]) -> list[int]:
    sorted_a = sorted(a)
    queue = deque()
    queue.append((len(sorted_a) // 2, 0, len(sorted_a) - 1, 0))
    return [el for el in _gen_bbst_tree(sorted_a, queue) if el is not None]


TypeBSTNode = TypeVar("TypeBSTNode", bound="BSTNode")
TypeBalancedBST = TypeVar("TypeBalancedBST", bound="BalancedBST")


class BSTNode:
    def __init__(self, key: int, parent: TypeBSTNode | None):
        self.NodeKey = key
        self.Parent = parent
        self.LeftChild = None
        self.RightChild = None
        self.Level = 0


class BalancedBST:
    def __init__(self):
        self.Root: BSTNode | None = None

    def _generate_tree_from_bbst_array(
        self, array: list, i: int, parent: BSTNode | None
    ):
        node = BSTNode(key=array[i], parent=parent)
        node.Level = parent.Level + 1 if parent else 0
        left_index = 2 * i + 1
        if left_index < len(array):
            node.LeftChild = self._generate_tree_from_bbst_array(
                array, left_index, node
            )
        right_index = 2 * i + 2
        if right_index < len(array):
            node.RightChild = self._generate_tree_from_bbst_array(
                array, right_index, node
            )
        return node

    def GenerateTree(self, a: list[int]):
        queue = deque()
        queue.append((len(a) // 2, 0, len(a) - 1, 0))
        tree = _gen_bbst_tree(sorted(a), queue)
        self.Root = self._generate_tree_from_bbst_array(tree, 0, None)

    def _tree_level(self, root_node: BSTNode):
        if root_node is None:
            return 0
        return max(
            root_node.Level,
            self._tree_level(root_node.LeftChild),
            self._tree_level(root_node.RightChild),
        )

    def IsBalanced(self, root_node: BSTNode):
        if root_node is None:
            return True
        return (
            self.IsBalanced(root_node.LeftChild)
            and self.IsBalanced(root_node.RightChild)
            and (
                abs(
                    self._tree_level(root_node.LeftChild)
                    - self._tree_level(root_node.RightChild)
                )
                <= 1
            )
        )
