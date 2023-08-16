# Ansible Collection - controlware.utils

## Filters

Provided ansible and Jinja2 filters:

- **cs_int_ranges**:
  - Description: Builds a list of comma-separated integer range list strings
    from any given informationen containing integers or integer ranges.
  - Parameters:
    - values:
      - Type: list[str] | list[int] | str | dict
      - Description: Element(s) containing integer information
      - Required: Yes
    - max_int:
      - Type: integer
      - Description: Maximal allowed interger values
      - Required: False
      - Default: 0
    - max_length:
      - Type: integer
      - Description: Maximum length of returned string containing
        comma-separated integer ranges
      - Required: False
      - Restrictions: >= 11
    - max_length_next:
      - Type: integer
      - Description: Maximum length of second and continueing strings
        containing comma-separated integer ranges
      - Required: False
      - Restrictions: >= 11
    - dual_int_ranges:
      - Type: bool
      - Description: Select between 10-11 (dual_int_range) and 10,11
      - Required: False
      - Default: True
  - Returns:
    - Type: list(str)
    - Description: List of comma-separated integer range strings
- **default**:
  - Description: Resturns given value, if defined and not None.
    Otherwise check given default values and returns first defined and
    not None.
  - Parameters:
    - value:
      - Type: any
      - Description: Data to check
      - Required: Yes
    - default_values:
      - Type: any
      - Description: Single value or list of values to check
      - Required: False
      - Default: 0
  - Returns:
    - Type: any
    - Description: Value of 'value' or value of a 'default_value' or None
- **ipv4_range**:
  - Description: Returns a list of all host addresses between
    'start' and 'end' address
  - Parameters:
    - start:
      - Type: str (representing an IPv4 address)
      - Description: Starting IPv4 address
      - Required: No
      - Default: '0.0.0.0'
    - end:
      - Type: str [representing an IPv4 address]
      - Description: Ending IPv4 address
      - Required: No
      - Default: '0.0.0.0'
  - Returns:
    - Type: list(str)
    - Description: List of strings representing IPv4 addresses within the range
- **ipsort**:
  - Description: Sort a given list of IP address xor IP networks.
  - Parameters:
    - ip_strings:
      - Type: list(str) [representing IP addresses xor IP networks]
      - Description: IP elements to sort
      - Required: Yes
    - reverse:
      - Type: bool
      - Description: Invert sorting
      - Required: No
      - Default: False
  - Returns:
    - Type: list(str) [representing IP addresses xor IP networks]
    - Description: Sorted list of strings representing IP addresses xor
      IP networks
- **sort_cs_int_ranges**:
  - Description: Sort comma-separated integer range strings by sorting
    first integer value in each string.
  - Parameters:
    - ranges_list:
      - Type: list(str) [comma-separated integer range strings]
      - Description: List to sort
      - Required: Yes
  - Returns:
    - Type: list(str) [comma-separated integer range strings]
    - Description: Sorted list of comma-separated integer range strings
- **sort_interface_names**:
  - Description: Sort a list of given interface names with respect to
    given vendor and plattform.
  - Parameters:
    - interfaces:
      - Type: list(str) [interface names]
      - Description: List to sort
      - Required: Yes
    - vendor:
      - Type: str
      - Description: Vendor Name
      - Required: Yes
      - Restrictions: Allowed values are 'cisco'
      - Remarks: Ignores upper-cases
    - platform:
      - Type: str
      - Description: Platform Name
      - Required: Yes
      - Restrictions: Allowed values are 'ios', 'iosxe', 'ios-xe',
        'nexus', 'nxos' and 'nx-os'
      - Remarks: Ignores upper-cases
  - Returns:
    - Type: list(str) [interface names]
    - Description: Sorted list of interface names
