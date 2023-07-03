"""Pytest test definitions for ip filters"""
import pytest
from ansible_collections.controlware.utils.plugins.filter.ip_filter import (
    ipv4_range,
    ipsort,
    FilterModule,
)


TEST_PAIR_LIST = [
    # start, end, result
    ("0.0.0.0", "0.0.0.2", ["0.0.0.0", "0.0.0.1", "0.0.0.2"]),
    ("255.255.255.253", "255.255.255.254", ["255.255.255.253", "255.255.255.254"]),
    ("10.0.0.0", "10.0.0.2", ["10.0.0.0", "10.0.0.1", "10.0.0.2"]),
    ("10.0.0.2", "10.0.0.2", ["10.0.0.2"]),
    ("10.0.0.3", "10.0.0.2", []),
]

f = FilterModule()


class TestIpv4RangeFilter:
    #
    @pytest.mark.parametrize("start, end, result", TEST_PAIR_LIST)
    def test_successful(self, start, end, result):
        resp = ipv4_range(start, end)
        assert resp == result


TEST_NETWORKS = [
    # given, result, reverse
    (
        ["192.168.23.0/24", "10.0.1.0/28", "10.0.1.0/24", "39.0.0.0/8", "0.0.0.0/0"],
        ["0.0.0.0/0", "10.0.1.0/24", "10.0.1.0/28", "39.0.0.0/8", "192.168.23.0/24"],
        False,
    ),
    (
        ["192.168.23.0/24", "10.0.1.0/24", "39.0.0.0/8", "0.0.0.0/0"],
        ["192.168.23.0/24", "39.0.0.0/8", "10.0.1.0/24", "0.0.0.0/0"],
        True,
    ),
]


TEST_ADDRESSES = [
    # given, result, reverse
    (
        ["192.168.23.1", "10.0.1.2", "10.0.1.1", "39.0.0.0", "0.0.0.0"],
        ["0.0.0.0", "10.0.1.1", "10.0.1.2", "39.0.0.0", "192.168.23.1"],
        False,
    ),
    (
        ["192.168.23.1", "10.0.1.2", "10.0.1.1", "39.0.0.0", "0.0.0.0"],
        ["192.168.23.1", "39.0.0.0", "10.0.1.2", "10.0.1.1", "0.0.0.0"],
        True,
    ),
]


class TestSortIpFilter:
    @pytest.mark.parametrize("given, result, reverse", TEST_NETWORKS)
    def test_networks(self, given, result, reverse):
        assert result == ipsort(ip_strings=given, reverse=reverse)

    @pytest.mark.parametrize("given, result, reverse", TEST_ADDRESSES)
    def test_addresses(self, given, result, reverse):
        assert result == ipsort(ip_strings=given, reverse=reverse)
