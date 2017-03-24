# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Implements a bios control plugin to flash bios/change bios settings
on compute nodes
"""
import os
import json
import tempfile
from ...plugin import DeclarePlugin
from ..bios_control import BiosControl


@DeclarePlugin('mock', 1000)
class MockNC(BiosControl):
    "Mock class"
    def __init__(self, args=None):
        """Constructor that creates an utility and gets configuration"""
        BiosControl.__init__(self, args)
        self.__current_image_list = {}
        self.__persistent_file = os.path.sep + os.path.join(tempfile.gettempdir(), 'bios_file')
        if os.path.exists(self.__persistent_file):
            self._load_bios_file()

    def get_version(self, device, bmc):
        """Bios version"""
        node_name = device.get('device_name')
        if node_name in self.__current_image_list:
            return self.__current_image_list[node_name]
        else:
            return 'No image found on node {0}'.format(node_name)

    def bios_update(self, device, bmc, image):
        """Update Bios"""
        node_name = device.get('device_name')
        self.__current_image_list[node_name] = image
        self._save_bios_file()
        return "Bios for {0} updated with {1}".format(node_name, image)

    def _load_bios_file(self):
        """Loads the bios image file from disk."""
        file_obj = open(self.__persistent_file, 'r')
        self.__current_image_list = json.load(file_obj)
        file_obj.close()

    def _save_bios_file(self):
        """Saves the bios image file to disk."""
        file_obj = open(self.__persistent_file, 'w')
        json.dump(self.__current_image_list, file_obj)
        file_obj.close()
