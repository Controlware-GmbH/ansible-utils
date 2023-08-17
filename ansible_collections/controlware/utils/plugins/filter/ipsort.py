# pylint: disable=wrong-import-position
from __future__ import absolute_import, division, print_function

DOCUMENTATION = r"""
module: ipsort
author: Korte Noack (@kornoa)
version_added: "1.0.0"

short_description: This filter sorts a given list of IP address
  xor IP networks.
description: "This filter sorts a given list of IP address
  xor IP networks.
  returns:
    type: list
    description: IPv4 Address xor Network String
    elements: str"

options:
  ip_strings:
    type: list
    description: List of strings representing IPv4 addresses xor networks
    elements: str
    required: true
  reverse:
    type: bool
    description: Invert sorting order
    required: false
    default: false
"""

EXAMPLES = r"""
sort_ip(['10.0.1.1', '10.0.0.1']) --> ['10.0.0.1', '10.0.1.1']
sort_ip(['10.0.1.0/24', '10.0.2.1/32'], reverse=True) -->
     ['10.0.2.1/32', '10.0.1.0/24']
"""

from ipaddress import (
    ip_address,
    ip_interface,
    ip_network,
)

__metaclass__ = type


def ipsort(ip_strings: list, reverse: bool = False) -> list:
    if not ip_strings:
        return []

    element_type = None
    try:
        ip_address(ip_strings[0])
        element_type = ip_address
    except ValueError:
        try:
            ip_network(ip_strings[0])
            element_type = ip_network
        except ValueError:
            try:
                ip_interface(ip_strings[0])
                element_type = ip_interface
            except ValueError as ve:
                raise ValueError(
                    "Given element is neither IP address, network nor interface."
                ) from ve

    ip_list = []
    for element in ip_strings:
        ip_list.append(element_type(element))
    ip_list = sorted(ip_list, reverse=reverse)

    return_list = []
    for _ip in ip_list:
        return_list.append(str(_ip))

    return return_list


class FilterModule:
    # pylint: disable=too-few-public-methods

    def filters(self):
        return {
            "ipsort": ipsort,
        }
