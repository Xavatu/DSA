import pytest
from collections import deque

from tree.balanced_binary_search_tree import (
    GenerateBBSTArray,
    _gen_bbst_tree,
    BalancedBST,
)
from tree.binary_search_tree import BSTIterator


@pytest.mark.parametrize(
    "expected",
    [
        [1],
        [3, 2, 4, 1, None, None, None],
        [7, 4, 11, 2, 6, 9, 13, 1, 3, 5, None, 8, 10, 12, None],
        [9, 5, 15, 3, 7, 13, 17, 1, None, None, None, 11, None, None, None],
    ],
)
def test_generate_bbst(expected):
    expected_bbst = expected
    expected = [el for el in expected if el is not None]
    sorted_a = sorted(expected)
    queue = deque()
    queue.append((len(sorted_a) // 2, 0, len(sorted_a) - 1, 0))
    assert _gen_bbst_tree(sorted_a, queue) == expected_bbst
    assert GenerateBBSTArray(sorted(expected)) == expected
    tree = BalancedBST()
    tree.GenerateTree(expected)
    assert [el.NodeKey for el in BSTIterator(tree.Root, "bfs")] == expected_bbst
    assert tree.IsBalanced(tree.Root)
    if tree.Root.LeftChild:
        tree.Root.LeftChild = None
        assert not tree.IsBalanced(tree.Root)
