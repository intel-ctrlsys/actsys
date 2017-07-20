## 2.4 Power Commands
To get the help menu of power commands, use the "./ctrl power --help" command.
```

usage: ctrl power [-h] [-f] [-o [OUTLET]]
                  {on,off,cycle,bios,efi,hdd,pxe,cdrom,removable} device_name

positional arguments:
  {on,off,cycle,bios,efi,hdd,pxe,cdrom,removable}
                        Select an option:
                        on/off/cycle/bios/efi/hdd/pxe/cdrom/removable. Ex:
                        ctrl power on node001
  device_name           Device where command will be executed.

optional arguments:
  -h, --help            show this help message and exit
  -f, --force           This option will allow user to force the Power
                        On/Off/Reboot
  -o [OUTLET], --outlet [OUTLET]
                        Specify the outlet to edit (PDUs only)

```
For these power commands to work the local host account must have access to the remote system as root (not just some root privileges) for the graceful remote OS shutdown. Also, the local configuration file must contain the credentials to access the BMC correctly.

__Note:__ All nodes in the `nodelist` are attempted in a serial order.  Failures are reported but do not stop the next node attempt.
```bash
# ctrl power on [--force] <nodelist>
```
This command will power on a node from off.  If there are associated PDUs that are off they will be turned on before the node is attempted to power on to the default boot device.  If the node is already on this will fail and suggest you use the power cycle command.
```bash
# ctrl power off [--force] <nodelist>
```
This command will turn off each node in the `nodelist` if not already off.  It will attempt a graceful shutdown and if that cannot be accomplished in the given timeout period then if `--force` is not present a failure is reported.  IF the `--force` option is present the node will be forced off.
```bash
# ctrl power cycle [--force] <nodelist>
```
This command will power cycle nodes that are already in an chassis on state to another state of the same state.  If the node is off, then this will fail suggesting the user use the `power on` command.

These commands control power on a node (service nodes, compute nodes, or other nodes) using a combination of OS access (like ssh) and the BMC for the chassis.  The `--force` options has the following affect and should not be used unless dangers of a hard shutdown are negated using different methods:
#### The `--force` Option
Using this option will force the OS shutdown if the system has not shutdown and the OS shutdown timer has expired. The BMC is used to remove power completely (i.e. hard off without finishing a OS shutdown).  The possible dangers are as follows:

1. Any local HDD partitions may not by unmounted properly causing corruption.
2. Any remotely mounted volumes may not be unmounted properly causing corruption or simple loss of data.
3. Any queued network or fabric messages that have not been sent will be lost.

__Note:__ It is highly recommended that users assess the dangers of their specific situations to determine if using `--force` is acceptable or if the options should be completely ignored.

For PDU power commands to work, the configuration file must contain credentials to required to access the PDU. If the PDU cannot be managed or controlled remotely, the PDU configuration should be omitted from the configuration file.

```bash
# ctrl power on -o <n> <pdu>
```
This command will power on outlet n on the specified pdu if not already on.
```bash
# ctrl power off -o <n> <pdu>
```
This command will power off outlet n on the specified pdu if it is on.

__Note:__User must assess the situation of the nodes/psus/other pdus connected to the pdu outlets before using the power off command.
