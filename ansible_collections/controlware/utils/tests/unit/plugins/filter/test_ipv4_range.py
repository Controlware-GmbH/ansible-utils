from __future__ import absolute_import, division, print_function
import pytest
from ansible_collections.controlware.utils.plugins.filter.ipv4_range import (
    ipv4_range,
)

__metaclass__ = type


TEST_PAIR_LIST = [
    # start, end, result
    ("0.0.0.0", "0.0.0.2", ["0.0.0.0", "0.0.0.1", "0.0.0.2"]),
    ("255.255.255.253", "255.255.255.254", ["255.255.255.253", "255.255.255.254"]),
    ("10.0.0.0", "10.0.0.2", ["10.0.0.0", "10.0.0.1", "10.0.0.2"]),
    ("10.0.0.2", "10.0.0.2", ["10.0.0.2"]),
    ("10.0.0.3", "10.0.0.2", []),
]


class TestIpv4RangeFilter:
    # pylint: disable=too-few-public-methods
    @pytest.mark.parametrize("start, end, result", TEST_PAIR_LIST)
    def test_successful(self, start, end, result):
        resp = ipv4_range(start, end)
        assert resp == result
