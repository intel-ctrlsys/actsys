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
from ..console_log import ConsoleLog


@DeclarePlugin('ipmi_console_log', 100)
class IpmiConsoleLog(ConsoleLog):
    """This class implements the console log plugin via IPMI"""
    def __init__(self, **kwargs):
        ConsoleLog.__init__(self, kwargs)
        self.node_name = kwargs['node_name']
        self.bmc_address = kwargs['bmc_ip_address']
        self.user_name = kwargs['bmc_user']
        self.password = kwargs['bmc_password']
        self.utilities = Utilities()
        self.logger = get_logger()
        self.cmd = 'IPMI_console_log'
        self.consolelog = None
        self.stop_line = None
        self.result_line = None

    def start_log_capture(self, stop_line, result_line):
        """Start capturing console"""
        console_lines = []
        self.stop_line = stop_line
        self.result_line = result_line
        result = []
        try:
            self.consolelog = Popen(['tail', '-f', '/tmp/InputForAdapterProvisioner1.log'], stdout=PIPE, stderr=STDOUT, stdin=PIPE)
        except Exception as ex:  # Catching all Exceptions as Popen or IPMI could fail with some unknow exceptions
            self.logger.debug("Could not activate IPMI sol on BMC. Console logs will not be collected\n Received Error:"
                              + str(ex), self.node_name)

        result_found = False
        while self.consolelog.poll() is None:
            buffer_v = self.consolelog.stdout.readline()
            length_buff = len(buffer_v)
            if length_buff > 0:
                line = buffer_v.decode(errors='ignore').strip('\n')
                if self.result_line in line:
                    result_found = True
                elif self.stop_line in line:
                    self.stop_log_capture()
                else:
                    console_lines.append(line)
                if result_found == True:
                    result.append(line)
        self.consolelog.wait()
        self.consolelog = None
        try:
            log_capture_thread = Thread(target=self._write_to_datastore(console_lines))
            log_capture_thread.start()
        except Exception as ex:  # catching all Exceptions as threads could fail with some unknown exceptions
            self.logger.debug("Unable to create new thread. Console logs "
                              "will not be collected\n Received Error:"
                              + str(ex), self.node_name)

        return console_lines, result

    def stop_log_capture(self):
        """Stop capture"""
        self.consolelog.terminate()

    def _write_to_datastore(self, raw_data):
        """Write logs to datastore"""
        self.logger.journal(self.cmd, None, self.node_name, raw_data)
