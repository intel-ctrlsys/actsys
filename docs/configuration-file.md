Configuration file in Ctrl should be named as ctrl-config.json.

ctrl-config.json file can be located at following different locations in order of priority.
1. Current working directory
2. Home directory
3. /etc

This file is used to model the configuration of a cluster and to provide some parameters that will be passed to the control component.

For this purpose, a set of objects that can be used in this configuration file is described in this section.

## Common Rules.

__Identifiers__.

There are some objects in the configuration file that need a way to be identified from other objects, so three different ways to define an identifier are provided:

-  `device_id`. Can be any string that you want to use as an identifier. This has precedence over the other two described below.
-  `hostname`. This should be a string with a *valid hostname expression*. A *valid hostname expression* may contain only the ASCII letters 'a' through 'z' (in a case-insensitive manner), the digits '0' through '9' and the hyphen ('-'); it cannot start or end with a hyphen and no other symbols, punctuation characters, or white space are permitted. This attribute has precedence over the `ip_address`.
-  `ip_address`. This should be a string with a *valid IP address expression*. A *valid IP address expression* is a string which consists of four decimal numbers, each ranging from 0 to 255, separated by dots, e.g., 172.16.254.1.

Only one of these three is mandatory; so if you provide a `device_id`, that will be used as identifier for that object, even though you provide a `hostname` and/or an `ip_address` too. If you don't provide a `device_id` but you provide a `hostname`, that will be used as identifier; and finally if you don't provide a `device_id` nor a `hostname` then the `ip_address` will be used as identifier.

__Expansion Lists__.

Expansion lists are a compact way to define a list of strings, where those strings share a prefix and/or a suffix and contain consecutive, ascending, numerical values.

_Syntax_:
```
<prefix>[<length>:<first_index>-<last_index>]<suffix>
```
_Where_:
-	`<prefix>` is optional and could be any string.
-	`<length>` is the number of leading zeros (plus one) to be used. (e.g., 1, 01, 001). Note that ‘1’ represents no leading zeros to be used.
-	`<first_index>` is the lower value in an inclusive range: [first_index, last_index].
-	`<last_index>` is the upper value in an inclusive range: [first_index, last_index].
-	`<suffix>` is optional and could be any string.

_Examples_:
- `[2:0-2]world` expands to: ’00world’, ‘01world’ and ’02world’.
- `hello[2:0-2]` expands to: ’hello00’, ‘hello01’ and ’hello02’.
- `hello[3:5-6]world` expands to: ’hello005world’ and ‘hello006world’.
- `hello-world[1:1:1]` expands to: ‘hello-world1’.
- `hello-world[1:10:7]` is invalid.
- `hello-world[0:1:1]` is invalid.
- `[1:10:14]` expands to: ‘10’, ‘11’, ’12’, ’13’ and ‘14’.

Expansion lists can be used to define several objects with common attributes in a simple and short way.
They are supported in the following object attributes: `device_id`, `hostname`, `ip_address`, and `bmc` (for node objects only). Note that if an object is using expansion lists, then the length of the expanded string lists of the attributes mentioned above should match; otherwise the minimum length will be considered as the lists size and bigger lists will be cut to fix that size.
In addition, there is a special case where expansion lists can also be used. This is in the `device` attribute inside the `connected_device` objects in `pdu` or `psu` object types. There is no restriction about the length of these lists; they don’t need to match the length of any other list inside that `pdu` or `psu` object. For more information about `pdu` or `psu`, see the corresponding section below.
Example:
```json
{
    "pdu": [
        {
            "device_id": "mypdu",
            "connected_device": [
                {
                    "outlet": 4,
                    "device": [
                        "mydevice-[3:1-10]",
                        "192.168.1.[1:45-55]",
                        "otherdevice"
                    ]
                }
            ]
        }
    ]
}
```

## Configuration Variables.

This section is intended to hold some variables that will be used globally in the control component. In other words, all global configuration variables should be defined inside the `configuration_variables` object.
This object does not need to have a `device_id`, as it's unique in the configuration file.

Example:

```json
{
    "configuration_variables": {
        "my_global_variable": "This is a global value",
        "a_set_of_variables": {
            "var1": 4,
            "var2_list": [
                "mydevice-[3:1-10]",
                "192.168.1.[1:45-55]",
                "otherdevice"
            ]
        },
        "other_var": 32
    }
}
```

## Profiles.

Profiles are used to define __default__ values for a given object.
For example, let's say you want to define a set of objects that will share the same `user` and `password` attributes, so you can create a profile to be used by those objects.
```json
{
    "profile": [
        {
            "profile_name": "common_credentials",
            "user": "myuser",
            "password": "mypassword123"
        }
    ]
}
```
So, you can identify that profile by its `profile_name` attribute, which is __mandatory__ for each profile.
To use that profile in an object, you just need to add the `profile` attribute to that object with the `profile_name` that you want to use, like in the following example:
```json
{
    "node": [
        {
            "profile": "common_credentials",
            "hostname": "mynode1"
        },
        {
            "profile": "common_credentials",
            "user": "otheruser",
            "hostname": "mynode2"
        }
    ]
}
```
Note that in the example, there are two nodes that are using the default values from the profile defined above, but the second one **will override its user attribute** with the value set inside the object ("*otheruser*"). So both nodes will have an attribute `password` with a value of "mypassword123", but only the first node will have "myuser" as its `user` attribute.

## Node.

A cluster node, independent of the role that it has in the physical cluster, can be represented as a `node` object in the configuration file. Examples of nodes: login nodes, compute nodes, aggregator nodes, etc. All of them will be defined as `node` objects.

##### __Mandatory__ attributes for a `node` object:
- __Identifier__: Each node needs a way to be identified from other nodes, see the __'Common Rules'__ section above for more information about __Identifiers__.
    __Note__: If you don't provide a valid identifier, that object won't be added to the list of objects in the cluster model.

##### __Recommended__ attributes for a `node` object:
- `hostname`. This should be a string with a *valid hostname expression*. A *valid hostname expression* may contain only the ASCII letters 'a' through 'z' (in a case-insensitive manner), the digits '0' through '9' and the hyphen ('-'); it cannot start or end with a hyphen and no other symbols, punctuation characters, or white space are permitted. As explained above, the hostname can be optional if another way to identify the object is provided.
- `ip_address`. This should be a string with a *valid IP address expression*. A *valid IP address expression* is a string which consists of four decimal numbers, each ranging from 0 to 255, separated by dots, e.g., 172.16.254.1. As explained above, the ip_address can be optional if another way to identify the object is provided.
- `profile`. A string with the name of a profile to be used for this object.
- `mac_address`. A string representing the MAC Address of this object.
- `bmc`. A string with the identifier of a bmc object related with this node.
- `role`. A JSON list of strings with the roles that the node is being used for.
- `service_list`. A JSON list of strings with the services that can be used in that node.
- `image`. A string with image used by the provisioning software.
- `user`. A string with the username to be used for remote access operations.
- `password`. A string with the password to be used for remote access operations.
- `port`. An integer from 0 to 65535, for the port to be used for remote access operations.
- `access_type`. A string with the protocol to be used for remote access. Typical value: 'ssh'.
- `resource_controller`. A string with the software used for resource management.
- `os_shutdown_timeout_seconds`. An integer for the number of seconds for the timeout of shutdown operations.
- `os_boot_timeout_seconds`. An integer for the number of seconds for the timeout of boot operations.
- `os_network_to_halt_time`. An integer for the max timeout to wait for the chassis to be off after the remote network services are gone (i.e. ping no longer works) in seconds.  This period is where a likely driver hang could occur.
- `wait_time_after_boot_services`. When booting the OS this is the wait time, in seconds, for stabilizing the post network services before the OS is actually booted fully.
- `bmc_boot_timeout_seconds`. An integer with the number of seconds for a sleep time after the chassis is on before the BMC will respond again to requests.
- `bmc_chassis_off_wait`. An integer with the number of seconds for a sleep time after the chassis is turned off before the BMC will respond again to requests.

Example:

```json
{
    "node": [
        {
            "hostname": "myhostname",
            "ip_address": "192.168.1.100",
            "mac_address": "a3:44:30:f9:b2:87",
            "bmc": "mybmc",
            "user": "myuser",
            "password": "password123",
            "port": 2020,
            "access_type": "ssh",
            "resource_controller": "slurm",
            "image": "RHEL_6.0_Jun23",
            "service_list": [
                "someservice"
            ],
            "role": [
                "compute"
            ],
            "os_shutdown_timeout_seconds": 10,
            "os_boot_timeout_seconds": 15,
            "os_network_to_halt_time": 20,
            "wait_time_after_boot_services": 13,
            "bmc_boot_timeout_seconds": 10,
            "bmc_chassis_off_wait": 3
        },
        {
            "profile": "mynodeprofile",
            "ip_address": "192.168.45.[1:10-30]",
            "bmc": "192.168.45.[1:50-80]"
        }
    ],
    "profile": [
        {
            "profile_name": "mynodeprofile",
            "user": "admin",
            "password": "admin123",
            "port": 2020,
            "access_type": "ssh",
            "resource_controller": "slurm",
            "image": "SLES12",
            "service_list": [
                "someservice",
                "otherservice"
            ],
            "role": [
                "aggregator",
                "login"
            ],
            "os_shutdown_timeout_seconds": 101,
            "os_boot_timeout_seconds": 151,
            "os_network_to_halt_time": 201,
            "wait_time_after_boot_services": 131,
            "bmc_boot_timeout_seconds":101,
            "bmc_chassis_off_wait": 31
        }
    ]
}
```

## BMC.

To represent a BMC (Baseboard Management Controller) object in the configuration file you can use the `bmc` keyword.

##### __Mandatory__ attributes for a `bmc` object:
- __Identifier__: Each bmc needs a way to be identified from other bmcs, see the __'Common Rules'__ section above for more information about __Identifiers__.
    __Note__: If you don't provide a valid identifier, that object won't be added to the list of objects in the cluster model.

##### __Recommended__ attributes for a `bmc` object:
- `hostname`. This should be a string with a *valid hostname expression*. A *valid hostname expression* may contain only the ASCII letters 'a' through 'z' (in a case-insensitive manner), the digits '0' through '9' and the hyphen ('-'); it cannot start or end with a hyphen and no other symbols, punctuation characters, or white space are permitted. As explained above, the hostname can be optional if another way to identify the object is provided.
- `ip_address`. This should be a string with a *valid IP address expression*. A *valid IP address expression* is a string which consists of four decimal numbers, each ranging from 0 to 255, separated by dots, e.g., 172.16.254.1. As explained above, the ip_address can be optional if another way to identify the object is provided.
- `profile`. A string with the name of a profile to be used for this object.
- `mac_address`. A string representing the MAC Address of this object.
- `user`. A string with the username to be used for remote access operations.
- `password`. A string with the password to be used for remote access operations.
- `port`. An integer from 0 to 65535, for the port to be used for remote access operations.
- `access_type`. A string with the protocol to be used for remote access. Typical value: 'ipmi_util'.
- `channel`. An integer from 0 to 15, for the IPMI channel to be used.
- `priv_level`. A string with the privilege level used for IPMI operations. Options are: 'CALLBACK', 'USER', 'OPERATOR' or 'ADMINISTRATOR'.
- `auth_method`. A string with the authentication method used for IPMI operations. Options are: 'NONE', 'PASSWORD', 'MD2', 'MD5' or 'OEM'.

Example:

```json
{
    "bmc": [
        {
            "hostname": "mybmc",
            "ip_address": "192.168.2.100",
            "mac_address": "e3:44:80:f9:72:89",
            "user": "myuser",
            "password": "password123",
            "port": 2020,
            "access_type": "ipmi_util",
            "channel": 1,
            "priv_level": "USER",
            "auth_method": "PASSWORD"
        },
        {
            "profile": "mybmcprofile",
            "ip_address": "192.168.45.[1:50-80]",
        }
    ],
    "profile": [
        {
            "profile_name": "mybmcprofile",
            "user": "admin",
            "password": "admin123",
            "port": 2020,
            "access_type": "ipmi_util",
            "channel": 0,
            "priv_level": "ADMINISTRATOR",
            "auth_method": "PASSWORD"
        }
    ]
}
```

## PSU.

To represent a PSU (Power Supply Unit) object in the configuration file you can use the `psu` keyword.

##### __Mandatory__ attributes for a `psu` object:
- __Identifier__: Each psu needs a way to be identified from other psus, see the __'Common Rules'__ section above for more information about __Identifiers__.
    __Note__: If you don't provide a valid identifier, that object won't be added to the list of objects in the cluster model.

##### __Recommended__ attributes for a `psu` object:
- `hostname`. This should be a string with a *valid hostname expression*. A *valid hostname expression* may contain only the ASCII letters 'a' through 'z' (in a case-insensitive manner), the digits '0' through '9' and the hyphen ('-'); it cannot start or end with a hyphen and no other symbols, punctuation characters, or white space are permitted. As explained above, the hostname can be optional if another way to identify the object is provided.
- `ip_address`. This should be a string with a *valid IP address expression*. A *valid IP address expression* is a string which consists of four decimal numbers, each ranging from 0 to 255, separated by dots, e.g., 172.16.254.1. As explained above, the ip_address can be optional if another way to identify the object is provided.
- `profile`. A string with the name of a profile to be used for this object.
- `mac_address`. A string representing the MAC Address of this object.
- `user`. A string with the username to be used for remote access operations.
- `password`. A string with the password to be used for remote access operations.
- `port`. An integer from 0 to 65535, for the port to be used for remote access operations.
- `access_type`. A string with the protocol to be used for remote access. Typical value: 'ipmi_util'.
- `outlets_count`. An integer representing the number of power outlets available in the object.
- `connected_device`: A JSON list of objects representing the connections between power outlets and devices. There will be an object for each power outlet that has a connection in place, and several devices can be connected to the same outlet. To specify the devices connected to each outlet the device identifier must be used.
    - `outlet`. A string representing the identifier for a given power outlet in the object.
    - `device`. A JSON list of strings with the identifiers of the devices connected to that power outlet.
    - `connected_device` example:
        ```json
        {
            "connected_device": [
                {
                    "outlet": "3",
                    "device": [
                        "myhostname",
                        "192.168.45.[1:10-12]"
                    ]
                },
                {
                    "outlet": "5",
                    "device": [
                        "192.168.45.30"
                    ]
                }
            ]
        }
        ```

PSU Example:

```json
{
    "psu": [
        {
            "hostname": "mypsu",
            "ip_address": "192.168.1.240",
            "mac_address": "78:45:b2:9f:13:a5",
            "user": "myuser",
            "password": "password123",
            "port": 2020,
            "access_type": "ipmi_util",
            "outlets_count": 2,
            "connected_device": [
                {
                    "outlet": "0",
                    "device": [
                        "myhostname",
                        "192.168.45.[1:10-12]"
                    ]
                },
                {
                    "outlet": "1",
                    "device": [
                        "192.168.45.30"
                    ]
                }
            ]
        },
        {
            "profile": "mypsu_profile",
            "hostname": "psu-[1:242-243]",
            "ip_address": "192.168.45.[1:242-243]",
            "connected_device": [
                {
                    "outlet": "0",
                    "device": [
                        "192.168.45.13"
                    ]
                },
                {
                    "outlet": "1",
                    "device": [
                        "192.168.45.14"
                    ]
                },
                {
                    "outlet": "2",
                    "device": [
                        "192.168.45.15"
                    ]
                },
                {
                    "outlet": "3",
                    "device": [
                        "192.168.45.16"
                    ]
                }
            ]
        }
    ],
    "profile": [
        {
            "profile_name": "mypsu_profile",
            "user": "admin",
            "password": "admin123",
            "port": 2020,
            "access_type": "impi_util",
            "outlets_count": 4
        }
    ]
}
```

## PDU.

To represent a PDU (Power Distribution Unit) object in the configuration file you can use the `pdu` keyword.

##### __Mandatory__ attributes for a `pdu` object:
- __Identifier__: Each pdu needs a way to be identified from other pdus, see the __'Common Rules'__ section above for more information about __Identifiers__.
    __Note__: If you don't provide a valid identifier, that object won't be added to the list of objects in the cluster model.

##### __Recommended__ attributes for a `pdu` object:
- `hostname`. This should be a string with a *valid hostname expression*. A *valid hostname expression* may contain only the ASCII letters 'a' through 'z' (in a case-insensitive manner), the digits '0' through '9' and the hyphen ('-'); it cannot start or end with a hyphen and no other symbols, punctuation characters, or white space are permitted. As explained above, the hostname can be optional if another way to identify the object is provided.
- `ip_address`. This should be a string with a *valid IP address expression*. A *valid IP address expression* is a string which consists of four decimal numbers, each ranging from 0 to 255, separated by dots, e.g., 172.16.254.1. As explained above, the ip_address can be optional if another way to identify the object is provided.
- `profile`. A string with the name of a profile to be used for this object.
- `mac_address`. A string representing the MAC Address of this object.
- `user`. A string with the username to be used for remote access operations.
- `password`. A string with the password to be used for remote access operations.
- `access_type`. A string with the PDU model. The current supported models are 'Raritan_PX3-5180CR' and 'IPS400'
- `outlets_count`. An integer representing the number of power outlets available in the object.
- `connected_device`: A JSON list of objects representing the connections between power outlets and devices. There will be an object for each power outlet that has a connection in place, and several devices can be connected to the same outlet. To specify the devices connected to each outlet the device identifier must be used.
    - `outlet`. A string representing the identifier for a given power outlet in the object.
    - `device`. A JSON list of strings with the identifiers of the devices connected to that power outlet.
    - `connected_device` example:
        ```json
        {
            "connected_device": [
                {
                    "outlet": "3",
                    "device": [
                        "mypsu",
                        "192.168.45.[1:20-22]"
                    ]
                },
                {
                    "outlet": "5",
                    "device": [
                        "psu-242",
                        "psu-243"
                    ]
                }
            ]
        }
        ```

PDU Example:

```json
{
    "pdu": [
        {
            "hostname": "mypdu",
            "ip_address": "192.168.1.200",
            "mac_address": "3a:45:03:9f:b2:78",
            "user": "myuser",
            "password": "password123",
            "access_type": "Raritan_PX3-5180CR",
            "outlets_count": 6,
            "connected_device": [
                {
                    "outlet": "3",
                    "device": [
                        "mypsu",
                        "192.168.45.[1:20-22]"
                    ]
                },
                {
                    "outlet": "5",
                    "device": [
                        "psu-242",
                        "psu-243",
                    ]
                }
            ]
        },
        {
            "profile": "mypdu_profile",
            "hostname": "pdu-[1:210-213]",
            "ip_address": "192.168.45.[1:210-213]",
            "connected_device": [
                {
                    "outlet": "0",
                    "device": [
                        "192.168.45.[1:23-26]"
                    ]
                },
                {
                    "outlet": "1",
                    "device": [
                        "192.168.45.[1:27-30]"
                    ]
                }
            ]
        }
    ],
    "profile": [
        {
            "profile_name": "mypdu_profile",
            "user": "admin",
            "password": "admin123",
            "access_type": "IPS400",
            "outlets_count": 8
        }
    ]
}
```

