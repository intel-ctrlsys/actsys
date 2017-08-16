# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""Ipmi Console log redirection plugin"""
from threading import Thread
from subprocess import Popen, PIPE, STDOUT
from datastore import get_logger
from control.plugin import DeclarePlugin
from control.utilities import Utilities


@DeclarePlugin('ipmi_console_log', 100)
class IpmiConsoleLog(object):
    """This class implements the console log plugin via IPMI"""
    def __init__(self, node_name, bmc_address, user_name, password):
        self.node_name = node_name
        self.bmc_address = bmc_address
        self.user_name = user_name
        self.password = password
        self.utilities = Utilities()
        self.logger = get_logger()
        self.cmd = 'IPMI_console_log'
        self.consolelog = None
        self.stop_line = None

    def start_log_capture(self, stop_line):
        """Start capturing console"""
        console_lines = []
        self.stop_line = stop_line
        try:
            self.consolelog = Popen(['ipmiutil', 'sol', '-a', '-N', self.bmc_address, '-U', self.user_name, '-P',
                                     self.password, '-o', '/tmp/output'], stdout=PIPE, stderr=STDOUT, stdin=PIPE)
        except Exception as ex:  # Catching all Exceptions as Popen or IPMI could fail with some unknow exceptions
            self.logger.debug("Could not activate IPMI sol on BMC. Console logs will not be collected\n Received Error:"
                              + ex.message, self.node_name)

        while self.consolelog.poll() is None:
            buffer_v = self.consolelog.stdout.readline()
            length_buff = len(buffer_v)
            if length_buff > 0:
                line = buffer_v.decode(errors='ignore').strip('\n')
                if self.stop_line in line:
                    self.stop_log_capture()
                else:
                    console_lines.append(line)
        self.consolelog.wait()
        self.consolelog = None
        try:
            log_capture_thread = Thread(target=self._write_to_datastore(console_lines))
            log_capture_thread.start()
        except Exception as ex:  # catching all Exceptions as threads could fail with some unknown exceptions
            self.logger.debug("Unable to create new thread. Console logs "
                              "will not be collected\n Received Error:"
                              + ex.message, self.node_name)
        return console_lines

    def stop_log_capture(self):
        """Stop capture"""
        self.consolelog.terminate()

    def _write_to_datastore(self, raw_data):
        """Write logs to datastore"""
        self.logger.journal(self.cmd, None, self.node_name, raw_data)
