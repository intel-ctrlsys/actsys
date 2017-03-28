# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Implements a provisioner that does nothing expect return stock values...
"""
from ..plugin import DeclarePlugin
from .provisioner import Provisioner, ProvisionerException
import json

@DeclarePlugin('mock', 100)
class MockProvisioner(Provisioner):
    """
    The MockProvisioner does nothing except return the same values every time.
    """

    def __init__(self, options=None):
        """
        Construct the obj, nothing more.
        """
        if options is not None and options.get("file") is not None:
            self.provisioner_file_location = options.get("file")
            with open(self.provisioner_file_location) as f:
                self.parsed_file = json.load(f)
        else:
            self.parsed_file = {}

    def add(self, device):
        """
        See @Provisioner for interface details. Implementation here.
        """
        print(self.parsed_file)
        if self.parsed_file.get("devices") is None:
            self.parsed_file["devices"] = set()

        self.parsed_file["devices"].add(device.get("hostname"))

        device[self.DEVICE_ADDED_TO_PROVISIONER_KEY] = True
        return device

    def delete(self, device):
        """
        See @Provisioner for interface details. Implementation here.
        """
        if self.parsed_file.get("devices") is None:
            self.parsed_file["devices"] = set()

        self.parsed_file["devices"].discard(device.get("hostname"))

        device.pop(self.DEVICE_ADDED_TO_PROVISIONER_KEY, None)
        return device

    def set_ip_address(self, device, ip_address, interface="eth0"):
        """
        See @Provisioner for interface details. Implementation here.
        """
        key = "ip_address"
        if device.get("default_network_interface", "eth0") != interface:
            key = "{}_{}".format(interface, key)

        if ip_address is None:
            device.pop(key, None)
        else:
            device[key] = ip_address

        return device

    def set_hardware_address(self, device, hardware_address, interface="eth0"):
        """
        See @Provisioner for interface details. Implementation here.
        """
        key = "mac_address"
        if device.get("default_network_interface", "eth0") != interface:
            key = "{}_{}".format(interface, key)

        if hardware_address is None:
            device.pop(key, None)
        else:
            device[key] = hardware_address

        return device

    def set_image(self, device, image):
        """
        See @Provisioner for interface details. Implementation here.

        This mock provisioner allows any image name, except things that begin with 1. This rules is put in place so that
        we have a method to raise ProvisionerException's per the provisioner interface. In other words, images that
        start with '1' are not found by the provisioner and thus, cannot be added.
        """
        if str(image)[0] == '1':
            raise ProvisionerException("Image {} does not exists in provisioner, "
                                       "cannot set the device to it.".format(image))

        if self.parsed_file.get("images") is None:
            self.parsed_file["images"] = set()

        if image is None:
            device.pop(self.PROVISIONER_IMAGE_KEY, None)
        else:
            device[self.PROVISIONER_IMAGE_KEY] = image
            self.parsed_file["images"].add(image)
        return device

    def set_bootstrap(self, device, bootstrap):
        """
        See @Provisioner for interface details. Implementation here.
        """
        if bootstrap is None:
            device.pop(self.PROVISIONER_BOOTSTRAP_KEY, None)
        else:
            device[self.PROVISIONER_BOOTSTRAP_KEY] = bootstrap
        return device

    def set_files(self, device, files):
        """
        See @Provisioner for interface details. Implementation here.
        """
        if files is None:
            device.pop(self.PROVISIONER_FILE_KEY, None)
        else:
            device[self.PROVISIONER_FILE_KEY] = files
        return device

    def add_file(self, src_file_location, dst_file_location=None):
        """
        See @Provisioner for interface details. Implementation here.
        """
        if dst_file_location is None:
            dst_file_location = src_file_location
        pass

    def set_kernel_args(self, device, args):
        """
        See @Provisioner for interface details. Implementation here.
        """
        if args is None:
            device.pop(self.PROVISIONER_KARGS_KEY, None)
        else:
            device[self.PROVISIONER_KARGS_KEY] = args
        return device

    def list(self):
        """
        See @Provisioner for interface details. Implementation here.
        """
        return sorted(self.parsed_file.get("devices"))

    def list_images(self):
        """
        See @Provisioner for interface details. Implementation here.
        """
        return sorted(self.parsed_file.get("images"))
