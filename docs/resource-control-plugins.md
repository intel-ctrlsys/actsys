To support a different type of resource manager, a resource control plugin and a factory that creates the plugin instance will need to be developed. The resource control plugin will implement the "ResourceControl" interface, and the factory will implements the "PluginMetadataInterface" interface.

### 3.3.1 ResourceControl Interface
```python
class ResourceControl(object):
    ""Interface for resource control classes.""
    def __init__(self):
        pass

    def remove_node_from_resource_pool(self, node_name):
        ""Remove the specified node from the cluster resource pool""
        pass

    def add_node_to_resource_pool(self, node_name):
        ""Add the specified node to the cluster resource pool""
        pass

    def check_node_state(self, node_name):
        ""Check the state of the specified node""
        pass

    def check_resource_manager_installed(self):
        ""Check whether the resource manager is installed ""
        pass
```
The `remove_node_from_resource_pool`, `add_node_to_resource_pool`, and `check_node_state` functions take a compute node name as the input parameter, and returns a `<return_code, message>` tuple. A `return_code` of 0 means the command executes succesfully.

The `check_resource_manager_installed` function returns a boolean value: `True` means that the resource manager is installed and running and `False` means the opposite. A typical way of checking whether a resource manager is installed and running is to run a command of that resource manager. For example, `sinfo` command of the SLURM resource manager.

### 3.3.2 PluginMetadataInterface Factory Interface
```python
class PluginMetadataInterface(object):
    ""Interface for all plugins added to the plugin manager.""
    def __init__(self):
        pass

    def category(self):
        ""Retrieves the category name for the plugin.""
        pass

    def name(self):
        ""Retrieves the category implementation name for the plugin.""
        pass

    def priority(self):
        ""
        Retrieves the priority of the implementation for the plugin for
        default plugin selection.
        ""
        pass

    def create_instance(self, options=None):
        ""Factor for this specific plugin instance.""
        pass
```
The return value of the `category` function must always be `"resource_control"`. The return value of the `name` function is the name of the resource manager specified in the configuration file (e.g. `slurm`). The `priority` function returns a positive integer indicating the priority of the plugin. The `create_instance` function should always create an instance of the resource control plugin and return it.
