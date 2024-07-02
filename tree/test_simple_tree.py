import pytest

from tree.simple_tree import SimpleTree, SimpleTreeNode

#
#         1
#        / \
#       /   \
#      /     \
#     /       \
#    2         3
#   / \       /|\
#  /   \     / | \
# 4     5   6  7  8
#        \
#         9
#


@pytest.fixture()
def get_test_nodes():
    n1 = SimpleTreeNode(1, None)
    n2 = SimpleTreeNode(2, n1)
    n3 = SimpleTreeNode(3, n1)
    n4 = SimpleTreeNode(4, n2)
    n5 = SimpleTreeNode(5, n2)
    n6 = SimpleTreeNode(6, n3)
    n7 = SimpleTreeNode(7, n3)
    n8 = SimpleTreeNode(8, n3)
    n9 = SimpleTreeNode(9, n5)
    n5.Children.append(n9)
    n2.Children.append(n4)
    n2.Children.append(n5)
    n3.Children.append(n6)
    n3.Children.append(n7)
    n3.Children.append(n8)
    n1.Children.append(n2)
    n1.Children.append(n3)
    return [n1, n2, n3, n4, n5, n6, n7, n8, n9]


@pytest.fixture()
def get_test_tree(get_test_nodes):
    simple_tree = SimpleTree(get_test_nodes[0])
    return simple_tree


def test_inorder(get_test_tree):
    tree = get_test_tree
    assert [el.NodeValue for el in tree.inorder()] == [
        1,
        2,
        4,
        5,
        9,
        3,
        6,
        7,
        8,
    ]


def test_postorder(get_test_tree):
    tree = get_test_tree
    assert [el.NodeValue for el in tree.postorder()] == [
        4,
        9,
        5,
        2,
        6,
        7,
        8,
        3,
        1,
    ]


def test_node_levels(get_test_tree):
    tree = get_test_tree
    assert [el[1] for el in tree.node_levels()] == [2, 3, 2, 1, 2, 2, 2, 1, 0]


def test_add_child(get_test_tree):
    tree = get_test_tree
    n9 = tree.FindNodesByValue(9)[0]
    n10 = SimpleTreeNode(10, None)
    tree.AddChild(n9, n10)
    assert n9.Children[0] == n10
    assert n10.Parent == n9
    assert tree.FindNodesByValue(10)[0]


def test_delete_node(get_test_tree):
    tree = get_test_tree
    n5 = tree.FindNodesByValue(5)[0]
    tree.DeleteNode(n5)
    assert (tree.FindNodesByValue(5), tree.FindNodesByValue(9)) == ([], [])
    n2 = tree.FindNodesByValue(2)[0]
    assert n5 not in n2.Children
    n1 = tree.FindNodesByValue(1)[0]
    tree.DeleteNode(n1)
    assert tree.Root is None


def test_move_node(get_test_tree):
    tree = get_test_tree
    n1 = tree.FindNodesByValue(1)[0]
    n2 = tree.FindNodesByValue(2)[0]
    n3 = tree.FindNodesByValue(3)[0]
    tree.MoveNode(n3, n2)
    assert n3 in n2.Children
    assert n3 not in n1.Children
    assert [el.NodeValue for el in tree.postorder()] == [
        4,
        9,
        5,
        6,
        7,
        8,
        3,
        2,
        1,
    ]


def test_count(get_test_tree):
    tree = get_test_tree
    assert tree.Count() == 9


def test_leaf_count(get_test_tree):
    tree = get_test_tree
    assert tree.LeafCount() == 5


def test_subtree_size(get_test_nodes, get_test_tree):
    nodes = get_test_nodes
    tree = get_test_tree
    subtree_size = tree._subtree_size(tree.Root, {})
    assert [subtree_size[nodes[i]] for i in range(9)] == [
        9,
        4,
        4,
        1,
        2,
        1,
        1,
        1,
        1,
    ]


def test_even_trees(get_test_nodes, get_test_tree):
    nodes = get_test_nodes
    tree = get_test_tree
    assert tree.EvenTrees() == []
    assert tree.even_trees(tree.Root.Children[0]) == [nodes[1], nodes[4]]
    assert tree.even_trees(tree.Root.Children[1]) == []
    tree = SimpleTree(nodes[8])
    assert tree.EvenTrees() == []
