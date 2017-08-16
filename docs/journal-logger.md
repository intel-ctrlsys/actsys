Ctrllogger is used for logging messages in Ctrl, the logs will be available in the user's home directory as "ctrl.log".

CrtlLogger is a singleton class which extends the [python logging module](https://docs.python.org/2/library/logging.html), a standard library module which provides a set of functions for simple logging usage.

The logging module provides functions that are named after the level or severity of the events they are used to track.

|LEVEL       | When it's used                                                                              |
|------------| --------------------------------------------------------------------------------------------|
|DEBUG       | Detailed information, typically of interest only when diagnosing problems.                  |
|INFO        | Confirmation that things are working as expected.                                           |
|WARNING     | An indication that something unexpected happened, or indicative of some problem in the near future. The software is still working as expected.|
|ERROR       | Due to a more serious problem, the software has not been able to perform some function.     |
|CRITICAL    | A serious error, indicating that the program itself may be unable to continue running.      |

CtrlLogger includes a new function named journal that will log detailed information of the start of a command execution as a result of the same.

**journal**(*command:Command*, *result:CommandResult=None*)

*command*: The command object has important information as the command name, the target device and the arguments.
*result*: The command result has the return code and the message after a command execution.

###Using the CtrlLogger.

To instance a logger use the CtrlLogger function get_ctrl_logger(). As CtrlLogger is following a Singleton pattern, multiple calls to get_ctrl_logger() will always return a reference to the same Logger object named "ctrl".

####Simple example
Simple message to log
```
from control.ctrl_logger.ctrl_logger import get_ctrl_logger
logger  = get_ctrl_logger()
logger.warning('This is a simple warning message')
```

and will display:
```2016-12-15 16:53:40,479 WARNING  ctrl  : This is a simple warning message```

####Log variable data
To log variable data, use the format string for the message and append the variable data as arguments:
```
from control.ctrl_logger.ctrl_logger import get_ctrl_logger
logger  = get_ctrl_logger()
logger.error('Device %s failed', 'node03')
```

will display:
```2016-12-15 16:53:40,479 ERROR  ctrl  : Device node03 failed.```

#### Log multiple messages
If you want to log multiple messages you can do it by sending a list of messages. Journal doesn't support multiple messages and variable data is not supported for multiple messages.
```
from control.ctrl_logger.ctrl_logger import get_ctrl_logger
logger  = get_ctrl_logger()
messages = ['With CtrlLogger', 'you can send', 'multiple messages']
logger.info(messages)
```

will display each item as a different message:
```
2016-12-16 11:51:45,400 INFO     ctrl  : With CtrlLogger
2016-12-16 11:51:45,400 INFO     ctrl  : you can send
2016-12-16 11:51:45,400 INFO     ctrl  : multiple messages
```
