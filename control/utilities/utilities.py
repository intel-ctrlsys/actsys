# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Intel Corp.
#
"""
    High Level OS Utilities for Control.
"""
import subprocess
import os
from datastore.datastore import get_logger


class Utilities(object):
    """Class to hold low level system call helpers and mock-able objects."""
    def __init__(self):
        self.logger = get_logger()
        pass

    def execute_no_capture(self, command):
        """
        Execute a command list suppressing output and returning the return
           code. The call is blocking.
        :param command: A list of args to execute (i.e. ['ls', '/home'])
        :return: The return code output by the process completion
        """
        file_desc = open(os.devnull)
        result = subprocess.call(command, stderr=file_desc, stdout=file_desc)
        file_desc.close()
        return result

    def execute_subprocess(self, command):
        """
        Execute a command list capturing output and returning the return
           code, stdout, stderr.
        :param command: A list of args to execute
        """
        self.logger.debug("Attempting command {}".format(command))
        pipe = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = pipe.communicate()
        result = SubprocessOutput(pipe.returncode, stdout, stderr)
        self.logger.debug(result)
        return result

    def execute_in_shell(self, command):
        """
        :param command:
        :return:
        """
        # TODO: This should return A "SubprocessOutput" Object.
        self.logger.debug("Attempting command {}".format(command))
        pipe = subprocess.Popen(command, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, shell=True)
        stdout, stderr = pipe.communicate()
        if pipe.returncode == 0:
            return 0, stdout
        else:
            return 255, None

    def ping_check(self, address):
        """
        Check if a network address has a OS responding to pings.  NOTE: until a
        new plugin framework for network availability is created any address
        starting with '127.' is considered a mocked address and only addresses
        ending in ".1" will return True, all other return False.  This allows
        for black box testing in BATS and functional testing.
        """
        if not address.startswith('127.'):
            options = ['ping', '-c', '1', '-W', '1', '-q']
            result = self.execute_no_capture(options + [address])
        else:
            return address.endswith('.1')
        return result == 0

    @staticmethod
    def print_nested_list(data_list):
        """
        Print a list of list with automatic left alignment. For outer layer
        list, each item is one row; for inner layer list, each item is one
        column. The columns are aligned on the left.
        """
        if data_list is None or len(data_list) == 0:
            return ''
        width = list()
        for column in data_list[0]:
            width.append(len(column))
        for i in range(1, len(data_list)):
            for j in range(0, len(data_list[i])):
                width[j] = max(width[j], len(data_list[i][j]))
        res = ''
        for i in range(0, len(data_list)):
            for j in range(0, len(data_list[i])):
                res += ''.join(data_list[i][j].ljust(width[j] + 2))
            if i != len(data_list) - 1:
                res += os.linesep
        return res

    def remove_duplicates_from_bmc_data(self, bmc_list):
        return [dict(t) for t in set([tuple(bmc.items()) for bmc in bmc_list])]

    def map_devices_to_bmc(self, device_list, bmc_list, func):
        for bmc in bmc_list:
            bmc_device_list = []
            for device in device_list:
                if bmc.get('hostname') == device.get('bmc'):
                    bmc_device_list.append(device)
            func(bmc_device_list, bmc)


class SubprocessOutput(object):

    def __init__(self, return_code, stdout, stderr):
        self.return_code = return_code
        self.stdout = stdout
        self.stderr = stderr

    def __str__(self):
        return "{} - {} - {}".format(self.return_code, self.stdout, self.stderr)
