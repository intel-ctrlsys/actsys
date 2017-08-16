## Building and Installation

Requirements:

- [pip](https://pip.pypa.io/en/stable/) "The PyPA recommended tool for installing Python packages"

### Build and install actsys from the source:

1. Download and extract the source code.
2. In the source code directory, go to `datastore` directory, run `sudo python setup.py sdist`. This will produce a `dist` directory which contains the file `ctrlsys_datastore-<version>-tar.gz`. This file can be installed using the command `sudo pip install ctrlsys_datastore-<version>.tar.gz`.
3. In the source code directory, go to ctrl directory, run `sudo python setup.py sdist`. This will produce a `dist` directory which contains the file `ctrl-<version>-tar.gz`. This file can be installed using the command `sudo pip install ctrl-<version>.tar.gz`.

### Installation from an *.tar.gz file:

To install actys from a pre-built `*.tar.gz`, run the command `sudo pip install <file>.tar.gz`. You will need to first install the `*.tar.gz` of `datastore`, then install the `*.tar.gz` of `ctrl`.

### Installation from source:

To install directly from the source code (skipping build steps) follow these steps:

1. Download and extract the source code
2. In the source code directory, go to datastore directory, run `sudo python setup.py install`
3. In the source code directory, go to ctrl directory, run `sudo python setup.py install`

### Removing actsys

To remove actsys from your machine run `sudo pip uninstall ctrl`. You will need to remove your configuration file manually.
