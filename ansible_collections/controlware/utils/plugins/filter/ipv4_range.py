# pylint: disable=wrong-import-position
from __future__ import absolute_import, division, print_function

DOCUMENTATION = r"""
module: ipv4_range
author: Korte Noack (@kornoa)
version_added: "1.0.0"

short_description: This filter returns a list of all host addresses between
  start and end address.
description: "This filter returns a list of all host addresses between
  start and end address.
  returns:
    type: list
    description: List of IPv4 Address Strings
    elements: str"

options:
  start:
    type: str
    description: String representing the starting IPv4 address
    required: true
  end:
    type: str
    description: String representing the ending IPv4 address
    required: true
"""

EXAMPLES = r"""
ipv4_range('10.0.0.1', '10.0.0.3') --> ['10.0.0.1', '10.0.0.2', '10.0.0.3']
"""

from ipaddress import ip_address

__metaclass__ = type


def ipv4_range(start: str = "0.0.0.0", end: str = "0.0.0.0") -> list:
    ip_start = ip_address(start)
    ip_end = ip_address(end)

    host_list = []
    i = 0
    while ip_start + i <= ip_end:
        host_list.append(str(ip_start + i))
        i += 1

    return host_list


class FilterModule:
    # pylint: disable=too-few-public-methods

    def filters(self):
        return {
            "ipv4_range": ipv4_range,
        }
