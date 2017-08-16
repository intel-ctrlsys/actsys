## 2.6 Service Commands

To get the help menu of the service commands enter `ctrl service --help` on the command line.
```
usage: ctrl service [-h] {status,start,stop} device_name

positional arguments:
  {status,start,stop}  Select an action to perform
  device_name          Device where command will be executed.

optional arguments:
  -h, --help           show this help message and exit

```

These commands only accept devices whose type is "node". Any other kind of device will result in a error. The service commands attempt to mimic systemctl behavior. The service commands perform actions on the services specified in the configuration file.

```bash
ctrl service status <device_name>
```
The command will attempt to check the status of services on a given device.

```bash
ctrl service start <device_name>
```
The command will attempt to start the services on a given device.

```bash
ctrl service stop <device_name>
```
The command will attempt to stop the services on a given device.