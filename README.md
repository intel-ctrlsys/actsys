# DataStore

DataStore is reusable, encpsulated, componnent for storing node information in HPC clusters. DataStore is targeted toward excascale clusters. As such datastore is deisnged to be flexible, while providing a common interface for use.

## Installation

Install with pip: `pip install <datastore-file>`

Or install from source:

1. cd `/path/to/datastore/src`
2. python setup.py sdist
3. pip install dist/datastore-<version>.tar.gz 

## Usage

DataStore can be used as a python module or as a CLI.

### With the CLI

With DataStore installed you can run the `datastore` on the command line. Running the command `datastore -h` or `datastore --help` will show  the help on the command line:

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

### With the python API

DataStore can be imported and used like any python API. This allows DataStore to easily be extended or used in external applications. In general the step to do this are:

1. Import the `DataStoreBuilder`
2. Specify what you want in the DataStore with the `DataStoreBuilder`
3. Build it
4. Use it

These steps translate to code like so:

```
from datastore import DataStoreBuilder

# Build a datastore instance
dsb = DataStoreBuilder()
dsb.add_postgres_db(connection_uri)
ds = dsb.build()

# Use it
ds.device_get()
# ...

logger = ds.get_logger()
logger.journal(cmd_name, cmd_args, device, result)
logs = ds.log_get()
```

Or if you want to have a file db instead:
```
from datastore import DataStoreBuilder

# Build a datastore instance
dsb = DataStoreBuilder()
# If you don't give filestore a location, it will create two files ~/datastore.config
# and ~/datastore.log
dsb.add_file_db(None)
ds = dsb.build()

# Use it
ds.device_get()
# ...

logger = ds.get_logger()
logger.journal(cmd_name, cmd_args, device, result)
logs = ds.log_get()
```

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

DataStore Follows the log levels outlined in the [Python documentation](https://docs.python.org/2/library/logging.html#logging-levels) while adding one additional level called JOURNAL (35). This makes the chart of logging levels look like:

| Level	| Numeric value |
|*******|***************|
| CRITICAL	| 50 |
| ERROR	| 40 |
| WARNING	| 30 |
| INFO	| 20 |
| JOURNAL | 15 |
| DEBUG	| 10 |
| NOTSET	| 0 |

DataStore logs all of it function calls to log level DEBUG. DataStore results are printed to log level INFO. When print_to_screen is set these messages are shown (depending on log level set).