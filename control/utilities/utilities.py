# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
    High Level OS Utilities for Control.
"""
import subprocess
import os
from ..ctrl_logger.ctrl_logger import get_ctrl_logger


class Utilities(object):
    """Class to hold low level system call helpers and mock-able objects."""
    def __init__(self):
        self.logger = get_ctrl_logger()

    def execute_no_capture(self, command):
        """Execute a command list suppressing output and returning the return
           code."""
        file_desc = open(os.devnull)
        result = subprocess.call(command, stderr=file_desc, stdout=file_desc)
        file_desc.close()
        return result

    def execute_with_capture(self, command):
        """Execute a command list capturing output and returning the return
           code, stdout, stderr"""
        self.logger.debug("Attempting command {}".format(command))
        pipe = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = pipe.communicate()
        if pipe.returncode == 0:
            return stdout, stderr
        else:
            return None, None

    def ping_check(self, address):
        """Check if a network address has a OS responding to pings."""
        options = ['ping', '-c', '1', '-W', '1', '-q']
        result = self.execute_no_capture(options + [address])
        return result == 0