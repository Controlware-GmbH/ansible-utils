from __future__ import absolute_import, division, print_function

__metaclass__ = type


def sort_cs_int_ranges(ranges_list: list[str]) -> list[str]:
    """
    sort_cs_int_ranges will sort comma-separated integer range strings
    by sorting first integer value in each string.

    Parameters
    ----------
    ranges_list:
        list of comma-separated integer range strings

    Returns
    -------
    list[str]
        list of sorted comma-separated integer range strings

    Example Jinja Code
    ------------------
    {% cs_int_list | controlware.utils.sort_cs_int_ranges() }}

    Examples
    --------
    values: ['13', 2-10', '200-299', '16', '500-501']
    max_length: 20
    returns [2-10', '13', '16', '200-299', '500-501']
    """

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
