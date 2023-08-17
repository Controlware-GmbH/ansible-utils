===============================
Controlware.Utils Release Notes
===============================

.. contents:: Topics


v1.0.3
======

Bugfixes
--------

- #14 Filter cs_int_ranges: dual_int_ranges==false does not respect last two values

v1.0.2
======

Minor Changes
-------------

- #12 Filter cs_int_ranges: Add switch 'dual_int_ranges'

v1.0.1
======

Minor Changes
-------------

- #10 Filter ipsort - Support IP interfaces (address/prefix)

v1.0.0
======

New Plugins
-----------

Filter
~~~~~~

- controlware.utils.cs_int_ranges - This filter builds a list of comma-separated integer range list strings from any given informationen containing integers or integer ranges.
- controlware.utils.default - This filter tests and return the given value if defined and not None. Otherwise check given other values and returns first defined and not None.
- controlware.utils.ipsort - This filter sorts a given list of IP address xor IP networks.
- controlware.utils.ipv4_range - This filter returns a list of all host addresses between start and end address.
- controlware.utils.sort_cs_int_ranges - This filter sorts comma-separated integer range strings by sorting first integer value in each string.
- controlware.utils.sort_interface_names - This filter sorts a list of given interface names with respect to given vendor and plattform.
