import pytest

from tree.binary_search_tree import BSTNode, BSTFind, BST


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
    n5 = BSTNode(5, 5, None)
    n2 = BSTNode(2, 2, n5)
    n5.LeftChild = n2
    n7 = BSTNode(7, 7, n5)
    n5.RightChild = n7
    n0 = BSTNode(0, 0, n2)
    n2.LeftChild = n0
    n3 = BSTNode(3, 3, n2)
    n2.RightChild = n3
    n6 = BSTNode(6, 6, n7)
    n7.LeftChild = n6
    n8 = BSTNode(8, 8, n7)
    n7.RightChild = n8
    n4 = BSTNode(4, 4, n3)
    n3.RightChild = n4
    tree = BST(n5, 8)
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
    assert bst.AddKeyValue(9, 9)
    assert bst.Count() == 9
    assert bst.FindNodeByKey(9).Node.NodeKey == 9
    assert bst.FindNodeByKey(9).NodeHasKey
    assert bst.AddKeyValue(-1, -1)
    assert bst.Count() == 10
    assert bst.FindNodeByKey(-1).Node.NodeKey == -1
    assert bst.FindNodeByKey(-1).NodeHasKey
