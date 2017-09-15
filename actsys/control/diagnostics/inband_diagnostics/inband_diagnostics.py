#
#Copyright (c) 2017 Intel Corp.
#

"""
Interface for inband diagnostic tests plugins.
"""

from control.console_log.ipmi_console_log.ipmi_console_log import IpmiConsoleLog
from control.diagnostics.diagnostics import Diagnostics
from control.plugin import DeclarePlugin


@DeclarePlugin('diagnostics_inband', 100)
class InBandDiagnostics(Diagnostics):
    """This class controls launching the inband diagnostic tests
    This needs the input of a file """
    MOCK_PROVISION = False
    Test_Status = {}
    Return_Code = {}

    def __init__(self, **kwargs):
        Diagnostics.__init__(self, **kwargs)
        self.reboot_true = False
        self.img = kwargs['diag_image']
        self.old_image = None
        self.kargs = kwargs['test_name']
        if self.kargs is None:
            self.kargs = 'DiagReboot=no'
        if "DiagReboot=yes" not in self.kargs:
            self.kargs += ' DiagReboot=no'
        else:
            self.reboot_true = True
        self.old_kargs = None
        self.console_log = None
        self.device = None
        self.bmc = None
        self.device_name = None
        self.plugin_manager = kwargs['plugin_manager']
        self.resource_manager = None
        self.provisioner = None
        self.power_manager = None

    def _verify_provisioning(self, device, img):
        self.old_image = self.device.get("image")
        self.old_kargs = self.device.get("provisioner_kernel_args")

        if self.MOCK_PROVISION is True:
            self.provisioner.add(self.device)
            self.provisioner.set_image(self.device, img)

        try:
            device_list = self.provisioner.list()
            img_list = self.provisioner.list_images()
        except Exception as ex:
            raise Exception(
                "Error: Failed to read data from provisioner because {0}. No tests will be run.".format(str(ex)))

        if device not in device_list or img not in img_list:
            raise Exception(
                "Error: Device does not exist in provisioner, provision device to continue")
        else:
            self.old_image = self.device.get("image")
            self.old_kargs = self.device.get("provisioner_kernel_args")

    def _provision_image(self, img, args):
        try:
            self.provisioner.set_image(self.device, img)
            self.provisioner.set_kernel_args(self.device, args)
        except Exception as ex:
            raise Exception("Failed to set image {0} or test {1}. Provisioner returned error {2}. "
                            "Cannot run diagnostics. ".format(img, args, str(ex)))

    def _set_node_state(self, state):
        result = self.power_manager.set_device_power_state(state)
        if result[self.device_name] is not True:
            raise Exception("Failed to power {0} node during provisioning "
                            "diagnostic image. No tests will be run.".format(state))

    def launch_diags(self, device, bmc):
        """launches the diagnostic tests"""
        self.device = device
        self.bmc = bmc
        bmc_ip_address = self.bmc.get("ip_address")
        bmc_user = self.bmc.get("user_name")
        bmc_password = self.bmc.get("password")
        self.device_name = self.device.get("hostname")

        if self.device.get("provisioner") is None or self.device.get("resource_controller") is None or \
                        self.device.get("device_power_control") is None:
            raise Exception("You are missing provisioner or resource_control or device_power_control keys in your "
                            "config file. Please edit the file and try again.")

        self.provisioner = self.plugin_manager.create_instance('provisioner', self.device.get("provisioner"))
        self.resource_manager = self.plugin_manager.create_instance('resource_control',
                                                                    self.device.get("resource_controller"))
        power_options = self._pack_options()
        self.power_manager = self.plugin_manager.create_instance('power_control', self.device.get(
            "device_power_control"), **power_options)

        if self.device.get("provisioner") in "mock":
            InBandDiagnostics.MOCK_PROVISION = True

        self._verify_provisioning(self.device_name, self.img)

        # Step 1: Remove node from resource pool
        dev_l = list()
        dev_l.append(self.device_name)
        current_state = self.resource_manager.check_nodes_state(dev_l)[1]
        if "idle" in current_state:
            result = self.resource_manager.remove_nodes_from_resource_pool(dev_l)
            if result[0] != 0:
                raise Exception(
                    "Cannot remove node from resource pool for running diagnostics since {0}".format(result[1]))
        else:
            raise Exception("Cannot remove node from resource pool. {}".format(current_state))
        # start console log
        try:
            self.console_log = IpmiConsoleLog(self.device_name, bmc_ip_address, bmc_user, bmc_password)
            self.console_log.start_log_capture('End of Diagnostics')
        except Exception as ex:
            raise Exception('Unable to connect to the bmc, update the config file for device {0} and try again. Error '
                            'received from console log: {1}'.format(self.device_name, str(ex)))

        # Step 2: Provision diagnostic image
        self._provision_image(self.img, self.kargs)
        self._set_node_state('Off')
        self._set_node_state('On')

        # Step 4: Provision node back to old image
        if not self.reboot_true:
            self._provision_image(self.old_image, self.old_kargs)
            self._set_node_state('Off')
            self._set_node_state('On')

        # Step 5: Add node back to resource pool
        result = self.resource_manager.add_nodes_to_resource_pool(dev_l)
        if result[0] != 0:
            raise Exception("Failed to add node back to resource pool")

        return "Diagnostics completed on node {0}".format(self.device_name)

    def _pack_options(self):
        """Return the node power control options based on the node_name and
                   configuration object."""
        options = {}
        dev_l = list()
        dev_l.append(self.device)
        options['device_list'] = dev_l
        options['bmc_list'] = self.bmc
        options['plugin_manager'] = self.plugin_manager
        return options