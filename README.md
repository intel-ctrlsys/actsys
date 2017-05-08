# DataStore

DataStore is reusable, encapsulated, component for storing device information in HPC clusters. DataStore is targeted toward excascale clusters. As such datastore is desinged to be flexible, while providing a common interface for use.

DataStore holds 4 types of objects:

1. configuration - System-wide configuration. Examples include log file location, system wide defaults and constants.
2. logs - Any log. This can be from a system, device, anything.
3. devices - Any item with an IP address. Devices store their own configuration and state.
4. profiles - properties common among devices. A great example is access port = 22, every devices uses port 22 so we write it once in a profile and link devices to that profile.

## Installation

Install with pip: `pip install <datastore-file>`

Or install from source:

1. cd `/path/to/datastore/src`
2. python setup.py sdist
3. pip install dist/datastore-<version>.tar.gz

If you are planning on using a PostgreSQL database with DataStore you must setup the correct schema first. This can be done by following the instructions in datastore/database_schema/README

## Usage

To use the datastore you must first select a location for the DataStore to be created. Currently, DataStore supports two locations:

1. A file
2. A PostgreSQL DB

The method for selecting which datastore is used depends on how you plan to use datastore. DataStore can be used as a python module or as a CLI.

### With the CLI

With DataStore installed you can run `datastore` on the command line. DataStore attempts to get its current DB location from the environment variable `DATASTORE_LOCATION`. If it cannot connect to whatever was supplied (or not supplied) in your environment variable it will default to storing its configuration at /usr/share/datastore_db. It will also default to storing its logs at /var/log/datastore.log. This will error if you do not have permission to access these files.

Running the command `datastore -h` or `datastore --help` will show  the help on the command line:

```
[user@host]$ datastore --help
usage: datastore [-h] {device,profile,config,log} ...

optional arguments:
  -h, --help            show this help message and exit

Data Type:
  What datatype to manipulate

  {device,profile,config,log}
    device              Manipulations for devices
    profile             Manipulations for profiles
    config              Manipulations for configuration
    log                 Manipulations for logs
```

This same help command can be run for any of the subcommands. For example 'datastore device --help' will produce:

```
[user@host]$ datastore device -h
usage: datastore device [-h] [--fatal]
                        {list,get,set,delete} [options [options ...]]

positional arguments:
  {list,get,set,delete}
  options               key=value pairs used to assist in selecting and
                        setting attributes

optional arguments:
  -h, --help            show this help message and exit
  --fatal, -f           The existance of this flag fatally deletes an item.
                        The default is to only logically delete the item.
```

See the datastore help commands for more details.

### With the python API

DataStore can be imported and used like any python API. This allows DataStore to easily be extended or used in external applications. In general the steps to do this are:

1. Import the `DataStoreBuilder`
2. Specify what you want in the DataStore with the `DataStoreBuilder`
3. Build it
4. Use it

These steps translate to code like so:

```
from datastore import DataStoreBuilder

# Build a datastore instance
ds = DataStoreBuilder.get_datastore_from_string(connection_string) # A file location or PostgresURI

# Use it
ds.get_device("compute1")
# ...

logger = ds.get_logger()
logger.journal(cmd_name, cmd_args, device, result)
logs = ds.list+logs()
```

The full documentation for the Datastore is found in the datastore/datastore.py file. You can get a more human readable
for with pydoc by running `pydoc datastore/datastore.py`.

### Usage for just logging

If you only want to log to the screen then you can just use the DataStore logger:

```
from datastore import get_logger, add_stream_logger

# Get a bare bones logger
logger = get_logger()
# Add a stream logger (prints to std.err)
add_stream_logger(logger)
```

## DataStore Log Levels

DataStore Follows the log levels outlined in the [Python documentation](https://docs.python.org/2/library/logging.html#logging-levels) while adding one additional level called JOURNAL (15). This makes the chart of logging levels look like:

| Level	| Numeric value |
|*******|***************|
| CRITICAL	| 50 |
| ERROR	| 40 |
| WARNING	| 30 |
| INFO	| 20 |
| JOURNAL | 15 |
| DEBUG	| 10 |
| NOTSET	| 0 |

The default log level is DEBUG, but can be set to other levels if desired.

## The possible future of DataStore

This section contains ramblings on how we might make DataStore better.

**Idea 1:** Change the 4 kinds of objects:

1. global_configuration - remains the same as global configuration
2. logs - remains the same
3. devices - device state (only). State may be changed by anything at any time. I.E it was allocated by a user or shut down by a administrative process.
4. device_configuration - device configuration. May shared among devices. Configuration may only be edited by admins. When a config for a device is edited the config is edited for all of these devices. This makes changes on one device more difficult (the configuration will have to be cloned and modified to edit only 1 out of a group of 10), but changes in aggregate easier.

Problems: State vs configuration. This is not an easy line to draw. For example an IP address may be configured or it may be dynamic and is a state of what the DNS provider gave us. This argument can be extended to more complex ideas like what image does this node have. Its current image is centos7.2 but its configured to centos 7.3, should state and configuration be different?