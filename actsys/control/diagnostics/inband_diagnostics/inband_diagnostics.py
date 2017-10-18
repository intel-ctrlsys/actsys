#
#Copyright (c) 2017 Intel Corp.
#

"""
Interface for inband diagnostic tests plugins.
"""
import queue
import re
import os
from threading import Thread
from control.console_log.ipmi_console_log.ipmi_console_log import IpmiConsoleLog
from control.diagnostics.diagnostics import Diagnostics
from control.plugin import DeclarePlugin


@DeclarePlugin('inband_diagnostics', 100)
class InBandDiagnostics(Diagnostics):
    """This class controls launching the inband diagnostic tests
    This needs the input of a file """
    MOCK_PROVISION = False

    def __init__(self, **kwargs):
        Diagnostics.__init__(self, **kwargs)
        self.reboot_true = False
        self.img = kwargs['diag_image']
        self.old_image = None
        self.kargs = kwargs['test_name']
        if "DiagReboot=yes" not in self.kargs:
            self.kargs += ' DiagReboot=no'
        else:
            self.reboot_true = True
        self.kargs = "console=ttyS0,115200n1 " + self.kargs
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
        self.old_image = self.device.get("provisioner_bootstrap")
        self.old_kargs = self.device.get("provisioner_kernel_args")

        if self.MOCK_PROVISION is True:
            self.provisioner.add(self.device)
            self.provisioner.set_bootstrap(self.device, img)

        try:
            device_list = self.provisioner.list()
        except Exception as ex:
            raise Exception("Error: Failed to read data from provisioner because {0}. No tests will be "
                            "run.".format(str(ex)))

        if device not in device_list:
            raise Exception("Error: Device does not exist in provisioner, provision device to continue")
        else:
            self.old_image = self.device.get("provisioner_bootstrap")
            self.old_kargs = self.device.get("provisioner_kernel_args")

    def _provision_image(self, img, args):
        try:
            self.provisioner.set_bootstrap(self.device, img)
            self.provisioner.set_kernel_args(self.device, args)
        except Exception as ex:
            raise Exception("Failed to set image {0} or test {1}. Provisioner returned error {2}. "
                            "Cannot run diagnostics. ".format(img, args, ex.message))
        mac_address = self.device.get("mac_address")
        self._edit_boot_parameters(mac_address)

    def _edit_boot_parameters(self, mac_address):
        mac_addr = mac_address.replace(':', '-')
        bootstrap_config_fullpath = "/var/lib/tftpboot/warewulf/pxelinux.cfg/01-" + mac_addr
        file_d = open(bootstrap_config_fullpath, 'r')
        fd_content = file_d.read()
        if 'DiagList' in fd_content:
            self._edit_boot_params(bootstrap_config_fullpath)
        return

    @staticmethod
    def _edit_boot_params(bootstrap_config_fullpath):
        """ Editing the /var//lib/tftpboot/warewulf/pxelinux.cfg/01-<mac-address> file to work
        with specific diag image """
        file_d = open(bootstrap_config_fullpath, 'r')
        fd_content = file_d.read()
        fd_content = re.sub(r"ro initrd=bootstrap/[0-9]+/initfs.gz", r'', fd_content)
        file_d.close()
        file_d = open(bootstrap_config_fullpath, 'w+')
        file_d.write(fd_content)
        file_d.flush()
        os.fsync(file_d.fileno())
        file_d.close()
        return

    def _set_node_state(self, state):
        result = self.power_manager.set_device_power_state(state)
        if result[self.device_name] is not True:
            raise Exception("Failed to power {0} node during provisioning diagnostic image. No tests will "
                            "be run.".format(state))

    def _console_log_calling(self, bmc_ip_address, bmc_user, bmc_password, queue_var):
        try:
            self.console_log = IpmiConsoleLog(self.device_name, bmc_ip_address, bmc_user, bmc_password)
            consolelines, result_line = self.console_log.start_log_capture('End of Diagnostics',
                                                                           'Final Diagnostic Results')
            queue_var.put(result_line)
        except Exception as ex:
            raise Exception('Unable to connect to the bmc, update the config file for device {0} and try again. Error '
                            'received from console log: {1}'.format(self.device_name, str(ex)))
        return

    def launch_diags(self, device, bmc):
        """launches the diagnostic tests"""
        self.device = device
        self.bmc = bmc
        bmc_ip_address = self.bmc.get("ip_address")
        bmc_user = self.bmc.get("user")
        bmc_password = self.bmc.get("password")
        self.device_name = self.device.get("hostname")
        result_list = dict()
        result_queue = queue.Queue()

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
        console_log_thread = Thread(target=self._console_log_calling, args=[bmc_ip_address, bmc_user, bmc_password, result_queue])
        console_log_thread.start()
        # Step 2: Provision diagnostic image
        self._provision_image(self.img, self.kargs)
        self._set_node_state('Off')
        self._set_node_state('On')
        console_log_thread.join()
        if not result_queue.empty():
            result_list[self.device_name] = result_queue.get()
        else:
            raise Exception('Console log failed to receive data, diagnostics did not complete and the node will be in '
                            'bad state')
        # Step 3: Provision node back to old image
        if not self.reboot_true:
            self._provision_image(self.old_image, self.old_kargs)
            self._set_node_state('Off')
            self._set_node_state('On')
        # Step 4: Add node back to resource pool
        result = self.resource_manager.add_nodes_to_resource_pool(dev_l)
        if result[0] != 0:
            raise Exception("Failed to add node back to resource pool")

        return "Diagnostics completed on node {0} with {1}".format(self.device_name, result_list[self.device_name])

    def _pack_options(self):
        """Return the node power control options based on the node_name and
                   configuration object."""
        options = {}
        dev_l = list()
        self.device['access_type'] = 'mock'
        dev_l.append(self.device)
        options['device_list'] = dev_l
        options['bmc_list'] = [self.bmc]
        options['plugin_manager'] = self.plugin_manager
        return options
