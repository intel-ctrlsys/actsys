# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
ServicesCheckCommand Plugin
"""
from .. import Command, CommandResult
from ...plugin import DeclarePlugin


@DeclarePlugin('provisioner_add', 100)
class ProvisionerAddCommand(Command):
    """
    Add a device to the provisioner.
    """

    def __init__(self, args=None):
        """Retrieve dependencies and prepare for power on"""
        Command.__init__(self, args)

        print("getting device")
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

        print("adding...")
        self.provisioner.add(self.device)
        self.configuration.device_upsert(self.device)

        return CommandResult(0, "Successfully added {} to the provisioner".format(self.device.get("device_id")))
