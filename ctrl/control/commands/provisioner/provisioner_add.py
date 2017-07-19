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

    def __init__(self, device_name, configuration, plugin_manager, logger=None, provisioner=None):
        """Retrieve dependencies, prepare to perform command."""
        Command.__init__(self, device_name, configuration, plugin_manager, logger, provisioner=provisioner)

        self.device = self.configuration.get_device(self.device_name)
        provisioner = provisioner if provisioner != "UNDEF" else None
        config_provisioner = self.device.get("provisioner")
        config_provisioner = config_provisioner if config_provisioner != "UNDEF" else None
        if provisioner is not None and config_provisioner is not None \
                and provisioner != config_provisioner:
            raise RuntimeError("Device already has a provisioner, remove the first before adding another.")

        provisioner_name = provisioner or config_provisioner
        if provisioner_name is None:
            # TODO: Return a configuration error
            raise RuntimeError("No provisioner is specified via args or config. Cannot perform command.")

        self.provisioner = self.plugin_manager.create_instance('provisioner', provisioner_name)

    def execute(self):
        """Execute the command"""
        if self.device.get("device_type") not in ['compute', 'node']:
            return CommandResult(1, 'Failure: cannot perform provisioner actions on this device'
                                    ' type ({})'.format(self.device.get("device_type")))

        self.provisioner.add(self.device)
        self.configuration.set_device(self.device)

        return CommandResult(0, "Successfully added {} to the provisioner".format(self.device.get("hostname")))
