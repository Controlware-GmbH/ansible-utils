# pylint: disable=wrong-import-position
from __future__ import absolute_import, division, print_function

DOCUMENTATION = r"""
module: cs_int_ranges
author: Korte Noack (@kornoa)
version_added: "1.0.0"

short_description: This filter builds a list of comma-separated integer range
  list strings from any given informationen containing integers or
  integer ranges.
description: "This filter builds a list of comma-separated integer range
  list strings from any given informationen containing integers or
  integer ranges.
  returns:
    type: list
    description: List of comma-separated integer range strings
    elements: str"

options:
  values:
    type: list[str] | list[int] | str | dict
    description: Element(s) containing integer information
    required: true
  max_int:
    type: int
    description: "Maximum allowed integer value"
    required: false
    default: 0
  max_length:
    type: int
    description: "Maximum length of first returned string containing
      comma-separated integer ranges (0 or >10)"
    required: false
    default: 0
  max_length_next:
    type: int
    description: "Maximum length of second and continueing returned
      string containing comma-separated integer ranges (>10)"
    required: false
    default: 0
  dual_int_ranges:
    type: bool
    description: "Select parsing mode of a range of two values.
      I.E. select between '10-11' (dual_int_range) and '10,11'."
    required: false
    default: true
"""

EXAMPLES = r"""
"""

__metaclass__ = type


def check_integer_value(value: str | int, max_int: int) -> int:
    value = int(value)
    if value < 0:
        raise ValueError("Integer values must be >= 0")
    if 0 < max_int < value:
        raise ValueError(f"Integer value '{value}' is higher than limit of {max_int}")
    return value


def string_list_to_integer_list(string_list: str, max_int: int) -> list[int]:
    """
    Parse a string representing a comma-separated list of integer ranges
    into a list of integers

    Example:
    str_list: ['100-103,105']
    returns: [100, 101, 102, 103, 105]
    """
    integer_list = []
    for element in string_list.split(","):
        words = element.split("-")
        if len(words) == 1:
            integer_list.append(check_integer_value(element, max_int))
        elif len(words) == 2:
            start, end = words
            integer_list.extend(
                range(
                    check_integer_value(start, max_int),
                    check_integer_value(end, max_int) + 1,
                )
            )
        else:
            raise ValueError(
                f"'{string_list}' is not a valid comma-separated integer range list."
            )
    return integer_list


def cs_int_ranges(
    values: list[str] | list[int] | str | dict,
    max_int: int = 0,
    max_length: int = 0,
    max_length_next: int = None,
    dual_int_ranges: bool = True,
):
    # pylint: disable=too-many-statements
    # pylint: disable=too-many-branches

    """
    cs_int_ranges will try to identify an integer information in values.
    Each integer must be 0<=x<=max_int!
    Then it builds a list of comma-separated integer range list strings.
    Each string is not longer than max_length.

    Parameters
    ----------
    values: None or str or list(str) or dict
    max_int: int # >=0 ; 0 means don't use a limit
    max_length: int # >= 11 # max length of string
    max_length_next: int # >= 11 # max length of each string after first
    dual_int_ranges: bool = True # Select between 10-11 (dual_int_range) and 10,11

    Returns
    -------
    list(str)
        list of comma-separated integer range strings

    Example Jinja Code
    ------------------
    {% allowed_vlans | controlware.utils.cs_int_ranges() }}

    Examples
    --------
    values: ['2-10', '13', '16', '200-299', '500-501']
    max_length: 20
    returns ['2-10,13,16,200-299', '500-501']
    """

    def add_range(str_list: list[str], s_id: int, e_id: int) -> list[str]:
        if s_id < e_id:
            new_range = f"{s_id}-{e_id}"
        else:
            new_range = str(s_id)

        # If list is empty, we just create first entry
        if not str_list:
            return [new_range]

        __max = max_length
        if max_length_next is not None and len(str_list) > 1:
            __max = max_length_next

        # We need to append new_range to last string
        last_str = str_list[-1]
        if 0 < __max < len(last_str) + len(",") + len(new_range):
            str_list.append(new_range)
        else:
            last_str = last_str + "," + new_range
            str_list = str_list[:-1] + [last_str]
        return str_list

    # Check 'max_int' parameter
    if not isinstance(max_int, int) or max_int < 0:
        raise ValueError("Parameter 'max_int' needs to be an integer and >= 0.")
    # Check 'max_length' and 'max_length_next' parameters
    if not isinstance(max_length, int) or (max_length != 0 and max_length < 11):
        raise ValueError("Parameter 'max_length' needs to be an integer and >= 11.")
    if max_length_next is not None and (
        not isinstance(max_length_next, int)
        or (max_length != 0 and max_length_next < 11)
    ):
        raise ValueError(
            "Parameter 'max_length_next' needs to be an integer and >= 11."
        )

    # Check 'values'
    if values is None:
        return []
    if isinstance(values, str):
        if values == "all":
            return ["all"]
        values = string_list_to_integer_list(values, max_int)
    elif isinstance(values, dict):
        values = list(values.keys())
    elif not isinstance(values, list):
        raise ValueError("Given Integer information is not valid.")

    # Convert strings to integers and sort list, if needed:
    input_int_list = []
    for i in values:
        i_int = int(i)
        if 0 < max_int < i_int or i_int < 0:
            raise ValueError(
                f"Integer value '{i_int}' is greather than limit of {max_int}"
            )
        if i_int < 0:
            raise ValueError(f"Unsupported negative integer value '{i_int}'")
        input_int_list.append(i_int)
    if not input_int_list:
        return []
    if len(input_int_list) == 1:
        return [str(input_int_list[0])]

    # We have more than 1 integer
    input_int_list = sorted(input_int_list)
    return_list = []
    end_int = start_int = input_int_list[0]
    for cur_int in input_int_list[1:]:
        if cur_int == end_int + 1:
            # This vlan ID extends current range
            end_int = cur_int
            continue
        # We have a new range
        if not dual_int_ranges and start_int + 1 == end_int:
            return_list = add_range(return_list, start_int, start_int)
            return_list = add_range(return_list, end_int, end_int)
        else:
            return_list = add_range(return_list, start_int, end_int)
        start_int = cur_int
        end_int = cur_int

    if not dual_int_ranges and start_int + 1 == end_int:
        return_list = add_range(return_list, start_int, start_int)
        return_list = add_range(return_list, end_int, end_int)
    else:
        return_list = add_range(return_list, start_int, end_int)

    return return_list


class FilterModule:
    # pylint: disable=too-few-public-methods

    def filters(self):
        return {
            "cs_int_ranges": cs_int_ranges,
        }
