#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: custom_structured_data
short_description: Combine selected variables into a YAML file
version_added: "2.1.0"
description:
  - Selects variables available to the current task by their name prefixes.
  - Combines their mapping values and writes the result to a YAML file on
    the controller.
  - At least one of O(custom_update_prefix) and O(custom_merge_prefix)
    must be supplied.
author:
  - Korte Noack (@kornoa)
options:
  output_folder:
    description:
      - Directory on the controller in which to write the YAML file.
      - The filename is the inventory hostname followed by C(.yml).
      - The directory is created if necessary, except in check mode.
      - Relative paths are resolved against the controller's current working
        directory. A leading tilde is expanded.
      - Must be a non-empty string.
    type: path
    required: true
  custom_update_prefix:
    description:
      - Selects variables for a shallow update of the working mapping.
      - Each top-level key in a selected mapping replaces the corresponding
        key in the working mapping.
      - If supplied, must be a non-empty string.
    type: str
  custom_merge_prefix:
    description:
      - Selects variables for a recursive merge into the working mapping.
      - Nested mappings are merged recursively.
      - Incoming list elements are prepended to existing lists. Duplicate
        elements are retained.
      - For other combinations of value types, the incoming value replaces
        the existing value.
      - If supplied, must be a non-empty string.
    type: str
attributes:
  action:
    description: Processing and file operations run on the controller.
    support: full
  check_mode:
    description: Reports whether the file would change without writing it.
    support: full
  diff_mode:
    description: Does not provide file-content differences.
    support: none
notes:
  - Matches from both prefixes are sorted together by variable name after
    removing the matching prefix. The full variable name breaks ties.
  - If a name matches both prefixes, the longer prefix is used. Identical
    prefixes are rejected.
  - Every selected variable must contain a mapping. If no variables match,
    the resulting mapping is empty.
  - Variables are selected from the effective task variables, which can
    include more than inventory-defined host variables.
  - In check mode, the action reports whether the file would change without
    creating directories or writing the file.
  - An existing destination must be a regular file; a symbolic link at the
    destination is rejected.
  - On POSIX systems, newly written files are private, subject to the process
    umask. Rewriting a file does not preserve its previous permissions.
  - Consider using C(no_log) for sensitive data. The output file itself
    still contains that data.
"""

EXAMPLES = r"""
- name: Combine update and merge fragments
  controlware.utils.custom_structured_data:
    output_folder: /tmp/structured-data
    custom_update_prefix: update_
    custom_merge_prefix: merge_
  vars:
    update_10_base:
      system:
        hostname: router1
        dns:
          - "192.0.2.1"
      vlan_ids:
        - 10
    merge_20_extra:
      system:
        dns:
          - "192.0.2.2"
      vlan_ids:
        - 20

# With no other matching variables, the resulting mapping contains:
#
# system:
#   hostname: router1
#   dns:
#     - "192.0.2.2"
#     - "192.0.2.1"
# vlan_ids:
#   - 20
#   - 10

- name: Use only the merge prefix
  controlware.utils.custom_structured_data:
    output_folder: /tmp/structured-data
    custom_merge_prefix: merge_
  vars:
    merge_10_base:
      enabled: true
"""

RETURN = r"""
path:
  description: Absolute path of the output file on the controller.
  returned: success
  type: str
  sample: /tmp/structured-data/router1.yml
processed_variables:
  description: Names of selected variables in processing order.
  returned: success
  type: list
  elements: str
  sample:
    - update_10_base
    - merge_20_extra
"""

# pylint: disable=wrong-import-position

from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec={
            "output_folder": {"type": "path", "required": True},
            "custom_update_prefix": {"type": "str"},
            "custom_merge_prefix": {"type": "str"},
        },
        required_one_of=[["custom_update_prefix", "custom_merge_prefix"]],
        supports_check_mode=True,
    )
    module.fail_json(
        msg=(
            "custom_structured_data requires its matching action plugin. "
            "Check the collection installation and use its fully qualified name."
        )
    )


if __name__ == "__main__":
    main()
