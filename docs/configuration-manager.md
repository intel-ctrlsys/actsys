Configuration manager is used to read, parse and expose data from configuration files across Ctrl.

Configuration manager is following a Singleton pattern. Thus, there will be one and only one instance of the configuration manager for each file successfully parsed, despite of the number of times or places where we call the configuration manager constructor for the same file. That said, the instance returned by the configuration manager will be the one from the first time the file was parsed without errors.

There could be several types of configuration files, but for now we are only supporting one: `ClusterConfiguration`, although the configuration manager can support more in case is needed. A `ConfigurationTypeInterface` was created for this purpose.

__Note__: For now, only JSON files can be parsed by the configuration manager, but if a different format would be needed in the future, it should be pretty simple to support it by adding a parser object for that kind of files and use it in the ClusterConfigurationParser instead of the current JsonParser.

#### Using the Configuration Manager.

To create a configuration manager call its constructor and pass it the path to the file that will be parsed.

```python
from control.configuration_manager.configuration_manager import ConfigurationManager
cm = ConfigurationManager('path_to_configuration_file/file_name.json')
```

If the configuration manager cannot find the file it will throw a `__FileNotFound__` exception.
If the configuration manager cannot parse the file (i.e. is not a valid JSON file), it will throw a `__NonParsableFile__` exception.

To access the data parsed from the configuration file, the configuration manager exposes the following API:

```python
from control.configuration_manager.configuration_manager import ConfigurationManager
cm = ConfigurationManager('path_to_configuration_file/file_name.json')
extractor = cm.get_extractor('ClusterConfiguration')
# extractor = cm.get_extractor()
```

By default, get_extractor returns an extractor for `ClusterConfiguration` type. If another type would be required, it should be passed as a parameter for get_extractor function. However, `ClusterConfiguration` is the only type supported for now.

#### Using the Extractor.

The extractor is an object that exposes the data parsed by the configuration manager to the users that will consume that data. Notice that users refers to the code that needs the configuration file data to process it.

For the `ClusterConfigurationExtractor` the following functions are defined:

##### Get_device function.

This function receives a `device_id`, then searches that device id in the internal extractor data and returns a deep copy of that device to the user.
If not found, then it returns None.
This function looks for the given device_id no matter what device_type it might has.

Example:

```python
from control.configuration_manager.configuration_manager import ConfigurationManager
cm = ConfigurationManager('ctrl-config-example.json')
extractor = cm.get_extractor()
device = extractor.get_device('compute-29')
```

##### Get_device_types function.

This function will return a list with all the device_type names in the extractor data.
If the extractor data is empty, an empty list will be returned ([]).

Example:

```python
from control.configuration_manager.configuration_manager import ConfigurationManager
cm = ConfigurationManager('ctrl-config-example.json')
extractor = cm.get_extractor()
types = extractor.get_device_types()
```

##### Get_devices_by_type function.

This function receives the device_type to be searched in the extractor data and returns a dictionary with a copy of the objects of that type found in the extractor data.
The keys of that dictionary are the device_id values from the objects of that type.
If the device_type doesn't exist or there's no objects of that type in the extractor data, it will return an empty dictionary ({}).

Example:

```python
from control.configuration_manager.configuration_manager import ConfigurationManager
cm = ConfigurationManager('ctrl-config-example.json')
extractor = cm.get_extractor()
nodes = extractor.get_devices_by_type('node')
bmcs = extractor.get_devices_by_type(cm.BMC_TAG)
```

In the example, cm.BMC_TAG is being passed to the get_devices_by_type function to get all the 'bmc' objects from the configuration file.
There are some already defined variables that can be used for the most common types in the `ClusterConfigurationParser`: NODE_TAG, BMC_TAG, PSU_TAG, PDU_TAG and CONFIG_VARS_TAG.
Use them instead of hard coding the 'node', 'bmc', 'psu', 'pdu', or 'configuration_variables' strings.

##### Get_node function.

This function receives a `device_id`, which will be searched in among the nodes in the extractor data.
If the device_id is a node and is in the extractor data, a deep copy of that device will be returned.
If not found or is not a node, then it returns None.

Example:

```python
from control.configuration_manager.configuration_manager import ConfigurationManager
cm = ConfigurationManager('ctrl-config-example.json')
extractor = cm.get_extractor()
device = extractor.get_node('compute-29')
```

##### Get_bmc function.

This function receives a `device_id`, which will be searched in among the bmcs in the extractor data.
If the device_id is a bmc and is in the extractor data, a deep copy of that device will be returned.
If not found or is not a bmc, then it returns None.

Example:

```python
from control.configuration_manager.configuration_manager import ConfigurationManager
cm = ConfigurationManager('ctrl-config-example.json')
extractor = cm.get_extractor()
device = extractor.get_bmc('bmc-compute-29')
```

##### Get_psu function.

This function receives a `device_id`, which will be searched in among the psus in the extractor data.
If the device_id is a psu and is in the extractor data, a deep copy of that device will be returned.
If not found or is not a psu, then it returns None.

Example:

```python
from control.configuration_manager.configuration_manager import ConfigurationManager
cm = ConfigurationManager('ctrl-config-example.json')
extractor = cm.get_extractor()
device = extractor.get_psu('mypsuid')
```

##### Get_pdu function.

This function receives a `device_id`, which will be searched in among the pdus in the extractor data.
If the device_id is a pdu and is in the extractor data, a deep copy of that device will be returned.
If not found or is not a psu, then it returns None.

Example:

```python
from control.configuration_manager.configuration_manager import ConfigurationManager
cm = ConfigurationManager('ctrl-config-example.json')
extractor = cm.get_extractor()
device = extractor.get_pdu('pdu-1')
```

##### Get_config_vars function.

Returns a deep copy of the global configuration variables in the configuration file.
Returns None, in case there are no configuration_variables in the extractor data.

Example:

```python
from control.configuration_manager.configuration_manager import ConfigurationManager
cm = ConfigurationManager('ctrl-config-example.json')
extractor = cm.get_extractor()
config_vars = extractor.get_config_vars()
```

#### The Device Class.

The functions seen above return Device objects (except by get_device_types and get_devices_by_type).

A Device object can have any number of attributes and those attributes are defined where the object is created. This means that two Device objects might have a different set of attributes between them.

Other important characteristic of the Device objects is that their attributes are read-only attributes, meaning that once the device is created you cannot assign a value to those attributes.
In addition, a device attribute contains any type of object (e.g., an integer, a string, a list, a dictionary or a custom object). Nevertheless, the lists and dictionaries returned when accessing an attribute can be modified and those changes will be reflected in the device object.

In the following example, a demonstration of how to create a Device and how to access its attributes is shown:

```python
from control.configuration_manager.objects.device import Device
device = Device({'attribute1':'value1', 'attribute2':42})
print device.attribute1 # prints 'value1'
print device.attribute2 # prints 42
print device.get_attribute_list() #prints a list with all the device's attributes.
print device.invalid_attribute # prints None
print device.get_attribute_list() #prints a list with the attributes of the device.
device.attribute2 = 50
print device.attribute2 # prints 42, as its read-only attribute.
```

See that a device will return `None` if the attribute that is being requested doesn't exists in the device's attributes. To know what attributes a device has, use the `get_attribute_list` function.

__Caveats__:

There are some internal functions of the `Device` class that can be used to update its internal dictionary and consequently its attributes or attribute's values.
You can find those functions in the Device's super class: `ConfigurationManagerItem` at control/configuration_manager/objects/configuration_manager_item.py.

For more details about defined attributes for the `ClusterConfiguration` Devices, see section 2.2.1 Cluster Configuration Files(2.2.1-Cluster-Configuration-File.md) in the User Guide.
