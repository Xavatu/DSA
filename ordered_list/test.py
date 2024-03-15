import pytest
from ordered_list import OrderedList, OrderedStringList, Node


@pytest.fixture()
def get_empty_ordered_list():
    return OrderedList(asc=True)


@pytest.fixture()
def get_ordered_list_with_one_element():
    list_ = OrderedList(asc=True)
    list_.add(1)
    return list_


@pytest.fixture()
def get_ordered_list_with_several_elements_asc_true():
    list_ = OrderedList(asc=True)
    list_.add(1)
    list_.add(2)
    list_.add(2)
    list_.add(2)
    list_.add(0)
    list_.add(-1)
    list_.add(3)
    list_.add(5)
    list_.add(6)
    return list_


@pytest.fixture()
def get_ordered_list_with_several_elements_asc_false():
    list_ = OrderedList(asc=False)
    list_.add(1)
    list_.add(2)
    list_.add(2)
    list_.add(2)
    list_.add(0)
    list_.add(-1)
    list_.add(3)
    list_.add(5)
    list_.add(6)
    return list_


def test_add_empty_list(get_empty_ordered_list):
    list_ = get_empty_ordered_list
    list_.add(4)
    assert list_.get_all()[0].value == 4


def test_add_list_with_several_elements_asc_true(
    get_ordered_list_with_several_elements_asc_true,
):
    list_ = get_ordered_list_with_several_elements_asc_true
    list_.add(-2)
    assert list_.get_all()[0].value == -2
    assert list_.get_all()[0].next.value == -1
    assert list_.get_all()[1].prev.value == -2
    list_.add(2)
    assert list_.get_all()[4].value == 2
    assert list_.get_all()[4].next.value == 2
    assert list_.get_all()[4].prev.value == 1
    assert list_.get_all()[3].next.value == 2
    list_.add(7)
    assert list_.get_all()[-1].value == 7
    assert list_.get_all()[-1].prev.value == 6
    assert list_.get_all()[-2].next.value == 7


def test_add_list_with_several_elements_asc_false(
    get_ordered_list_with_several_elements_asc_false,
):
    list_ = get_ordered_list_with_several_elements_asc_false
    list_.add(-2)
    assert list_.get_all()[-1].value == -2
    assert list_.get_all()[-1].prev.value == -1
    assert list_.get_all()[-2].next.value == -2
    list_.add(2)
    assert list_.get_all()[3].value == 2
    assert list_.get_all()[3].next.value == 2
    assert list_.get_all()[3].prev.value == 3
    list_.add(7)
    assert list_.get_all()[0].value == 7
    assert list_.get_all()[0].next.value == 6
    assert list_.get_all()[1].prev.value == 7


def test_find(
    get_ordered_list_with_several_elements_asc_true,
    get_ordered_list_with_several_elements_asc_false,
):
    list_ = get_ordered_list_with_several_elements_asc_true
    assert list_.find(1).value == 1
    assert list_.find(-1).value == -1
    assert list_.find(40) is None

    list_ = get_ordered_list_with_several_elements_asc_false
    assert list_.find(1).value == 1
    assert list_.find(-1).value == -1
    assert list_.find(40) is None


def test_delete_list_with_one_element(get_ordered_list_with_one_element):
    list_ = get_ordered_list_with_one_element
    list_.delete(1)
    assert list_.get_all() == []


def test_delete_list_with_several_elements(
    get_ordered_list_with_several_elements_asc_true,
    get_ordered_list_with_several_elements_asc_false,
):
    list_ = get_ordered_list_with_several_elements_asc_true
    list_.delete(0)
    assert list_.get_all()[1].value == 1
    list_.delete(-1)
    assert list_.get_all()[0].value == 1
    list_.delete(6)
    assert list_.get_all()[-1].value == 5
    first_2_hash = hash(list_.get_all()[1])
    list_.delete(2)
    assert list_.get_all()[1].value == 2
    assert hash(list_.get_all()[1]) != first_2_hash

    list_ = get_ordered_list_with_several_elements_asc_false
    list_.delete(0)
    assert list_.get_all()[-2].value == 1
    list_.delete(-1)
    assert list_.get_all()[-1].value == 1
    list_.delete(6)
    assert list_.get_all()[0].value == 5
    first_2_hash = hash(list_.get_all()[-4])
    list_.delete(2)
    assert list_.get_all()[-3].value == 2
    assert hash(list_.get_all()[-3]) != first_2_hash
