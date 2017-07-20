Ctrl architecture is explained in the below picture.

![Control Architecture Diagram](3-Developer-Guide/Control-Architecture.png)

Ctrl has following major components
1. CLI - CLI component accepts the commands from user and calls the callback functions in Commands component.
2. Commands - Commands component takes the appropriate sequence of actions for each command.
3. Configuration Manager - Configuration Manager is used to model the configuration of a cluster and to provide parameters that will be passed to the control component.
4. Ctrl_logger - Ctrl_logger is used for logging messages in the ctrl.
5. Power_control - Power_control component is responsible for power related commands. Currently this component can support on/off/reset commands for nodes.
6. Resource - Resource component is responsible for communication with resource manager.
7. BMC - BMC component is responsible for communication with BMC. For each new BMC that needs to be supported, a new BMC plugin has to be added.
8. PDU - PDU component is responsible for communication with PDU. For each new PDU that needs to be supported, a new PDU plugin has to be added.
9. OS_remote_access - OS remote access component provides SSH and Telnet plugins. These plugins will be useful to remotely login to a node/pdu and perform operations.
