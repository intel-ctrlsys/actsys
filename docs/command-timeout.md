## 2.12 Commands Timeout
This section describes how to use the timeout feature for control commands. If a command is not done before the timeout expired, the command will exit and a timeout exception
event will be logged in datastore.

Timeout value is a number (either integer or float). There are two ways to specify timeout value for a command.

One way is to set the timeout as a global variable, named "cmd_timeout", in configuration file. Please refer to section 2.2.1 about how to
set global variables in configuration file. The "cmd_timeout" value is for all control commands. The user can also change the timeout value
through datastore command later using the following command:

# ctrl datastore config set cmd_timeout <timeout_value>

The other way is to set timeout value during runtime for each individual command. An optional command line argument, "-t/--timeout", is provided to
allow users to specify the timeout value. For example, the command "ctrl -t 300 bios update -i<IMAGE> device_name" will set the timeout value to be
300 seconds to do "bios update". The "-t/--timeout" argument has higher priority than the "cmd_timeout" value in configuration file.

A timeout value of 0 means that the timeout does not take effect. If no timeout value is set (either through configuration or command argument), a default value of 1800 seconds will be used.