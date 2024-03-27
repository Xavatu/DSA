import pytest

from native_dictionary import NativeDictionary


def get_empty_native_dictionary(sz: int):
    return NativeDictionary(sz)


def get_almost_full_native_dictionary(sz: int):
    nd = NativeDictionary(sz)
    for i in range(sz - 1):
        nd.put(key=f"string {i}", value=i)
    return nd


# print(get_almost_full_native_dictionary(33).slots)
@pytest.mark.parametrize(
    "sz, expected",
    [(10, 8), (13, 10), (33, 30)],
)
def test_find_index(sz, expected):
    nd = get_almost_full_native_dictionary(sz)
    assert nd._find_index("string 1") == expected
    assert nd._find_index("12345") is None


@pytest.mark.parametrize(
    "sz, expected",
    [(10, 8), (13, 10), (33, 30)],
)
def test_seek_slot(sz, expected):
    nd = get_almost_full_native_dictionary(sz)
    assert nd._seek_slot("string 1") == expected


@pytest.mark.parametrize(
    "sz",
    [10, 13, 33],
)
def test_is_key(sz):
    nd = get_almost_full_native_dictionary(sz)
    assert nd.is_key("string 1") is True
    assert nd.is_key("12345") is False


@pytest.mark.parametrize(
    "sz, expected",
    [(10, 8), (13, 10), (33, 30)],
)
def test_get(sz, expected):
    nd = get_almost_full_native_dictionary(sz)
    assert nd.get("string 1") == 1
    assert nd.get("12345") is None


def test_put():
    nd = get_almost_full_native_dictionary(100)
    nd.put(key="string 1", value=True)
    assert nd.get("string 1") is True
    nd.put(key="string 99", value=True)
    assert nd.get("string 99") is True
    index = nd._seek_slot("new key")
    old_key = nd.slots[index]
    nd.put(key="new key", value=True)
    assert nd.get("new key") is True
    assert nd.get(old_key) is None
    assert nd.is_key(old_key) is False
