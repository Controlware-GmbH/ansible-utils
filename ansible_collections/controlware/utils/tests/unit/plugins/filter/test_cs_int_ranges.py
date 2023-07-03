"""Pytest test definitions for cs_int_ranges filter"""
from __future__ import absolute_import, division, print_function
import pytest
from ansible_collections.controlware.utils.plugins.filter.cs_int_ranges import (
    FilterModule,
    cs_int_ranges,
)

__metaclass__ = type


TEST_PAIRS = [
    (None, []),
    ([], []),
    ("1-3,5-6", ["1-3,5-6"]),
    ("all", ["all"]),
    ([2, 3, 4, 6, 7, 10, 11, 20], ["2-4,6-7,10-11,20"]),
    ([2, 3, 4, 6, 10, 11, 20, 7], ["2-4,6-7,10-11,20"]),
    (["1", "17", "18", "19", "2"], ["1-2,17-19"]),
    ([1, 4094], ["1,4094"]),
    ([1, 2, 4093, 4094], ["1-2,4093-4094"]),
    ({}, []),
    ({"1": {}, "2": {}, "5": {}, "6": {}}, ["1-2,5-6"]),
    ({"1": {}, "5": {}, "6": {}, "2": {}}, ["1-2,5-6"]),
]
TEST_RAISE = [
    [-1],
    ["1-2-3"],
    ["1-2a?i-3"],
    ["1-2,a?i,-3"],
]
TEST_MAX_INT = [
    ({"1": {}, "2": {}, "5": {}, "6": {}}, 15, ["1-2,5-6"]),
]
TEST_RAISE_MAX_INT = [
    ({"1": {}, "2": {}, "5": {}, "16": {}}, 15),
    ("1-2,4-16", 15),
]
TEST_MAX_LEN = [
    (
        [2001, 2003, 2005, 2007, 2009, 2011, 2013, 2015, 2017, 2019, 2021],
        16,
        ["2001,2003,2005", "2007,2009,2011", "2013,2015,2017", "2019,2021"],
    ),
]
TEST_RAISE_MAX_LEN = [
    ([1, 2], 10),
]
TEST_MAX_LEN_NEXT = [
    (
        [2001, 2003, 2005, 2007, 2009, 2011, 2013, 2015, 2017, 2019, 2021],
        16,
        11,
        ["2001,2003,2005", "2007,2009", "2011,2013", "2015,2017", "2019,2021"],
    ),
]
TEST_RAISE_MAX_LEN_NEXT = [
    ([1, 2], 10),
]

f = FilterModule()


class TestCiscoVlanListFilter:
    @pytest.mark.parametrize("value, expected", TEST_PAIRS)
    def test_correct_values(self, value, expected):
        resp = cs_int_ranges(value)
        assert resp == expected

    @pytest.mark.parametrize("value", TEST_RAISE)
    def test_raise_value_error(self, value):
        try:
            resp = cs_int_ranges(value)
        except ValueError:
            return
        assert resp is None

    @pytest.mark.parametrize("value, m_int, expected", TEST_MAX_INT)
    def test_correct_values_with_max_int(self, value, m_int, expected):
        resp = cs_int_ranges(value, m_int)
        assert resp == expected

    @pytest.mark.parametrize("value, m_int", TEST_RAISE_MAX_INT)
    def test_raise_value_error_with_max_int(self, value, m_int):
        try:
            resp = cs_int_ranges(value, m_int)
        except ValueError:
            return
        assert resp is None

    @pytest.mark.parametrize("value, m_len, expected", TEST_MAX_LEN)
    def test_correct_values_with_max_length(self, value, m_len, expected):
        resp = cs_int_ranges(value, max_length=m_len)
        assert resp == expected

    @pytest.mark.parametrize("value, m_len", TEST_RAISE_MAX_LEN)
    def test_raise_value_error_with_max_length(self, value, m_len):
        try:
            resp = cs_int_ranges(value, max_length=m_len)
        except ValueError:
            return
        assert resp is None

    @pytest.mark.parametrize("value, m_len, m_len_n, expected", TEST_MAX_LEN_NEXT)
    def test_correct_values_with_max_length_next(self, value, m_len, m_len_n, expected):
        resp = cs_int_ranges(value, max_length=m_len, max_length_next=m_len_n)
        assert resp == expected

    @pytest.mark.parametrize("value, m_len_n", TEST_RAISE_MAX_LEN_NEXT)
    def test_raise_value_error_with_max_length_next(self, value, m_len_n):
        try:
            resp = cs_int_ranges(value, max_length=m_len_n)
        except ValueError:
            return
        assert resp is None

    def test_filter_registration(self):
        resp = f.filters()
        assert isinstance(resp, dict)
        assert "cs_int_ranges" in resp
        assert resp["cs_int_ranges"] == cs_int_ranges
