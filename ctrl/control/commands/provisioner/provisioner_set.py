# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
ProvisionDeleteCommand
"""
from .. import Command, CommandResult
from ...plugin import DeclarePlugin


@DeclarePlugin('provisioner_set', 100)
class ProvisionerSetCommand(Command):
    """
    Set options for the device in the provisioner
    """

    def __init__(self, device_name, configuration, plugin_manager, logger=None, ip_address=None, hw_address=None,
                 net_interface=None, image=None, bootstrap=None, files=None, kernel_args=None):
        """Retrieve dependencies, prepare to perform command."""
        Command.__init__(self, device_name, configuration, plugin_manager, logger, ip_address=ip_address,
                         hw_address=hw_address, net_interface=net_interface, image=image, bootstrap=bootstrap,
                         files=files, kernel_args=kernel_args)

        self.ip_address = ip_address
        self.hw_address = hw_address
        self.net_interface = net_interface
        self.image = image
        self.bootstrap = bootstrap
        self.files = files
        self.kernel_args = kernel_args

        self.device = self.configuration.get_device(self.device_name)
        if self.device.get("provisioner") is None:
            # TODO: Return a configuration error
            raise RuntimeError("No provisioner is specified in the config. Cannot perform command.")

        self.provisioner = self.plugin_manager.create_instance('provisioner', self.device.get("provisioner"))

    def execute(self):
        """Execute the command"""
        if self.device.get("device_type") not in ['compute', 'node']:
            return CommandResult(1, 'Failure: cannot perform provisioner actions on this device'
                                    ' type ({})'.format(self.device.get("device_type")))

        if self.ip_address is not None:
            args = [self.device, self.ip_address]
            if self.net_interface is not None:
                args.append(self.net_interface)
            self.provisioner.set_ip_address(*args)

        if self.hw_address is not None:
            args = [self.device, self.hw_address]
            if self.net_interface is not None:
                args.append(self.net_interface)
            self.provisioner.set_hardware_address(*args)

        if self.image is not None:
            self.provisioner.set_image(self.device, self.image)

        if self.bootstrap is not None:
            self.provisioner.set_bootstrap(self.device, self.bootstrap)

        if self.files is not None:
            self.provisioner.set_files(self.device, self.files)

        if self.kernel_args is not None:
            self.device = self.provisioner.set_kernel_args(self.device, self.kernel_args)

        self.configuration.set_device(self.device)

        return CommandResult(0, "Successfully set {} options for the provisioner".format(self.device.get("hostname")))
