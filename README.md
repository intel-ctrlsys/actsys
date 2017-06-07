# Actsys

Actsys is a unified API to perform commands on excascale computers. With this API are two UIs, a CLI and a REST API. Actsys is build in a modular fashion to support clusters and computers of many different configurations.

## Quick-start

1. Make sure the prerequisites are installed. You can view the prerequisites in the `setup.py` file.
2. Install Actsys by running `python setup.py install`.
3. Browse the Actsys help:

```
[new-user@my-machine]$ ctrl -h
usage: ctrl [-h] [-V] [-v] [-t TIMEOUT]

            {power,resource,process,get,set,service,datastore,provision,bios,sensor}
            ...

Control Component Parser

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         Provides the version of the tool
  -v, --verbosity       increase output verbosity
  -t TIMEOUT, --timeout TIMEOUT
                        Provides a timeout for the command

Sub Commands:
  List of Valid Sub Commands

  {power,resource,process,get,set,service,datastore,provision,bios,sensor}
    power               Power on/off/reset a device.
    resource            Resource add/remove from a resource pool.
    process             Process list/kill on a node in a cluster.
    get                 Get powercap/freq value of a node.
    set                 Set powercap/freq value of a node.
    service             Check, start or stop services specified in the
                        configuration file
    bios                Update or get version of bios on specified nodes/group
                        of nodes
    sensor              Get specified sensor value on specified nodes/group of
                        nodes

```

## User guide

To get much farther, you'll need to look at the user guide. This is either packaged with the distribution or online on the wiki.

## Developers Guide

This section contains a few notes about development processes.

### Test Development:

This document describes how to use these tests and any docker related
limitations.


#### Prerequisites for testing are:

* python 2.7.* (should be pre-installed)
* pylint (use you favorite package manager like apt-get, yum, or zypper)
* py.test (use you favorite package manager like apt-get, yum, or zypper)
* pytest-cov (use PIP to install this dependency; use google to figure out how to install PIP for your specific platform)

#### Running tests:

> NOTE: All unit tests are expected to run without hardware or system dependencies. Your tests should mock all necessary calls to function for instance in docker.

In the root git folder type the following command:

```
$ make test
```

These tests can be run from a pycharm configuration for "Python tests->Unittests" as a "Test all in folder" configuration.


#### Checking Coverage:

Run the coverage task in the Makefile in the root of the repo.

```
$ make coverage
```

This can by run from a pycharm configuration for "Python" not "Python tests".

A ".coverage" file will be created as well as a ".html" folder with a web
version of the report.

### Folder Structure

The folder structure being used is very hierarchical and generally is in the following format:

```
feature_folder:
    interfaces and common code (words separated by underscores):
        tests for interfaces and common code (must be "tests"):
        specific plugin implementation (words separated by underscores):
            tests for specific implementation (must be "tests"):
```

Each folder in this structure containing python code must also have an empty
__init__.py file included.

This will also be true for non-feature source code like the initial CLI
implementation.  For example:

```
ctrl:
        __init__.py
        .coveragerc
        plugin: (plugin manager folder)
                __init__.py
                <source_files>
                tests:
                        __init__.py
                        <test_source_files>
                <sourcefiles>
        os_remote_access: (remote OS access and execution feature)
                __init__.py
                <common_source_files>
                tests:
                        __init__.py
                        <common_test_source_files>
                ssh:
                        __init__.py
                        <plugin_source_files>
                        tests:
                                __init__.py
                                <plugin_test_source_files>
        commands: (command invoker plugins)
                __init__.py
                <common_source_files>
                tests:
                        __init__.py
                        <common_test_source_files>
                power_on_command:
                        __init__.py
                        <plugin_source_files>
                        tests:
                                __init__.py
                                <plugin_test_source_files>
        utilities (generally useful classes):
                __init__.py
                <source_files>
                tests:
                        __init__.py
                        <test_source_files>
        bmc: (IPMI implementation of BMC control)
                __init__.py
                <common_source_files>
                tests:
                        __init__.py
                        <common_test_source_files>
                ipmi_util:
                        __init__.py
                        <plugin_source_files>
                        tests:
                                __init__.py
                                <plugin_test_source_files>
                mock:
                        __init__.py
                        <plugin_source_files>
                        tests:
                                __init__.py
                                <plugin_test_source_files>
        clusterctl: (Example CLI name only)
                __init__.py
                <source_files>
                tests:
                        __init__.py
                        <test_source_files>
```

Every production source file has tests in an immediate subfolder called "tests"
and features are at the top level with plugin implementations having an extra
level down to prevent issues when a plugin is more than one python file
(or module).

----------------------------------------------------------
Copyright (c) 2016-2017 Intel Corp.
