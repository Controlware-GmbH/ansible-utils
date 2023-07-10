"""Pytest test definitions for sort_interface_names filter"""
from __future__ import absolute_import, division, print_function
import pytest
from ansible_collections.controlware.utils.plugins.filter.sort_interface_names import (
    sort_interface_names,
    FilterModule,
)

__metaclass__ = type

TEST_LIST_PAIRS = [
    # params(interace_list, vendor, platform), result
    (([], "cisco", "iosxe"), []),
    (
        (["GigabitEthernet2", "GigabitEthernet1", "Tunnel1"], "cisco", "IOS-XE"),
        ["Tunnel1", "GigabitEthernet1", "GigabitEthernet2"],
    ),
    (
        (
            ["GigabitEthernet2", "GigabitEthernet1", "Port-channel1", "Loopback0"],
            "cisco",
            "iosxe",
        ),
        ["Loopback0", "Port-channel1", "GigabitEthernet1", "GigabitEthernet2"],
    ),
    (
        (["BDI1", "GigabitEthernet2", "GigabitEthernet1", "Tunnel1"], "cisco", "iosxe"),
        ["Tunnel1", "GigabitEthernet1", "GigabitEthernet2", "BDI1"],
    ),
    (
        (
            [
                "GigabitEthernet1/1.100",
                "GigabitEthernet1/2.50",
                "GigabitEthernet1/1.50",
            ],
            "cisco",
            "iosxe",
        ),
        ["GigabitEthernet1/1.50", "GigabitEthernet1/1.100", "GigabitEthernet1/2.50"],
    ),
    # Nexus
    (
        (
            [
                "loopback0",
                "port-channel1",
                "mgmt0",
                "Ethernet1/2",
                "Ethernet1/1",
                "Tunnel0",
            ],
            "cisco",
            "nxos",
        ),
        [
            "port-channel1",
            "Tunnel0",
            "Ethernet1/1",
            "Ethernet1/2",
            "mgmt0",
            "loopback0",
        ],
    ),
    (
        (
            [
                "Ethernet1/2",
                "Ethernet1/20",
                "Ethernet1/29",
                "Ethernet1/1/1",
                "Ethernet1/1/2",
            ],
            "cisco",
            "nxos",
        ),
        [
            "Ethernet1/1/1",
            "Ethernet1/1/2",
            "Ethernet1/2",
            "Ethernet1/20",
            "Ethernet1/29",
        ],
    ),
]

f = FilterModule()


class TestSortInterfacesFilter:
    #
    @pytest.mark.parametrize("param", TEST_LIST_PAIRS)
    def test_lists(self, param):
        test_param, ret_val = param
        interfaces, vendor, platform = test_param
        resp = sort_interface_names(interfaces, vendor, platform)
        assert resp == ret_val
