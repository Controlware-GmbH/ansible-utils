#!/usr/bin/env python
#
# Example:
#
#   - name: Write structured data
#     custom_structured_data:
#       output_folder: ./structured_data
#       custom_merge_prefix: sd_merge_
#
# custom_update_prefix and custom_merge_prefix are optional individually,
# but at least one must be supplied. Files are written on the controller as
# <inventory_hostname>.yml.
#
# Matches are sorted together by suffix, then by full name for ties. For
# overlapping prefixes, the longer prefix wins. Identical prefixes are
# rejected. Update is shallow; merge recursively combines mappings and
# prepends incoming lists without removing duplicates.
#
# Check mode does not write files. Use no_log: true if data contains secrets.

import os
import stat
import tempfile
from collections.abc import Mapping

from ansible.plugins.action import ActionBase
from ansible.plugins.filter.core import to_nice_yaml


def merge_mappings(existing, incoming):
    """Return a recursive merge without modifying either input."""
    result = dict(existing)

    for key, new_value in incoming.items():
        if key not in result:
            result[key] = new_value
            continue

        old_value = result[key]
        if isinstance(old_value, Mapping) and isinstance(new_value, Mapping):
            result[key] = merge_mappings(old_value, new_value)
        elif isinstance(old_value, list) and isinstance(new_value, list):
            result[key] = list(new_value) + list(old_value)
        else:
            result[key] = new_value

    return result


def select_variables(task_vars, update_prefix, merge_prefix):
    """Select matches once and sort them by suffix, then full name."""
    selected = []

    for name in task_vars:
        if not isinstance(name, str):
            continue

        matches = []
        if update_prefix is not None and name.startswith(update_prefix):
            matches.append((update_prefix, "update"))
        if merge_prefix is not None and name.startswith(merge_prefix):
            matches.append((merge_prefix, "merge"))

        if matches:
            prefix, operation = max(matches, key=lambda item: len(item[0]))
            selected.append((name[len(prefix) :], name, operation))

    return sorted(selected, key=lambda item: (item[0], item[1]))


def existing_content(path):
    """Read a regular file, or return None if it does not exist."""
    try:
        file_stat = os.lstat(path)
    except FileNotFoundError:
        return None

    if not stat.S_ISREG(file_stat.st_mode):
        raise ValueError(f"Output path exists but is not a regular file: {path}")

    with open(path, "rb") as existing_file:
        return existing_file.read()


def atomic_write(path, content):
    """Replace path using a temporary file in the same directory."""
    directory = os.path.dirname(path)
    os.makedirs(directory, mode=0o700, exist_ok=True)

    fd, temporary_path = tempfile.mkstemp(
        prefix=".custom_structured_data-",
        suffix=".tmp",
        dir=directory,
    )
    try:
        with os.fdopen(fd, "wb") as temporary_file:
            temporary_file.write(content)
        os.replace(temporary_path, path)
    finally:
        try:
            os.unlink(temporary_path)
        except FileNotFoundError:
            pass


class ActionModule(ActionBase):
    # pylint: disable=too-few-public-methods
    TRANSFERS_FILES = False
    _requires_connection = False
    _supports_check_mode = True

    def run(self, tmp=None, task_vars=None):
        # pylint: disable=too-many-locals,too-many-statements,too-many-branches
        task_vars = task_vars or {}
        result = super().run(tmp=tmp, task_vars=task_vars)
        result["changed"] = False

        try:
            args = self._task.args
            allowed = {
                "output_folder",
                "custom_update_prefix",
                "custom_merge_prefix",
            }

            unknown = set(args) - allowed
            if unknown:
                raise ValueError(f"Unknown arguments: {', '.join(sorted(unknown))}")

            if "output_folder" not in args:
                raise ValueError("Missing required argument: output_folder")

            prefix_names = ("custom_update_prefix", "custom_merge_prefix")
            if not any(name in args for name in prefix_names):
                raise ValueError(
                    "At least one of custom_update_prefix or "
                    "custom_merge_prefix must be supplied"
                )

            for name in ("output_folder",) + prefix_names:
                if name in args and (not isinstance(args[name], str) or not args[name]):
                    raise ValueError(f"{name} must be a non-empty string")

            update_prefix = args.get("custom_update_prefix")
            merge_prefix = args.get("custom_merge_prefix")
            if update_prefix is not None and update_prefix == merge_prefix:
                raise ValueError("The update and merge prefixes must differ")

            hostname = task_vars.get("inventory_hostname")
            if (
                not isinstance(hostname, str)
                or not hostname
                or hostname in (".", "..")
                or any(character in hostname for character in ("/", "\\", "\0"))
            ):
                raise ValueError("inventory_hostname must be a safe filename component")

            output_folder = os.path.abspath(os.path.expanduser(args["output_folder"]))
            output_path = os.path.join(output_folder, hostname + ".yml")

            selected = select_variables(task_vars, update_prefix, merge_prefix)
            working = {}

            for item in selected:
                name, operation = item[1], item[2]
                value = self._templar.template(task_vars[name], fail_on_undefined=True)
                if not isinstance(value, Mapping):
                    raise ValueError(f"Variable {name!r} must contain a mapping")

                if operation == "update":
                    working.update(value)
                else:
                    working = merge_mappings(working, value)

            yaml_text = to_nice_yaml(
                working,
                indent=2,
                sort_keys=False,
                width=100,
            )
            content = yaml_text.encode("utf-8")
            previous = existing_content(output_path)

            result["path"] = output_path
            result["processed_variables"] = [item[1] for item in selected]

            if previous == content:
                return result

            check_mode = self._task.check_mode
            if check_mode is None:
                check_mode = self._play_context.check_mode

            if not check_mode:
                atomic_write(output_path, content)

            result["changed"] = True
            return result

        except Exception as exc:  # pylint: disable=broad-exception-caught
            result["failed"] = True
            result["msg"] = f"custom_structured_data: {exc}"
            return result
