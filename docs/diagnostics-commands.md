## 2.13 Diagnostics Commands

The Diagnostics commands are designed to help advanced users run diagnostic tests on compute nodes. These commands use the diagnostics interface to perform these commands. 

### 2.13.1 `diag online`

```
usage: diag online [-h] [--image DIAGNOSTIC_IMAGE] [--test TESTS] device_name

positional arguments:
  device_name           The device name of the device you want to add.

optional arguments:
  -h, --help            show this help message and exit
  --image IMAGE         The diagnostic image you want to add use for running tests
  --tests TEST          The diagnostic tests to run on the compute node. These test would include the kernel arguments
                        to set while provisioning the node.
```

### 2.13.2 `diag offline`

```
usage: diag offline [-h] [--test TESTS] device_name

positional arguments:
  device_name            The name of the device you want to delete.

optional arguments:
  -h, --help             show this help message and exit
  --tests TESTS          The diagnostic tests to run on the compute node, IFST/Ping
```
