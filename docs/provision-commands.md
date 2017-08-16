## 2.9 Provision Commands

The Provision commands are designed to help advanced users provision and de-provision devices. These commands use the provisioner interface to perform these commands. Which provisioner to use is determined by the configuration of the device being edited.

### 2.9.1 `provision add`

```
usage: provision add [-h] [--provisioner PROVISIONER] device_name

positional arguments:
  device_name           The device name of the device you want to add.

optional arguments:
  -h, --help            show this help message and exit
  --provisioner PROVISIONER The provisioner you want to add this device too.
```

The provisioner to add this device too is determined by the --provisioner flag or whatever is in the configuration for the given device. Valid provisioners are determined by what plugins are loaded into the provisioner interface (see section 3.6).

### 2.9.2 `provision delete`

```
usage: provision delete [-h] device_name

positional arguments:
  device_name  The name of the device you want to delete.

optional arguments:
  -h, --help   show this help message and exit
```

### 2.9.3 `provision set`

```
usage: provision set [-h] [--ip_address IP_ADDRESS] [--hw_address HW_ADDRESS]
                     [--net_interface NET_INTERFACE] [--image IMAGE]
                     [--bootstrap BOOTSTRAP] [--files FILES]
                     [--kernel_args KERNEL_ARGS]
                     device_name

Manage devices by setting options to them.

positional arguments:
  device_name           The device name of the device you want to add

optional arguments:
  -h, --help            show this help message and exit
  --ip_address IP_ADDRESS, -i IP_ADDRESS
                        The IP address you want to set. This is set on the
                        interface specified with the --net_interface flag. If
                        no value is given, then no change takes place. Set
                        this field to UNDEF to remove the currently specified
                        IP address.
  --hw_address HW_ADDRESS, -a HW_ADDRESS
                        The Hardware address of this device. This is set for
                        the interface specified with the --net_interface flag.
                        If no value is given, then no change takes place. Set
                        this field to UNDEF to remove the currently specified
                        hardware address.
  --net_interface NET_INTERFACE, -d NET_INTERFACE
                        The network interface which you want to set the
                        options on. This applies to the --ip_address and
                        --hw_address flags. If no network interface is
                        supplied, it defaults to eth0.
  --image IMAGE, -m IMAGE
                        The image you want to set to this node. If no value is
                        given, then no image is set. The image should already
                        be defined and known to the provisioner and only the
                        image name is specified here.
  --bootstrap BOOTSTRAP, -b BOOTSTRAP
                        The bootstrap to be used by the provisioner. The
                        existance and use of a bootstrap image depends on the
                        provisioner. If no value is given, then no change
                        takes place. Set this field to UNDEF to remove the
                        currently specified bootstrap.
  --files FILES, -f FILES
                        The files you want to set on this device. This should
                        be a comma seperated list if you are specifying
                        multiple files. If no value is given, then no change
                        takes place. Set this field to UNDEF to remove all
                        existing files.
  --kernel_args KERNEL_ARGS, -k KERNEL_ARGS
                        The kernel arguments to set on this device. This
                        should be in the same format you want to show up in
                        the kernel arguments. If no value is given, then no
                        change takes place. Set this field to UNDEF to remove
                        all existing kernel arguments.
```