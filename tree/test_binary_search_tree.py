import pytest

from tree.binary_search_tree import BSTNode, BSTFind, BST, aBST


#
#         5
#        / \
#       /   \
#      /     \
#     /       \
#    2         7
#   / \       / \
#  /   \     /   \
# 0     3   6     8
#        \
#         4
#


@pytest.fixture()
def get_empty_tree():
    return BST(None)


@pytest.fixture()
def get_test_tree():
    tree = BST(None)
    tree.AddKeyValue(5, 5)
    tree.AddKeyValue(2, 2)
    tree.AddKeyValue(7, 7)
    tree.AddKeyValue(0, 0)
    tree.AddKeyValue(3, 3)
    tree.AddKeyValue(6, 6)
    tree.AddKeyValue(8, 8)
    tree.AddKeyValue(4, 4)
    return tree


@pytest.fixture()
def get_test_abst():
    tree = aBST(3)
    tree.Tree = [8, 3, 10, 1, 6, None, 14, None, None, 4, 7, None, None, 13, 15]
    return tree


def test_find_node_by_key(get_test_tree, get_empty_tree):
    bst = get_empty_tree
    assert bst.FindNodeByKey(0).Node is None
    bst = get_test_tree
    assert bst.FindNodeByKey(7).Node.NodeKey == 7
    assert bst.FindNodeByKey(7).NodeHasKey
    assert bst.FindNodeByKey(0).Node.NodeKey == 0
    assert bst.FindNodeByKey(0).NodeHasKey
    assert bst.FindNodeByKey(1).Node.NodeValue == 0
    assert not bst.FindNodeByKey(1).NodeHasKey
    assert not bst.FindNodeByKey(1).ToLeft
    assert bst.FindNodeByKey(-1).Node.NodeValue == 0
    assert not bst.FindNodeByKey(-1).NodeHasKey
    assert bst.FindNodeByKey(-1).ToLeft


def test_add_key_value(get_test_tree, get_empty_tree):
    bst = get_empty_tree
    assert bst.AddKeyValue(1, 1)
    assert bst.Root.NodeKey == 1
    assert bst.Count() == 1
    bst = get_test_tree
    assert not bst.AddKeyValue(8, 8)
    assert bst.FindNodeByKey(9).Node.NodeKey == 8
    assert bst.AddKeyValue(9, 9)
    assert bst.Count() == 9
    assert bst.FindNodeByKey(9).Node.NodeKey == 9
    assert bst.FindNodeByKey(9).NodeHasKey
    assert bst.FindNodeByKey(8).Node.RightChild.NodeKey == 9
    assert bst.FindNodeByKey(-1).Node.NodeKey == 0
    assert bst.AddKeyValue(-1, -1)
    assert bst.Count() == 10
    assert bst.FindNodeByKey(-1).Node.NodeKey == -1
    assert bst.FindNodeByKey(-1).NodeHasKey
    assert bst.FindNodeByKey(0).Node.LeftChild.NodeKey == -1


def test_find_min_max(get_test_tree):
    bst = get_test_tree
    assert bst.FinMinMax(bst.Root, False).NodeKey == 0
    assert bst.FinMinMax(bst.Root, True).NodeKey == 8
    assert bst.FinMinMax(bst.Root.LeftChild, False).NodeKey == 0
    assert bst.FinMinMax(bst.Root.LeftChild, True).NodeKey == 4


def test_delete_node_by_key(get_test_tree):
    bst = get_test_tree
    assert bst.DeleteNodeByKey(5)
    assert bst.FindNodeByKey(5).Node.NodeKey == 4
    assert not bst.FindNodeByKey(5).ToLeft
    assert bst.Root.NodeKey == 6
    assert bst.DeleteNodeByKey(2)
    assert bst.FindNodeByKey(2).Node.NodeKey == 0
    assert not bst.FindNodeByKey(2).ToLeft


def test_orders(get_test_tree):
    bst = get_test_tree
    assert [el.NodeKey for el in bst.WideAllNodes()] == [5, 2, 7, 0, 3, 6, 8, 4]
    assert [el.NodeKey for el in bst.DeepAllNodes(0)] == [0, 2, 3, 4, 5, 6, 7, 8]
    assert [el.NodeKey for el in bst.DeepAllNodes(1)] == [0, 4, 3, 2, 6, 8, 7, 5]
    assert [el.NodeKey for el in bst.DeepAllNodes(2)] == [5, 2, 0, 3, 4, 7, 6, 8]


def test_mirrored_tree(get_test_tree):
    bst = get_test_tree
    bst = BST.mirror(bst)
    assert [el.NodeKey for el in bst.WideAllNodes()] == [5, 7, 2, 8, 6, 3, 0, 4]
    assert [el.NodeKey for el in bst.DeepAllNodes(0)] == [8, 7, 6, 5, 4, 3, 2, 0]
    assert [el.NodeKey for el in bst.DeepAllNodes(1)] == [8, 6, 7, 4, 3, 0, 2, 5]
    assert [el.NodeKey for el in bst.DeepAllNodes(2)] == [5, 7, 8, 6, 2, 3, 4, 0]


def test_abst(get_test_abst):
    abst = get_test_abst
    assert abst.FindKeyIndex(0) == -7
    assert abst.AddKey(0) == 7
    assert abst.FindKeyIndex(0) == 7
    assert abst.Tree == [8, 3, 10, 1, 6, None, 14, 0, None, 4, 7, None, None, 13, 15]
    assert abst.FindKeyIndex(2) == -8
    assert abst.AddKey(2) == 8
    assert abst.FindKeyIndex(2) == 8
    assert abst.Tree == [8, 3, 10, 1, 6, None, 14, 0, 2, 4, 7, None, None, 13, 15]
    assert abst.FindKeyIndex(9) == -5
    assert abst.AddKey(9) == 5
    assert abst.FindKeyIndex(9) == 5
    assert abst.Tree == [8, 3, 10, 1, 6, 9, 14, 0, 2, 4, 7, None, None, 13, 15]
    assert abst.FindKeyIndex(17) is None
    assert abst.AddKey(17) == -1

