"""Helper class to handle interface names"""
from __future__ import absolute_import, division, print_function
import re

__metaclass__ = type


class Interface:
    def __init__(
        self, name: str, id_separator: str = "/", sub_interface_separator: str = "."
    ):
        self.type = "None"
        self.ids = []
        self.id_separator = id_separator
        self.sub_interface_separator = sub_interface_separator
        self.sub_interface_id = 0
        if name.count(self.sub_interface_separator) == 1:
            interface_str, sub_interface_str = name.split(self.sub_interface_separator)
            self.sub_interface_id = int(sub_interface_str)
        else:
            interface_str = name
        match = re.match(
            r"([A-Za-z\-]+)([" + self.id_separator + r"\d]+)", interface_str
        )
        if match:
            self.type = match.group(1)
            for _id in match.group(2).split(self.id_separator):
                self.ids.append(int(_id))

    def __str__(self):
        if self.sub_interface_id:
            return (
                self.type
                + self.id_separator.join(map(str, self.ids))
                + self.sub_interface_separator
                + str(self.sub_interface_id)
            )
        return self.type + self.id_separator.join(map(str, self.ids))

    def __eq__(self, other):
        if self.type != other.type:
            return False
        if self.ids != other.ids:
            return False
        return self.sub_interface_id == other.sub_interface_id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        if self.type != other.type:
            return self.type > other.type
        s_id_len = len(self.ids)
        o_id_len = len(other.ids)
        for i in range(s_id_len):
            if i < o_id_len:
                if self.ids[i] != other.ids[i]:
                    return self.ids[i] > other.ids[i]
            else:
                return True
        # Self ids are same as in others. But if other has more ids it is greater than self.
        if o_id_len > s_id_len:
            return False
        # Both positions are absolutely the same. Checking Sub interface information
        return self.sub_interface_id > other.sub_interface_id

    def __ge__(self, other):
        return self.__eq__(other) or self.__gt__(other)

    def __lt__(self, other):
        return not self.__gt__(other) and not self.__eq__(other)

    def __le__(self, other):
        return not self.__gt__(other)
