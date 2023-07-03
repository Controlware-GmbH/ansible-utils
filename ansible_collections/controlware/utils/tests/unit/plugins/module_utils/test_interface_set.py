"""Pytest test definitions for InterfaceSet class"""
from __future__ import absolute_import, division, print_function
import pytest
from ansible_collections.controlware.utils.plugins.module_utils.interface_set import (
    InterfaceSet,
)

__metaclass__ = type


TEST_INIT_STRINGS = [
    (
        ["Loopback1", "Loopback0", "Loopback0", "Loopback2"],
        ["Loopback0", "Loopback1", "Loopback2"],
    ),
    (
        ["Ethernet1", "Ethernet1/2.100", "Ethernet1/2", "Ethernet1/1"],
        ["Ethernet1", "Ethernet1/1", "Ethernet1/2", "Ethernet1/2.100"],
    ),
    (
        [
            "GigabitEthernet1/41",
            "GigabitEthernet1/30",
            "GigabitEthernet1/17",
            "GigabitEthernet1/4",
        ],
        [
            "GigabitEthernet1/4",
            "GigabitEthernet1/17",
            "GigabitEthernet1/30",
            "GigabitEthernet1/41",
        ],
    ),
]


class TestCiscoHelperInterfaceSet:
    # Test valid interface names
    @pytest.mark.parametrize("param, result", TEST_INIT_STRINGS)
    def test_names(self, param, result):
        resp = InterfaceSet(param).string_list
        assert resp == result
