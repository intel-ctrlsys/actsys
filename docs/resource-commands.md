## 2.5 Resource Commands
To get the help menu of resource commands, use the "./ctrl resource --help" command.
```

usage: ctrl resource [-h] {add,remove,check} device_name

positional arguments:
  {add,remove,check}  Select one of the following options: add/remove/check
                      Ex: ctrl resource add node001
  device_name         compute nodes for which command will be executed.

```
For these resource commands to work, the cluster must already have a resource manager running. Also, the local configuration file must specify the resource manager (e.g. SLURM) that is running in the "resource_controller" field.
The "device_name" could include multiple compute nodes that are represented as comma separated list (e.g. c01,c03,c07), regex (c[01-10]), logical group name (@g1), or a comma separated mix of all these.
All the commands will print the output in a compact way that groups the nodes having the same states and results with node regex.


```bash
# ctrl resource remove device_name
```
This command will remove a list of idle compute nodes from the cluster resource pool. If the compute nodes are running jobs, or have already been removed from the resource pool, or in other states (e.g. down, unknown), the command will return user proper messages.

Below is an example of using this command:

```
# ctrl resource remove compute-[29-32]
```
The result will be as follows:

```
NODELIST         RESULT
compute-[29-30]  Had already been removed!
compute-[31-32]  Succeeded in removing!
```

```bash
# ctrl resource add device_name
```
This command will add a list of compute nodes (were removed before) back to the cluster resource pool. If the compute nodes are in the resource pool, or in other states, the command will return user proper message:

Below is an example of using this command:

```
# ctrl resource add compute-[29-32]
```
The result will be as follows:

```
NODELIST         RESULT
compute-[29-30]  Succeeded in adding!
compute-31       In down state, cannot be added!
compute-32       Already in the cluster resource pool!
```

```bash
# ctrl resource check device_name
```
This command will check the states of a list of compute nodes in the cluster resource pool.

Below is an example of using this command:

```
# ctrl resource check compute-[29-32]
```
The result will be as follows:

```
NODELIST         STATE
compute-[29-30]  idle
compute-31       drain
compute-32       alloc
```
