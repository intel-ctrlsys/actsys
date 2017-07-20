## 3.8 Diagnostics Interface

The current interface for diagnostics can be found in the source code. This contains the expected return codes.

One implemtation of this interface is packaged with ctrl:

mock - This always returns successful when called. It is designed to be a placeholder for testing. While not very useful for the end user, this implementation is a good place to start when implementing a new diagnostics plugin as it shows the developer what possible steps are expected.
