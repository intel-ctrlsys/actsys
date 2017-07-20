## 3.6 Provisioner Interface

The current interface for provisioners can be found in the source code. This contains the expected return codes and exceptions in the doc strings.

Two implemtations of this interface are packaged with ctrl:

1. mock - This always returns successful when called. It is designed to be a placeholder for testing. While not very useful for the end user, this implementation is a good place to start when implementing a new provisioner as it shows the developer what device mutations are expected.
2. warewulf - This implements an interface to warewulf via the shell. This is warewulfs most developed interface. In the case of permission errors or general problems a ProvisionerException is thrown. Note that ctrl does not depend on warewulf so installers are not required to install warewulf for you. You must ahve warewulf installed to use this plugin.