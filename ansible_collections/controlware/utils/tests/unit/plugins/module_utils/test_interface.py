from __future__ import absolute_import, division, print_function
import pytest
from ansible_collections.controlware.utils.plugins.module_utils.interface import (
    Interface,
)

__metaclass__ = type

TEST_INIT_STRINGS = [
    "Loopback0",
    "GigabitEthernet1/0/1",
    "Ethernet1/1.100",
    "Port-channel1",
    "Port-channel1.100",
]

TEST_EQ_INTERFACE = [
    ("Loopback0", "Loopback0", True),
    ("Loopback0", "Loopback1", False),
    ("Loopback0", "Ethernet0", False),
    ("Ethernet1/1", "Ethernet1/1", True),
    ("Ethernet1/1/10", "Ethernet1/1/10", True),
    ("Ethernet1/1/10.100", "Ethernet1/1/10.100", True),
    ("Ethernet1/1/10", "Ethernet1/1.10", False),
    ("Ethernet1/1/10.1", "Ethernet1/1/10.2", False),
]

TEST_GTE_INTERFACE = [
    ("Loopback0", "Loopback0", False, True),
    ("Loopback0", "Loopback1", False, False),
    ("Loopback1", "Loopback0", True, True),
    ("Loopback0", "Ethernet0", True, True),
    ("Ethernet1/1", "Ethernet1/1", False, True),
    ("Ethernet1/1", "Ethernet1/2", False, False),
    ("Ethernet2/1", "Ethernet1/1", True, True),
    ("Ethernet1/2", "Ethernet1/1", True, True),
    ("Ethernet1/1/10.100", "Ethernet1/1/10.100", False, True),
    ("Ethernet1/1/10.100", "Ethernet1/1/10.101", False, False),
    ("Ethernet1/1/10.101", "Ethernet1/1/10.100", True, True),
    ("Ethernet1/1/10.101", "Ethernet1/1/10", True, True),
    ("Ethernet1/1/10", "Ethernet1/1/10.100", False, False),
]

TEST_LTE_INTERFACE = [
    ("Loopback0", "Loopback0", False, True),
    ("Loopback0", "Loopback1", True, True),
    ("Loopback1", "Loopback0", False, False),
    ("Loopback0", "Ethernet0", False, False),
    ("Ethernet1/1", "Ethernet1/1", False, True),
    ("Ethernet1/1", "Ethernet1/2", True, True),
    ("Ethernet2/1", "Ethernet1/1", False, False),
    ("Ethernet1/2", "Ethernet1/1", False, False),
    ("Ethernet1/1/10.100", "Ethernet1/1/10.100", False, True),
    ("Ethernet1/1/10.100", "Ethernet1/1/10.101", True, True),
    ("Ethernet1/1/10.101", "Ethernet1/1/10.100", False, False),
    ("Ethernet1/1/10.101", "Ethernet1/1/10", False, False),
    ("Ethernet1/1/10", "Ethernet1/1/10.100", True, True),
]


class TestCiscoHelperInterface:
    # Test valid interface names
    @pytest.mark.parametrize("param", TEST_INIT_STRINGS)
    def test_names(self, param):
        resp = str(Interface(param))
        assert resp == param

    # Test interface.__eq__
    @pytest.mark.parametrize("if1, if2, result", TEST_EQ_INTERFACE)
    def test_eq(self, if1, if2, result):
        resp = Interface(if1) == Interface(if2)
        assert resp == result

    # Test interface.__gt__ and  interface.__ge__
    @pytest.mark.parametrize("if1, if2, result_gt, result_ge", TEST_GTE_INTERFACE)
    def test_gt(self, if1, if2, result_gt, result_ge):
        intf1 = Interface(if1)
        intf2 = Interface(if2)
        resp = intf1 > intf2
        assert resp == result_gt
        resp = intf1 >= intf2
        assert resp == result_ge

    # Test interface.__le__
    @pytest.mark.parametrize("if1, if2, result_lt, result_le", TEST_LTE_INTERFACE)
    def test_le(self, if1, if2, result_lt, result_le):
        intf1 = Interface(if1)
        intf2 = Interface(if2)
        resp = intf1 < intf2
        assert resp == result_lt
        resp = intf1 <= intf2
        assert resp == result_le
