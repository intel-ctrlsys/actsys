The ctrl logs reside in the ctrl log file which is available in the user's home directory as "ctrl.log".

###Log Format:
The format of the log messages is:

```H:M:S, ms  LOGLEVEL ctrl: message```

Where:
* H:M:S,ms is the message timestamp with milliseconds.
* LOGLEVEL: is the message loglevel.
* ctrl: is the name of the program that created the message.
* message: log message itself.

A common log file could look like:

2016-12-19 10:39:54,106 WARNING  ctrl  : Device compute skipped, because it is not found in the config file.
2016-12-19 10:39:59,218 JOURNAL  ctrl  : services status compute-29, Job Started
2016-12-19 10:39:59,218 DEBUG    ctrl  : Attempting to check for service orcmd on node compute-29
2016-12-19 10:40:03,233 DEBUG    ctrl  : Attempting to check for service gmond on node compute-29
2016-12-19 10:40:07,248 JOURNAL  ctrl  : services status compute-29, 255 - Failed: status - orcmd

###Journal Logs
Ctrl captures data from the commands issued through the command interface and store it into a file for troubleshooting purposes.  After issued a command, the journal will log the timestamp of the begging of the execution . Once the execution finished, will log the result and the timestamp as well.

The journal logs can be distinguished from other logs by the "JOURNAL" label. After the command with their arguments, it will appear a "Job Started" message or the result message. For the example above, the last line shows the JOURNAL result  message of  'service status compute-29'.
