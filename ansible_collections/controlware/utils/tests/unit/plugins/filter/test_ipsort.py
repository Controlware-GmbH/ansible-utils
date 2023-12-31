from __future__ import absolute_import, division, print_function
import pytest
from ansible_collections.controlware.utils.plugins.filter.ipsort import (
    ipsort,
)

__metaclass__ = type

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
    (
        ["2001:cafe:0:1::/64", "2001:CAFE::/64", "2001:abba::/32"],
        ["2001:abba::/32", "2001:cafe::/64", "2001:cafe:0:1::/64"],
        False,
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
    (
        ["2001:cafe:0:1::1", "2001:CAFE::2", "2001:abba::FF"],
        ["2001:abba::ff", "2001:cafe::2", "2001:cafe:0:1::1"],
        False,
    ),
]


TEST_INTERFACES = [
    # given, result, reverse
    (
        ["192.168.23.1/27", "10.0.1.2/24", "10.0.1.1/24", "39.0.0.0/8", "0.0.0.0/0"],
        ["0.0.0.0/0", "10.0.1.1/24", "10.0.1.2/24", "39.0.0.0/8", "192.168.23.1/27"],
        False,
    ),
    (
        ["192.168.23.1/27", "10.0.1.2/24", "10.0.1.1/24", "39.0.0.0/8", "0.0.0.0/0"],
        ["192.168.23.1/27", "39.0.0.0/8", "10.0.1.2/24", "10.0.1.1/24", "0.0.0.0/0"],
        True,
    ),
    (
        ["2001:cafe:0:1::1/64", "2001:CAFE::2/64", "2001:abba::FF/96"],
        ["2001:abba::ff/96", "2001:cafe::2/64", "2001:cafe:0:1::1/64"],
        False,
    ),
]


class TestSortIpFilter:
    @pytest.mark.parametrize("given, result, reverse", TEST_NETWORKS)
    def test_networks(self, given, result, reverse):
        assert result == ipsort(ip_strings=given, reverse=reverse)

    @pytest.mark.parametrize("given, result, reverse", TEST_ADDRESSES)
    def test_addresses(self, given, result, reverse):
        assert result == ipsort(ip_strings=given, reverse=reverse)

    @pytest.mark.parametrize("given, result, reverse", TEST_INTERFACES)
    def test_interfaces(self, given, result, reverse):
        assert result == ipsort(ip_strings=given, reverse=reverse)
