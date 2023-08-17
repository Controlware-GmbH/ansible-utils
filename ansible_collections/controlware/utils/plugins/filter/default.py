from __future__ import absolute_import, division, print_function

__metaclass__ = type

from jinja2.runtime import Undefined


def default(value: any, *default_values: any) -> any:
    """
    default will test value (inclduing path) if defined and is not None.
    If true return value else test default_value1.
    If false, iterate over default_values:
        If value is defined and not None, return value.
    If runnuing out of default values, return none.

    Parameters
    ----------
    value : any
        Ansible default value to look up
    default_values: single value or list of values to find return value

    Jinja Example
    -------------
    ip4_address: {{ interface.ip_address |
        controlware.utils.default(host.ip_address, "169.254.9.9") }}

    Returns
    -------
    any
        Default value
    """
    if isinstance(value, Undefined) or value is None:
        # Invalid value - try defaults
        if len(default_values) >= 1:
            # Return the result of another loop
            return default(default_values[0], *default_values[1:])
        return None
    return value


class FilterModule:
    # pylint: disable=too-few-public-methods

    def filters(self):
        return {"default": default}
