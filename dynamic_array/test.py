import pytest

from dynamic_array import DynArray


@pytest.fixture()
def get_array_with_not_full_buffer():
    da = DynArray()
    for i in range(10):
        da.append(i)
    return da


@pytest.fixture()
def get_array_with_full_buffer():
    da = DynArray()
    for i in range(16):
        da.append(i)
    return da


@pytest.fixture()
def get_half_filled_array():
    da = DynArray()
    for i in range(65):
        da.append(i)
    da.delete(64)
    return da


def test_insert_without_buffer_oversize(get_array_with_not_full_buffer):
    da = get_array_with_not_full_buffer
    da.insert(1, 10)
    assert da.array[1] == 10
    assert da.array[2] == 1
    assert da.count == 11
    assert da.capacity == 16

    da.insert(11, 11)
    assert da.array[11] == 11
    assert da.count == 12
    assert da.capacity == 16


def test_insert_with_buffer_oversize(get_array_with_full_buffer):
    da = get_array_with_full_buffer
    da.insert(10, 16)
    assert da.array[10] == 16
    assert da.array[11] == 10
    assert da.count == 17
    assert da.capacity == 32


def test_insert_into_incorrect_position(get_array_with_not_full_buffer):
    da = get_array_with_not_full_buffer
    try:
        da.insert(17, 1)
    except IndexError:
        assert True
    try:
        da.insert(-1, 1)
    except IndexError:
        assert True


def test_delete_with_same_buffer_capacity(get_array_with_full_buffer):
    da = get_array_with_full_buffer
    da.delete(15)
    assert da.array[14] == 14
    assert da.count == 15
    assert da.capacity == 16


def test_delete_with_reducing_buffer_size(get_half_filled_array):
    da = get_half_filled_array
    da.delete(10)
    assert da.array[10] == 11
    assert da.count == 63
    assert da.capacity == 85


def test_delete_from_incorrect_position(get_array_with_full_buffer):
    da = get_array_with_full_buffer
    try:
        da.delete(16)
    except IndexError:
        assert True
