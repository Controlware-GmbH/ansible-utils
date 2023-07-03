"""Helper class to handle interfaces"""
from __future__ import absolute_import, division, print_function

from ansible_collections.controlware.utils.plugins.module_utils.interface import (
    Interface,
)

__metaclass__ = type


class InterfaceSet:
    def __init__(self, interfaces: list = None):
        self.interfaces = []
        if isinstance(interfaces, list):
            for interface in interfaces:
                self.add(interface)

    def add(self, interface: str | Interface) -> None:
        if isinstance(interface, str):
            add_if = Interface(interface)
        elif isinstance(interface, Interface):
            add_if = interface
        else:
            return
        if add_if in self.interfaces:
            return
        added = False
        for i, i_if in enumerate(self.interfaces):
            if i_if < add_if:
                continue
            if i_if > add_if:
                self.interfaces.insert(i, add_if)
                added = True
                break
        if not added:
            self.interfaces.append(add_if)

    @property
    def string_list(self) -> list[str]:
        return_list = []
        for intf in self.interfaces:
            return_list.append(str(intf))
        return return_list

    def __iter__(self):
        for each in self.interfaces:
            yield each
