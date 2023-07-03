"""Ansible and Jinja2 filter for sorting interface names of different vendors and platforms"""
from __future__ import absolute_import, division, print_function
from __future__ import annotations
import re
from ansible.errors import AnsibleFilterError
from ansible_collections.controlware.utils.plugins.module_utils.interface_set import (
    InterfaceSet,
)

__metaclass__ = type


class SortInfo:
    plattform_strings = {
        "cisco": {
            "iosxe": ["ios", "iosxe", "ios-xe"],
            "nxos": ["nexus", "nxos", "nx-os"],
        }
    }

    def __init__(self) -> None:
        self.interface_lists = {
            "loopbacks": InterfaceSet(),
            "port_channels": InterfaceSet(),
            "tunnels": InterfaceSet(),
            "unspecific": InterfaceSet(),
            "physical": InterfaceSet(),
            "bvis": InterfaceSet(),
            "bdis": InterfaceSet(),
        }

        self.orders = {"cisco": {}}
        for plattform in self.plattform_strings["cisco"]["iosxe"]:
            self.orders["cisco"][plattform] = [
                "loopbacks",
                "port_channels",
                "tunnels",
                "unspecific",
                "physical",
                "bvis",
                "bdis",
            ]
        for plattform in self.plattform_strings["cisco"]["nxos"]:
            self.orders["cisco"][plattform] = [
                "port_channels",
                "tunnels",
                "unspecific",
                "physical",
                "loopbacks",
            ]

        self.sortings = {"cisco": {}}
        for plattform in self.plattform_strings["cisco"]["iosxe"]:
            self.sortings["cisco"][plattform] = {
                "loopbacks": {
                    "regex": "loopback.*",
                    "list": self.interface_lists["loopbacks"],
                },
                "port_channels": {
                    "regex": "port-channel.*",
                    "list": self.interface_lists["port_channels"],
                },
                "tunnels": {
                    "regex": "tunnel.*",
                    "list": self.interface_lists["tunnels"],
                },
                "physical": {
                    "regex": "[a-z]*thernet.*",
                    "list": self.interface_lists["physical"],
                },
                "bvis": {"regex": "bvi.*", "list": self.interface_lists["bvis"]},
                "bdis": {"regex": "bdi.*", "list": self.interface_lists["bdis"]},
                "unspecific": {
                    "regex": ".*",
                    "list": self.interface_lists["unspecific"],
                },
            }
        for plattform in self.plattform_strings["cisco"]["nxos"]:
            self.sortings["cisco"][plattform] = {
                "loopbacks": {
                    "regex": "loopback.*",
                    "list": self.interface_lists["loopbacks"],
                },
                "port_channels": {
                    "regex": "port-channel.*",
                    "list": self.interface_lists["port_channels"],
                },
                "tunnels": {
                    "regex": "tunnel.*",
                    "list": self.interface_lists["tunnels"],
                },
                "physical": {
                    "regex": "([a-z]*thernet|mgmt).*",
                    "list": self.interface_lists["physical"],
                },
                "unspecific": {
                    "regex": ".*",
                    "list": self.interface_lists["unspecific"],
                },
            }


def sort_interface_names(
    interfaces: list[str], vendor: str, plattform: str
) -> list[str]:
    """
    sort_interface_names will sort a list of given interface names
    in respect to given vendor and plattform.

    Parameters
    ----------
    interfaces : list[str]
        List of interface names
    vendor: str
        allowed_values: ['cisco']
    plattform: str
        allowed_values: ['iosxe', 'nxos']
        # Also accepting ios, ios-xe, nexus, nx-os as well as strings with upper cases.

    Returns
    -------
    list[str]
        Sorted list fo interface names

    Example Jinja Code
    ------------------
    {{ interfaces | controlware.utils.sort_interface_names('cisco', 'iosxe') }}

    Examples
    --------
    sort_interface_names(
        ['GigabitEthernet2', 'GigabitEthernet1', 'Loopback0', 'Port-channel1'],
        'iosxe')
        --> ['Loopback0', 'Port-channel1', 'GigabitEthernet1', 'GigabitEthernet2']
    """
    vendor = vendor.lower()
    plattform = plattform.lower()
    sort_info = SortInfo()

    if vendor not in sort_info.orders:
        raise AnsibleFilterError("Vendor '%s' not supported." % vendor)
    vendor_orders = sort_info.orders[vendor]
    vendor_sortings = sort_info.sortings[vendor]

    if plattform not in vendor_orders:
        raise AnsibleFilterError(
            "Plattform '%s' for vendor '%s' not supported." % (plattform, vendor)
        )
    active_order = vendor_orders[plattform]
    active_sorting = vendor_sortings[plattform]

    for interface in interfaces:
        for sort_entry in active_sorting:
            regex = active_sorting[sort_entry]["regex"]
            target_list = active_sorting[sort_entry]["list"]
            if re.match(regex, interface, re.IGNORECASE):
                target_list.add(interface)
                break

    return_list = []
    for order in active_order:
        return_list.extend(sort_info.interface_lists[order].string_list)

    return return_list


class FilterModule:
    @staticmethod
    def filters():
        return {"sort_interface_names": sort_interface_names}
