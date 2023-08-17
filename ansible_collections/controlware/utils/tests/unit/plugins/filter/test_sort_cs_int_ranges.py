from __future__ import absolute_import, division, print_function
import pytest
from ansible_collections.controlware.utils.plugins.filter.sort_cs_int_ranges import (
    FilterModule,
    sort_cs_int_ranges,
)

__metaclass__ = type


TEST_PAIRS = [
    (["2-6", "17-18", "171", "48"], ["2-6", "17-18", "48", "171"]),
]

f = FilterModule()


class TestSortCiscoIntegerListFilter:
    @pytest.mark.parametrize("unsorted_list, sorted_list", TEST_PAIRS)
    def test_list(self, unsorted_list, sorted_list):
        resp = sort_cs_int_ranges(unsorted_list)
        assert resp == sorted_list

    def test_filter_registration(self):
        resp = f.filters()
        assert isinstance(resp, dict)
        assert "sort_cs_int_ranges" in resp
        assert resp["sort_cs_int_ranges"] == sort_cs_int_ranges
