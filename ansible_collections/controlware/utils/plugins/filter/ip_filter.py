from __future__ import absolute_import, division, print_function
from ipaddress import (
    ip_address,
    ip_interface,
    ip_network,
)

__metaclass__ = type


def ipv4_range(start: str = "0.0.0.0", end: str = "0.0.0.0") -> list[str]:
    """
    ipv4_range will provide a list of all host address between 'start' and 'end' address.
    return list of host addresses.

    Parameters
    ----------
    start: str
        String representing a valid IPv4 address
    end: str
        String representing a valid IPv4 address

    Returns
    -------
    list
        with string elements representing IPv4 addresses

    Examples
    --------
    ipv4_range('10.0.0.1', '10.0.0.3') --> ['10.0.0.1', '10.0.0.2', '10.0.0.3']
    """

    ip_start = ip_address(start)
    ip_end = ip_address(end)

    host_list = []
    i = 0
    while ip_start + i <= ip_end:
        host_list.append(str(ip_start + i))
        i += 1

    return host_list


def ipsort(ip_strings: list, reverse: bool = False) -> list[str]:
    """
    'ipsort' will sort a given list of IP address xor IP networks.

    Parameters
    ----------
    ip_strings: list
        List of IP addresses xor IP networks
    reverse : boolean (default: False)
        If true, list is sorted in reverse direction

    Returns
    -------
    list
        Sorted list of IP addresses or IP networks

    Examples
    --------
    sort_ip(['10.0.1.1', '10.0.0.1']) --> ['10.0.0.1', '10.0.1.1']
    sort_ip(['10.0.1.0/24', '10.0.2.1/32'], reverse=True) --> ['10.0.2.1/32', '10.0.1.0/24']
    """

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
            "ipv4_range": ipv4_range,
            "ipsort": ipsort,
        }
