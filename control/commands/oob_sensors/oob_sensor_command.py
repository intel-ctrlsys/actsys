# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#

from .. import Command


class OobSensorCommand(Command):
    """Oob Sensor Command"""

    def __init__(self, device_name, configuration, plugin_manager, logger=None, **kwargs):
        Command.__init__(self, device_name, configuration, plugin_manager, logger, **kwargs)
        self.oob_sensor_plugin = None
        self.plugin_name = None
        self.device_data = None
        self.bmc_data = None

    def setup(self):
        cfg = self.configuration
        node = cfg.get_device(self.device_name)
        if node.get("device_type") not in ['node', 'compute', 'service']:
            raise RuntimeError('Sensor values can not be read for a non-node type '
                               'device!')
        self.device_data = node
        self.bmc_data = cfg.get_device(node.get("bmc"))
        self.plugin_name = node.get("oob_sensor", 'mock')
        return None

    def print_table(self, ret_msg):
        result = ""
        for key, value in ret_msg.iteritems():
            key1 = (key[:30] + '..') if len(key) > 30 else key
            values = list()
            for i_value in value:
                value1 = round(i_value, 5) if len(str(i_value)) > 5 else i_value
                values.append(value1)
            result += "\t\t{:40}{:^15}\n".format(key1, self.print_multiline(values)) + self.print_table_border('', '')
        return result

    @staticmethod
    def print_table_border(row, column, device_name=None):
        if device_name is None:
            result = '\t{:-^40} {:-^80}\n'.format(row, column)
        else:
            result = '\n Device: {0}\n\n'.format(device_name) + '\t{:^40} {:^40}\n'.format(row, column)
        return result

    @staticmethod
    def print_multiline(value):
        list_split = [value[x:x + 10] for x in xrange(0, len(value), 10)]
        result = ''
        for xs in list_split:
            result += ' '.join(map(str, xs)) + "\n\n{:40}{:15}".format("", "")
        return result