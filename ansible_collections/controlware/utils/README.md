# Ansible Collection - controlware.utils

## Filter

- [cs_int_ranges](#cs_int_ranges)
- [default](#default)
- [ipsort](#ipsort)
- [ipv4_range](#ipv4_range)
- [sort_cs_int_ranges](#sort_cs_int_ranges)
- [sort_interface_names](#sort_interface_names)

### cs_int_ranges

This filter builds a list of comma-separated integer range list strings from
any given informationen containing integers or integer ranges.

#### cs_int_ranges Input Parameters

<table border=1 cellpadding=4>

<tr>
<th class="head">parameter</th>
<th class="head">type</th>
<th class="head">required</th>
<th class="head">default</th>
<th class="head">choices</th>
<th class="head">comments</th>
</tr>

<tr>
<td>values<br/><div style="font-size: small;"></div></td>
<td>list[str] | list[int] | str | dict</td>
<td>yes</td>
<td></td>
<td></td>
<td>
    <div>Element(s) containing integer information</div>
</td>
</tr>

<tr>
<td>max_int<br/><div style="font-size: small;"></div></td>
<td>int</td>
<td>false</td>
<td>0</td>
<td></td>
<td>
    <div>Maximum allowed integer value</div>
</td>
</tr>

<tr>
<td>max_length<br/><div style="font-size: small;"></div></td>
<td>int</td>
<td>false</td>
<td>0</td>
<td></td>
<td>
    <div>Maximum length of first returned string containing
    comma-separated integer ranges.</br>
    Must be 0 (infinite) or greater than 10.</div>
</td>
</tr>

<tr>
<td>max_length_next<br/><div style="font-size: small;"></div></td>
<td>int</td>
<td>false</td>
<td>None</td>
<td></td>
<td>
    <div>Maximum length of second and continueing returned strings containing
    comma-separated integer ranges.</br>
    Must be greater than 10.</div>
</td>
</tr>

<tr>
<td>dual_int_ranges<br/><div style="font-size: small;"></div></td>
<td>bool</td>
<td>false</td>
<td>True</td>
<td></td>
<td>
    <div>Select parsing mode of a range of two values.
    I.E. select between "10-11" (dual_int_range) and "10,11".</div>
</td>
</tr>

</table>
</br>

#### cs_int_ranges Returns

````yaml
- <comma-separated integer range string>
````

### default

This filter tests and return the given value if defined and not None.
Otherwise check given other values and returns first defined and not None.

#### default Input Parameters

<table border=1 cellpadding=4>

<tr>
<th class="head">parameter</th>
<th class="head">type</th>
<th class="head">required</th>
<th class="head">default</th>
<th class="head">choices</th>
<th class="head">comments</th>
</tr>

<tr>
<td>value<br/><div style="font-size: small;"></div></td>
<td>any</td>
<td>yes</td>
<td></td>
<td></td>
<td>
    <div>Data to check</div>
</td>
</tr>

<tr>
<td>default_values<br/><div style="font-size: small;"></div></td>
<td>any</td>
<td>yes</td>
<td></td>
<td></td>
<td>
    <div>Single value or list of values to check as default values</div>
</td>
</tr>

</table>
</br>

#### default Returns

value or first non-None default_value

### ipsort

This filter sorts a given list of IP address xor IP networks.

#### ipsort Input Parameters

<table border=1 cellpadding=4>

<tr>
<th class="head">parameter</th>
<th class="head">type</th>
<th class="head">required</th>
<th class="head">default</th>
<th class="head">choices</th>
<th class="head">comments</th>
</tr>

<tr>
<td>ip_strings<br/><div style="font-size: small;"></div></td>
<td>list[str]</td>
<td>yes</td>
<td></td>
<td></td>
<td>
    <div>List of strings representing IPv4 addresses xor networks</div>
</td>
</tr>

<tr>
<td>reverse<br/><div style="font-size: small;"></div></td>
<td>bool</td>
<td>no</td>
<td>False</td>
<td></td>
<td>
    <div>Invert sorting order</div>
</td>
</tr>

</table>
</br>

#### ipsort Returns

```yaml
- < IPv4 Address xor Network String >
```

### ipv4_range

This filter returns a list of all host addresses between
*start* and *end* address.

#### ipv4_range Input Parameters

<table border=1 cellpadding=4>

<tr>
<th class="head">parameter</th>
<th class="head">type</th>
<th class="head">required</th>
<th class="head">default</th>
<th class="head">choices</th>
<th class="head">comments</th>
</tr>

<tr>
<td>start<br/><div style="font-size: small;"></div></td>
<td>str</td>
<td>yes</td>
<td></td>
<td></td>
<td>
    <div>String representing the starting IPv4 address</div>
</td>
</tr>

<tr>
<td>end<br/><div style="font-size: small;"></div></td>
<td>str</td>
<td>yes</td>
<td></td>
<td></td>
<td>
    <div>String representing the ending IPv4 address</div>
</td>
</tr>

</table>
</br>

#### ipv4_range Returns

```yaml
- < IPv4 Address String >
```

### sort_cs_int_ranges

This filter sorts comma-separated integer range strings by sorting
first integer value in each string.

#### sort_cs_int_ranges Input Parameters

<table border=1 cellpadding=4>

<tr>
<th class="head">parameter</th>
<th class="head">type</th>
<th class="head">required</th>
<th class="head">default</th>
<th class="head">choices</th>
<th class="head">comments</th>
</tr>

<tr>
<td>ranges_list<br/><div style="font-size: small;"></div></td>
<td>list[str]</td>
<td>yes</td>
<td></td>
<td></td>
<td>
    <div>List of comma-separated integer range strings</div>
</td>
</tr>

</table>
</br>

#### sort_cs_int_ranges Returns

```yaml
- < comma-separated integer range string >
```

### sort_interface_names

This filter sorts a list of given interface names with respect to
given vendor and plattform.

#### sort_interface_names Input Parameters

<table border=1 cellpadding=4>

<tr>
<th class="head">parameter</th>
<th class="head">type</th>
<th class="head">required</th>
<th class="head">default</th>
<th class="head">choices</th>
<th class="head">comments</th>
</tr>

<tr>
<td>interfaces<br/><div style="font-size: small;"></div></td>
<td>list[str]</td>
<td>yes</td>
<td></td>
<td></td>
<td>
    <div>List of interface name strings</div>
</td>
</tr>

<tr>
<td>vendor<br/><div style="font-size: small;"></div></td>
<td>str</td>
<td>yes</td>
<td></td>
<td>cisco</td>
<td>
    <div>Vendor name (case-insensitive)</div>
</td>
</tr>

<tr>
<td>platform<br/><div style="font-size: small;"></div></td>
<td>str</td>
<td>yes</td>
<td></td>
<td>[ios, iosxe, ios-xe, nexus, nxos, nx-os]</td>
<td>
    <div>Platform name (case-insensitive)</div>
</td>
</tr>

</table>
</br>

#### sort_interface_names Returns

```yaml
- < interface name string >
```
