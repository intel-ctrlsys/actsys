## 2.8 Bios Commands
To get the help menu of bios commands, use the "./ctrl bios --help" command.
```

usage: ctrl bios [-h] {update, get-version} [-i [IMAGE]] device_name

positional arguments:
  {update,get-version}  Select one of the following options: update/get-version
                      Ex: ctrl bios update -i <IMAGE> node001
  device_name         Device (usually a compute node) for which command will be executed.

```bash
# ctrl bios update -i<IMAGE> device_name
```
This command will flash the node with the provided bios image followed by a reboot. If the update or reboot fails, the command will fail and notify user a proper message.
```bash
# ctrl bios get-version device_name
```
This command will return the last bios image version, md5 of the bios image and time of the last bios update.