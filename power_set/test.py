import datetime
import random
import pytest

from power_set import PowerSet


def get_set_for_test(n: int):
    s = PowerSet()
    for i in range(n):
        s.put(i)
    return s


def test_empty_set():
    s = get_set_for_test(0)
    assert s.size() == 0
    assert s.get_all() == []


def test_put():
    s = get_set_for_test(33)
    s.put("1234")
    assert s.size() == 34
    assert s.get("1234")
    s.put("1234")
    assert s.size() == 34
    s.put(1234)
    assert s.size() == 35
    assert s.get(1234)
    s.put(b"1")
    assert s.size() == 36
    assert s.get(b"1")
    s.put(None)
    assert s.get(None)


def test_get():
    s = get_set_for_test(0)
    assert not s.get("")
    s = get_set_for_test(10)
    assert s.get(0)
    assert s.get(2)
    assert not s.get(10)
    assert not s.get([])
    assert not s.get(None)


def test_remove():
    s = get_set_for_test(10)
    assert s.get(9)
    assert s.size() == 10
    s.remove(9)
    assert not s.get(9)
    assert s.size() == 9
    s.remove(100)
    assert s.size() == 9
    s.put(None)
    assert s.get(None)
    s.remove(None)
    assert not s.get(None)
    for i in range(9):
        s.remove(i)
    assert s.size() == 0


def test_intersection():
    s1 = get_set_for_test(10)
    s2 = get_set_for_test(0)
    assert s1.intersection(s2).size() == 0
    assert s2.intersection(s1).size() == 0
    s2 = get_set_for_test(7)
    assert s1.intersection(s2).size() == 7
    assert s2.intersection(s1) == s1.intersection(s2)


def test_union():
    s1 = get_set_for_test(15)
    s2 = get_set_for_test(0)
    assert s1.union(s2) == s1 == s2.union(s1)
    s2 = get_set_for_test(20)
    assert s1.union(s2) == s2 == s2.union(s1)
    s2 = get_set_for_test(0)
    s2.put(None)
    assert s2.union(s1) == s1.union(s2)
    assert s2.union(s1).size() == 16
    assert s2.union(s1).get(None)
    s1 = get_set_for_test(0)
    s2 = get_set_for_test(0)
    assert s1.union(s2) == s1 == s2 == s2.union(s1)


def test_difference():
    s1 = get_set_for_test(0)
    s2 = get_set_for_test(0)
    assert s1.difference(s2) == s2.difference(s1) == s1 == s2
    s1 = get_set_for_test(10)
    s2 = get_set_for_test(7)
    assert s1.difference(s2).size() == 3
    assert s1.difference(s2).get(7)
    assert s2.difference(s1) == get_set_for_test(0)
    s1 = get_set_for_test(15)
    s2 = get_set_for_test(0)
    s2.put("1234")
    s2.put(1234)
    s2.put(None)
    assert s1.difference(s2) == s1
    assert s2.difference(s1) == s2


def test_issubnet():
    s1 = get_set_for_test(0)
    s2 = get_set_for_test(0)
    assert s1.issubset(s2)
    assert s2.issubset(s1)
    s2 = get_set_for_test(10)
    assert not s1.issubset(s2)
    assert s2.issubset(s1)
    s1 = get_set_for_test(7)
    assert not s1.issubset(s2)
    assert s2.issubset(s1)
    s1 = get_set_for_test(0)
    s1.put("None")
    s1.put(None)
    assert s1.size() == 2
    assert not s2.issubset(s1)
    s2 = get_set_for_test(0)
    s2.put(None)
    assert s1.issubset(s2)


def test_timing():
    s1 = get_set_for_test(0)
    for i in range(100000):
        value = random.randint(0, 9999999)
        time1 = datetime.datetime.now()
        s1.put(value)
        s1.get(value)
        s1.get(-1)
        time2 = datetime.datetime.now()
        assert (time2 - time1).total_seconds() < 0.5
    s2 = get_set_for_test(0)
    for i in range(200000):
        value = random.randint(-9999999, 9999999)
        time1 = datetime.datetime.now()
        s2.put(value)
        s2.remove(10000)
        s2.get(10000)
        time2 = datetime.datetime.now()
        assert (time2 - time1).total_seconds() < 0.5
    time1 = datetime.datetime.now()
    assert s1.intersection(s2) == s2.intersection(s1)
    time2 = datetime.datetime.now()
    assert (time2 - time1).total_seconds() < 2
    time1 = datetime.datetime.now()
    assert s1.union(s2)
    time2 = datetime.datetime.now()
    assert (time2 - time1).total_seconds() < 2
    time1 = datetime.datetime.now()
    s2.difference(s1)
    time2 = datetime.datetime.now()
    assert (time2 - time1).total_seconds() < 2
