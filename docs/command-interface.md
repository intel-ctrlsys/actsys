## 2.3 Command Line Interface
To get the help menu of Ctrl, use the "./ctrl --help" command.
```
usage: ctrl [-h] [-V] [-v] [-t TIMEOUT]

            {power,resource,process,get,set,service,datastore,provision,bios,sensor}
            ...

Control Component Parser

optional arguments:
  -h, --help            show this help message and exit
  -i, --interactive     Start interactive session
  -V, --version         Provides the version of the tool
  -v, --verbosity       increase output verbosity
  -t TIMEOUT, --timeout TIMEOUT
                        Provides a timeout for the command

Sub Commands:
  List of Valid Sub Commands

  {power,resource,process,get,set,service,datastore,provision,diag,bios,sensor}
    power               Power on/off/reset a device.
    resource            Resource add/remove from a resource pool.
    process             Process list/kill on a node in a cluster.
    get                 Get powercap/freq value of a node.
    set                 Set powercap/freq value of a node.
    service             Check, start or stop services specified in the
                        configuration file
    datastore           Device and configuration manipulations
    provision           Adding, setting and removing provisioning options for
                        devices
    bios                Update or get version of bios on specified nodes/group
                        of nodes
    sensor              Get specified sensor value on specified nodes/group of
                        nodes

```
Ctrl supports several subcommands. The list of valid sub commands is provided in "./ctrl --help" command
Each subcommand has its own help menu on how to use the subcommand.
To get the help menu of a specific subcommand, use "./ctrl {subcommand} --help" command.

##2.3.1 Interactive Commands
The interactive cli features the following commands in addition the Ctrl commands.

Interactive Commands:

  {select, clear_select}
    select              Set node/regex context for command execution
    clear_select        Remove context.
    %help               Display command help

