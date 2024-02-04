import pytest
from linked_list import LinkedList, Node, sum_linked_lists_nodes


@pytest.fixture()
def get_empty_list():
    return LinkedList()


@pytest.fixture()
def get_list_with_one_element():
    list_ = LinkedList()
    node = Node(v=1)
    list_.head = node
    list_.tail = node
    return list_


@pytest.fixture()
def get_list_with_several_elements():
    list_ = LinkedList()
    node1 = Node(v=1)
    node2 = Node(v=2)
    node3 = Node(v=3)
    node4 = Node(v=2)
    node5 = Node(v=4)
    node6 = Node(v=1)
    node7 = Node(v=7)
    node1.next = node2
    node2.next = node3
    node3.next = node4
    node4.next = node5
    node5.next = node6
    node6.next = node7
    list_.head = node1
    list_.tail = node7
    return list_


@pytest.fixture()
def get_node():
    return Node(v=1)


def test_add_in_tail_empty_list(get_empty_list, get_node):
    list_ = get_empty_list
    node = get_node
    list_.add_in_tail(node)
    assert list_.head == node
    assert list_.tail == node


def test_add_in_tail_list_with_several_elements(get_list_with_several_elements,
                                                get_node):
    list_ = get_list_with_several_elements
    node = get_node
    list_.add_in_tail(node)
    assert list_.tail == node


def test_find_empty_list(get_empty_list):
    list_ = get_empty_list
    assert list_.find(1) is None


def test_find_list_with_several_elements(get_list_with_several_elements):
    list_ = get_list_with_several_elements
    nodes = list_._get_nodes()
    assert list_.find(10) is None
    assert list_.find(2) == nodes[1]
    assert list_.find(1) == nodes[0]


def test_find_all_empty_list(get_empty_list):
    list_ = get_empty_list
    assert list_.find_all(1) == []


def test_find_all_list_with_several_elements(get_list_with_several_elements):
    list_ = get_list_with_several_elements
    nodes = list_._get_nodes()
    assert list_.find_all(10) == []
    assert list_.find_all(2) == [nodes[1], nodes[3]]
    assert list_.find_all(1) == [nodes[0], nodes[5]]


def test_delete_one_list_with_one_element(get_list_with_one_element):
    list_ = get_list_with_one_element
    list_.delete(1)
    assert list_.head is None
    assert list_.tail is None


def test_delete_one_list_with_several_elements(get_list_with_several_elements):
    list_ = get_list_with_several_elements
    nodes = list_._get_nodes()
    tail = list_.tail
    list_.delete(1)
    assert list_.head == nodes[1]
    assert list_.tail == tail
    assert [node for node in list_] == [node for node in nodes if
                                        node != nodes[0]]
    list_.delete(1)
    assert [node for node in list_] == [node for node in nodes if
                                        node not in (
                                            nodes[0], nodes[5])]
    assert nodes[4].next == nodes[6]
    list_.delete(7)
    assert [node for node in list_] == [node for node in nodes if
                                        node not in (
                                            nodes[0], nodes[5], nodes[6])]
    assert list_.tail == nodes[4]
    assert nodes[4].next is None


def test_delete_all_list_with_several_elements(get_list_with_several_elements):
    list_ = get_list_with_several_elements
    nodes = list_._get_nodes()
    # 1, 2, 3, 2, 4, 1, 7
    tail = list_.tail
    list_.delete(1, all=True)
    assert list_.head == nodes[1]
    assert list_.tail == tail
    assert [node for node in list_] == [node for node in nodes if
                                        node not in (
                                            nodes[0], nodes[5])]
    assert nodes[4].next == nodes[6]
    nodes = list_._get_nodes()
    # 2, 3, 2, 4, 7
    list_.delete(2, all=True)
    # 3, 4, 7
    assert list_.head == nodes[1]
    assert nodes[1].next == nodes[3]
    assert [node for node in list_] == [node for node in nodes if
                                        node not in (nodes[0], nodes[2])]


def test_clean_list_with_one_element(get_list_with_one_element):
    list_ = get_list_with_one_element
    list_.clean()
    assert list_.head is None
    assert list_.tail is None


def test_clean_list_with_several_elements(get_list_with_several_elements):
    list_ = get_list_with_several_elements
    list_.clean()
    assert list_.head is None
    assert list_.tail is None


def test_len_empty_list(get_empty_list):
    list_ = get_empty_list
    assert list_.len() == 0


def test_len_list_with_one_element(get_list_with_one_element):
    list_ = get_list_with_one_element
    assert list_.len() == 1


def test_len_list_with_several_elements(get_list_with_several_elements):
    list_ = get_list_with_several_elements
    assert list_.len() == 7


def test_insert_empty_list(get_empty_list, get_node):
    list_ = get_empty_list
    node = get_node
    list_.insert(None, node)
    assert list_.head == node
    assert list_.tail == node


def test_insert_after_none_list_with_one_element(get_list_with_one_element,
                                                 get_node):
    list_ = get_list_with_one_element
    nodes = list_._get_nodes()
    node = get_node
    list_.insert(None, node)
    assert list_.head == node
    assert node.next == nodes[0]


def test_insert_after_node_list_with_one_element(get_list_with_one_element,
                                                 get_node):
    list_ = get_list_with_one_element
    nodes = list_._get_nodes()
    node = get_node
    list_.insert(nodes[0], node)
    assert list_.head == nodes[0]
    assert list_.tail == node
    assert nodes[0].next == node


def test_insert_list_with_several_elements(get_list_with_several_elements,
                                           get_node):
    list_ = get_list_with_several_elements
    nodes = list_._get_nodes()
    node = get_node
    list_.insert(nodes[2], node)
    assert nodes[2].next == node
    assert node.next == nodes[3]


def test_sum_linked_lists_nodes(get_list_with_several_elements,
                                get_empty_list):
    list1 = get_list_with_several_elements
    list2 = get_list_with_several_elements
    list3 = get_empty_list

    result_list = sum_linked_lists_nodes(list1, list2)
    assert [node.value for node in result_list] == [2, 4, 6, 4, 8, 2, 14]
    assert result_list.head.value == 2
    assert result_list.head.next.value == 4
    assert result_list.tail.value == 14

    try:
        sum_linked_lists_nodes(list1, list3)
    except ValueError:
        assert True
