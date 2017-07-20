## 1 Overview
Ctrl is a tool that can be used to perform several useful operations in the cluster.

Currently Ctrl can be used to perform the following commands.

    1. Power on/off/reset a compute node, service node or a pdu outlet
    2. Add/Remove/Check a compute node from a resource pool.
    3. Check/start/stop services specified in the configuration file for a compute node and service node.
    4. Flash new bios or get current bios for a compute node
    5. Use a provisioner to add/delete/set a device to a provisioner (i.e. warewulf).
    6. Reading the OOB sensors on a compute node.
    7. Run diagnostic tests on a compute node.

Detailed information about how to use Ctrl and each respective command is provided in the user guide.

__Note:__ For ease of use, enabling port forwarding with ssh is suggested. However, it is highly recommended that users assess their specific security related situations to determine if using port forwarding is acceptable.
