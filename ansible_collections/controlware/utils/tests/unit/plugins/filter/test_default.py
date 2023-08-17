from __future__ import absolute_import, division, print_function
import pytest
from jinja2.runtime import Undefined
from ansible_collections.controlware.utils.plugins.filter.default import (
    default,
    FilterModule,
)

__metaclass__ = type


PRIMARY_VALUE_LIST = [1, "ABC", None, Undefined, {}, {"key": "value"}, [1, 2]]
DEFAULT_VALUE_LIST = [
    ["default"],
    [None, 1],
    [None, "abc"],
    [None, None, "2"],
    [{"key": "value"}],
]

f = FilterModule()


class TestDefaultFilter:
    @pytest.mark.parametrize("primary_value", PRIMARY_VALUE_LIST)
    @pytest.mark.parametrize("default_value", DEFAULT_VALUE_LIST)
    def test_default(self, primary_value, default_value):
        resp = default(primary_value, *default_value)
        if (
            isinstance(primary_value, Undefined)
            or primary_value is None
            and len(DEFAULT_VALUE_LIST) >= 1
        ):
            for i in default_value:
                if isinstance(i, Undefined) or i is None or i == "":
                    continue
                assert i == resp
        else:
            assert resp == primary_value

    def test_default_filter(self):
        resp = f.filters()
        assert isinstance(resp, dict)
        assert "default" in resp.keys()
