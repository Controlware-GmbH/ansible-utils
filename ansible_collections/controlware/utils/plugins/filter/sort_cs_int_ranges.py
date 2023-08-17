# pylint: disable=wrong-import-position
from __future__ import absolute_import, division, print_function

DOCUMENTATION = r"""
module: sort_cs_int_ranges
author: Korte Noack (@kornoa)
version_added: "1.0.0"

short_description: This filter sorts comma-separated integer range strings
  by sorting first integer value in each string.
description: "This filter sorts comma-separated integer range strings
  by sorting first integer value in each string.
  returns:
    type: list
    description: List of comma-separated integer range string
    elements: str"

options:
  ranges_list:
    type: list
    description: List of comma-separated integer range strings
    elements: str
    required: true
"""

EXAMPLES = r"""
sort_cs_int_ranges(["13", "2-10", "200-299", "16", "500-501"])
--> ["2-10", "13", "16", "200-299", "500-501"]
"""

__metaclass__ = type


def sort_cs_int_ranges(ranges_list: list) -> list:
    def get_first_integer_value(int_str):
        return int(int_str.split(",")[0].split("-")[0])

    sorted_list = []
    for range_str in ranges_list:
        i_first = get_first_integer_value(range_str)
        inserted = False
        for pos, string in enumerate(sorted_list):
            if i_first < get_first_integer_value(string):
                sorted_list.insert(pos, range_str)
                inserted = True
                break
        if not inserted:
            sorted_list.append(range_str)
    return sorted_list


class FilterModule:
    # pylint: disable=too-few-public-methods

    def filters(self):
        return {
            "sort_cs_int_ranges": sort_cs_int_ranges,
        }
