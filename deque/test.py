import pytest
from deque import Deque, is_palindrome


@pytest.fixture()
def get_empty_deque():
    return Deque()


@pytest.fixture()
def get_deque_with_one_element():
    deque_ = Deque()
    deque_.addTail(1)
    return deque_


@pytest.fixture()
def get_deque_with_several_elements():
    deque_ = Deque()
    for i in range(10):
        deque_.addTail(i)
    return deque_


def test_add_front_empty_deque(get_empty_deque):
    deque_ = get_empty_deque
    deque_.addFront(1)
    assert deque_.size() == 1
    assert str(deque_) == str([1])
    assert deque_.removeFront() == 1


def test_add_front_deque_with_several_elements(get_deque_with_several_elements):
    deque_ = get_deque_with_several_elements
    size = deque_.size()
    deque_.addFront(-1)
    assert deque_.size() == size + 1
    assert str(deque_) == str([i - 1 for i in range(11)])
    assert deque_.removeFront() == -1


def test_add_tail_empty_deque(get_empty_deque):
    deque_ = get_empty_deque
    deque_.addTail(1)
    assert deque_.size() == 1
    assert str(deque_) == str([1])
    assert deque_.removeTail() == 1


def test_add_tail_deque_with_several_elements(get_deque_with_several_elements):
    deque_ = get_deque_with_several_elements
    size = deque_.size()
    deque_.addTail(10)
    assert deque_.size() == size + 1
    assert str(deque_) == str([i for i in range(11)])
    assert deque_.removeTail() == 10


def test_remove_front_empty_deque(get_empty_deque):
    deque_ = get_empty_deque
    assert deque_.removeFront() is None


def test_remove_front_deque_with_one_element(get_deque_with_one_element):
    deque_ = get_deque_with_one_element
    removed_element = deque_.removeFront()
    assert removed_element == 1
    assert deque_.size() == 0


def test_remove_front_deque_with_several_elements(
    get_deque_with_several_elements,
):
    deque_ = get_deque_with_several_elements
    size = deque_.size()
    removed_element = deque_.removeFront()
    assert removed_element == 0
    assert deque_.size() == size - 1
    assert str(deque_) == str([i + 1 for i in range(9)])


def test_remove_tail_empty_deque(get_empty_deque):
    deque_ = get_empty_deque
    assert deque_.removeTail() is None


def test_remove_tail_deque_with_one_element(get_deque_with_one_element):
    deque_ = get_deque_with_one_element
    removed_element = deque_.removeTail()
    assert removed_element == 1
    assert deque_.size() == 0


def test_remove_tail_deque_with_several_elements(
    get_deque_with_several_elements,
):
    deque_ = get_deque_with_several_elements
    size = deque_.size()
    removed_element = deque_.removeTail()
    assert removed_element == 9
    assert deque_.size() == size - 1
    assert str(deque_) == str([i for i in range(9)])


def test_is_palindrome():
    assert is_palindrome("1234567890") is False
    assert is_palindrome("0") is True
    assert is_palindrome("") is True
    assert is_palindrome("1111111111") is True
    assert is_palindrome("0123210") is True
    assert is_palindrome("1221") is True
