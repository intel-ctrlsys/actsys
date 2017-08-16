## 3.7 OOB Sensor Interface

The current interface for OOB Sensor can be found in the source code. This contains the expected return codes and exceptions in the doc strings.

One implementation of this interface is packaged with ctrl:

1. mock - This always returns values of 10.0 for any sensor. It is designed to be a placeholder for testing. While not very useful for the end user, this implementation is a good place to start when implementing a new OOB Sensor plugin.