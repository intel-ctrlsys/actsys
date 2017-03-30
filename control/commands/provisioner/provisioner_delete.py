# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
ProvisionDeleteCommand
"""
from .. import Command, CommandResult
from ...plugin import DeclarePlugin


@DeclarePlugin('provisioner_delete', 100)
class ProvisionerDeleteCommand(Command):
    """
    Delete a device from the provisioner.
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

        self.provisioner.delete(self.device)
        self.configuration.set_device(self.device)

        return CommandResult(0, "Successfully deleted {} from the provisioner".format(self.device.get("hostname")))
