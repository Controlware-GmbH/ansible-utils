# pylint: disable=wrong-import-position
from __future__ import absolute_import, division, print_function

DOCUMENTATION = r"""
module: default
author: Korte Noack (@kornoa)
version_added: "1.0.0"

short_description: This filter tests and return the given value if defined and
  not None. Otherwise check given other values and returns first defined and
  not None.
description: "This filter tests and return the given value if defined and
  not None. Otherwise check given other values and returns first defined and
  not None.
  returns:
    type: any
    description: value or first non-None default_value"

options:
  values:
    type: any
    description: Data to check
    required: true
  default_values:
    type: any
    description: "Single value or list of values to check as default values"
    required: true
"""

EXAMPLES = r"""
"""

__metaclass__ = type

from jinja2.runtime import Undefined


def default(value: any, *default_values: any) -> any:
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
