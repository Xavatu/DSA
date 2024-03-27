import pytest
import os

from hash_table import HashTable, RollingHash

HASH = RollingHash()("12345")


def get_empty_hash_table():
    return HashTable(sz=100, stp=3)


def get_almost_full_hash_table(sz, stp):
    ht = HashTable(sz, stp)
    for i in range(sz - 1):
        ht.put(f"{i}")
    ht.slots[0] = None
    return ht


def test_hash_fun():
    ht = get_empty_hash_table()
    random_string = str(os.urandom(1000))
    assert ht.hash_fun(random_string) == ht.hash_fun(random_string)


def test_seek_slot_empty_hash_table():
    eht = get_empty_hash_table()
    assert eht.hash_fun("12345") == HASH % eht.size
    assert eht.seek_slot("12345") == eht.hash_fun("12345")


@pytest.mark.parametrize(
    "sz, stp, expected",
    [(10, 3, 8), (13, 2, 0), (33, 5, 13)],
)
def test_seek_slot_sz_stp_expected(sz, stp, expected):
    ht = get_almost_full_hash_table(sz, stp)
    assert ht.seek_slot("12345") == expected
    ht.put("12345")
    assert ht.seek_slot("12345") is None


@pytest.mark.parametrize(
    "sz, stp, expected",
    [(10, 3, 8), (13, 2, 0), (33, 5, 13)],
)
def test_put_sz_stp_expected(sz, stp, expected):
    ht = get_almost_full_hash_table(sz, stp)
    assert ht.put("12345") == expected
    ht.put("12345")
    assert ht.put("12345") is None


def test_find_empty_hash_table():
    ht = get_empty_hash_table()
    assert ht.find("12345") is None


@pytest.mark.parametrize(
    "sz, stp, expected",
    [(10, 3, 8), (13, 2, 0), (33, 5, 13)],
)
def test_find_sz_stp_expected(sz, stp, expected):
    ht = get_almost_full_hash_table(sz, stp)
    assert ht.find("12345") is None
    ht.put("12345")
    assert ht.find("12345") == expected
