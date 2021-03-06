# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Interface for all resource control plugins.
"""
from abc import ABCMeta, abstractmethod
from ..plugin import DeclareFramework


@DeclareFramework('provisioner')
class Provisioner(object, metaclass=ABCMeta):
    PROVISIONER_KEY = "provisioner"
    PROVISIONER_IMAGE_KEY = "image"
    PROVISIONER_BOOTSTRAP_KEY = "provisioner_bootstrap"
    PROVISIONER_FILE_KEY = "provisioner_files"
    PROVISIONER_KARGS_KEY = "provisioner_kernel_args"
    PROVISIONER_UNSET_KEY = "UNDEF"


    @abstractmethod
    def add(self, device):
        """
        Attempts to add a device to the provisioner. Does nothing if the device is already added.
        :param device:
        :return: Updated device with the new fields applied
        """
        pass

    @abstractmethod
    def delete(self, device):
        """
        Attempts to remove a device from the provisioner. Does nothing if the device isn't already there.
        :param device:
        :return: Updated device with the correct fields removed
        """
        pass

    @abstractmethod
    def set_ip_address(self, device, ip_address, interface="eth0"):
        """
        Mutate the device to include this ip_address.
        Save it to the DataStore
        And set it in the provisioner
        :param device:
        :param ip_address:
        :param interface:
        :return: Updated device with the new fields applied
        """
        pass

    @abstractmethod
    def set_hardware_address(self, device, hardware_address, interface="eth0"):
        """
        Same as Provisioner.set_ip_address
        :param device:
        :param hardware_address:
        :param interface:
        :return: Updated device with the new fields applied
        """
        pass

    @abstractmethod
    def set_image(self, device, image):
        """
        Set an image (already known by the provisioner) to a given device.
        :param device:
        :param image:
        :param kernel:
        :param network_interface:
        :return: Updated device with the new fields applied
        :raise: ProvisionException, the image specified is not known to the provisioner
        """
        pass

    @abstractmethod
    def set_bootstrap(self, device, bootstrap):
        """

        :param device:
        :param bootstrap:
        :return: Updated device with the new fields applied
        :raise: ProvisionException, the bootstrap specified is not known to the provisioner
        """
        pass

    @abstractmethod
    def set_files(self, device, files):
        """

        :param device:
        :param files:
        :return: Updated device with the new fields applied
        :raise: ProvisionException, the file(s) specified is not known to the provisioner
        """
        pass

    @abstractmethod
    def set_kernel_args(self, device, args):
        """

        :param device:
        :param args:
        :return: Updated device with the new fields applied
        """
        pass

    @abstractmethod
    def list(self):
        """
        List all devices that the provisioner knows about.
        does this come the DataStore or Warewulf?
        :return: return the list of device names
        """
        pass

    @abstractmethod
    def list_images(self):
        """
        List all the images this provisioner knows about.
        :return: list of known images (names only)
        """
        pass


class ProvisionerException(Exception):
    """
    A staple Exception thrown by the Provisioner
    """
    def __init__(self, msg, command_output=None):
        super(ProvisionerException, self).__init__()
        self.msg = msg
        if command_output is not None:
            self.cmd_stdout = command_output.stdout
            self.cmd_stderr = command_output.stderr
            self.cmd_return_code = command_output.return_code

    def __str__(self):
        return repr(self.msg)