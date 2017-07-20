## 2.10 OOB Sensor Commands

The OOb sensor commands are designed to help users read the OOB sensors from devices. These commands use a REST API to read the OOB sensors.

### 2.10.1 `sensor get`

```
usage: ctrl sensor [-h] --sensor-name [SENSOR_NAME]
                   [--get-overtime <sample-rate> <duration>]
                   {get} device_name

positional arguments:
  {get}                 Select an action to perform
  device_name           Device where command will be executed.

optional arguments:
  -h, --help            show this help message and exit
  --sensor-name [SENSOR_NAME]
                        Provide a specific sensor or .*/all for all sensors
  --get-overtime <sample-rate> <duration>
                        Please specify 2 values: --get-overtime <sample-rate>
                        <duration>, both greater than 0

```bash
# ctrl sensor get --sensor-name[SENSOR_NAME] device_name
```
This command will get the values of the mentioned sensor from the specified compute node or device_name. If this command
fails it will provide an error message to the user.

# ctrl sensor get --sensor-name[SENSOR_NAME] device_name --get-overtime <sample-rate> <duration>
```
This command will get the values of the mentioned sensor from the specified compute node or device_name for a requested sample rate over a duration of time. If this command
fails it will provide an error message to the user.
