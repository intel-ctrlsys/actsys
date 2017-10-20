# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""OOB sensors command class"""
from ..command import Command

class OobSensorCommand(Command):
    """Oob Sensor Command"""

    def __init__(self, device_name, configuration, plugin_manager, logger=None, **kwargs):
        Command.__init__(self, device_name, configuration, plugin_manager, logger, **kwargs)
        self.oob_sensor_plugin = None
        self.plugin_name = None
        self.device_data = []
        self.bmc_data = []

    def setup(self):
        """Setup function for OOB sensors"""
        for device in self.device_name:
            node = self.configuration.get_device(device)
            if node.get("device_type") not in ['node', 'compute', 'service']:
                raise RuntimeError('Sensor values can not be read for a non-node type '
                                   'device!')
            self.device_data.append(node)
            self.bmc_data.append(self.configuration.get_device(node.get("bmc")))
        self.plugin_name = self.bmc_data[0].get("access_type", None)
        if self.plugin_name is None:
            raise RuntimeError("No BMC access_type specified in the configuration file. Cannot perform action")
        self.oob_sensor_plugin = self.plugin_manager.create_instance('bmc', self.plugin_name)

    def print_table(self, ret_msg):
        """print the output in table format"""
        result = ""
        for key, value in ret_msg.items():
            length = len(key)
            key1 = (key[:30] + '..') if length > 30 else key
            values = list()
            for i_value in value:
                length_str = len(str(i_value))
                value1 = round(i_value, 5) if length_str > 5 and type(i_value) == float else i_value
                values.append(value1)
            result += "\t\t{:40}{:^15}\n".format(key1, self.print_multiline(values)) + self.print_table_border('', '')
        return result

    @staticmethod
    def get_sensor_name(sensor_name):
        """Get sensor name"""
        sensor_name_length = len(sensor_name)
        if sensor_name == ' ' or sensor_name_length == 0:
            raise RuntimeError("Empty string given to sensor_name")
        elif sensor_name.strip().lower() in ['all', '.*']:
            return ''
        else:
            return sensor_name

    @staticmethod
    def print_table_border(row, column, device_name=None, sensor_name=None):
        """Print table border"""
        if device_name is None:
            result = '\t{:-^40} {:-^80}\n'.format(row, column)
        else:
            result = '\n Device: {0}\n\n'.format(device_name) + '\n\t Sensor: {0}\n\n'.format(sensor_name) + '\t{:^40}'' \
            ''{:^40}\n'.format(row, column)
        return result

    @staticmethod
    def print_multiline(value):
        """Print multiple lines"""
        list_split = [value[x:x + 10] for x in range(0, len(value), 10)]
        result = ''
        for row in list_split:
            result += ' '.join(map(str, row)) + "\n\n{:40}{:15}".format("", "")
        return result
