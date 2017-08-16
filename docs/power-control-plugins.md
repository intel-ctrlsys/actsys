The node power control features are controlled by 2 plugin types or frameworks:
1. BMC Remote Access; default is a plugin using the `ipmiutil` command line tool.
2. OS Remote Execution; default is passwordless ssh to the __root__ account on the remote OS to execute the `shutdown` command.

New plugins can be written to replace these plugins.
### 3.2.1 BMC Python Interface
```python
class Bmc(object):
    ""Interface class for bmc classes."" 
    def __init__(self, options=None):
        pass

    def get_chassis_state(self, remote_access_object):
        ""Get the current chassis state for a node.""
        pass

    def set_chassis_state(self, remote_access_object, new_state):
        ""Set the target chassis state for a node.""
        pass
```
These methods return a Boolean value.  For `get_chassis_state` the Boolean is `True` = chassis on or `False` = chassis off. For the `set_chassis_state` method, the Boolean denotes execution success (`True`) or failure (`False`).

### 3.2.2 OS Remote Access Python Interface
```python
class OsRemoteAccess(object):
    ""Interface for remote process execution.""
    def __init__(self, options=None):
        pass

    def execute(self, cmd, remote_access_data, capture=False, other=None):
        ""Using address and credentials, execute the cmd remotely.""
        pass
```
The return value of the `execute` command is a pair of values `(return_code, captured_stdout)`.  The return code of `0` signifies success.  Any other code is failure. If the `capture` parameter is `False` then the `captured_stdout` should be the `None` Python object.

### 3.2.3 PDU Interface
```python
class PduInterface(object):
    ""Interface class for bmc classes.""
    def __init__(self, options=None):
        pass

    def get_outlet_state(self, remote_access_object, outlet):
        ""Get the current chassis state for a node. Returns 'On' or 'Off'(Case insensitive)""
        pass

    def set_outlet_state(self, remote_access_object, outlet, new_state):
        ""Set the target chassis state for a node.""
        pass
```
