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

    def __init__(self, args=None):
        """Retrieve dependencies, prepare to perform command."""
        Command.__init__(self, args)

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

        if self.command_args.get("ip_address") is not None:
            args = [self.device, self.command_args.get("ip_address")]
            if self.command_args.get("net_interface") is not None:
                args.append(self.command_args.get("net_interface"))
            self.provisioner.set_ip_address(*args)

        if self.command_args.get("hw_address") is not None:
            args = [self.device, self.command_args.get("hw_address")]
            if self.command_args.get("net_interface") is not None:
                args.append(self.command_args.get("net_interface"))
            self.provisioner.set_hardware_address(*args)

        if self.command_args.get("image") is not None:
            self.provisioner.set_image(self.device, self.command_args.get("image"))

        if self.command_args.get("bootstrap") is not None:
            self.provisioner.set_bootstrap(self.device, self.command_args.get("bootstrap"))

        if self.command_args.get("files") is not None:
            self.provisioner.set_files(self.device, self.command_args.get("files"))

        if self.command_args.get("kernel_args") is not None:
            self.device = self.provisioner.set_kernel_args(self.device, self.command_args.get("kernel_args"))

        self.configuration.device_upsert(self.device)

        return CommandResult(0, "Successfully set {} to the provisioner".format(self.device.get("device_id")))
