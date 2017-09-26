# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Implements a class for collecting console logs over IPMI
"""
from threading import Thread
from control.utilities import Utilities
from control.plugin import DeclarePlugin
from datastore import get_logger

@DeclarePlugin('ipmi_console_log', 100)
class MockConsoleLog(object):
    """The mock plugin doesn nothing except write string to the datastore"""
    def __init__(self, node_name, bmc_address, user_name, password):
        self.node_name = node_name
        self.bmc_address = bmc_address
        self.user_name = user_name
        self.password = password
        self.utilities = Utilities()
        self.logger = get_logger()
        self.log_capture_thread = None
        self.consolelog = None
        self.cmd = "Mock_Console_Log"

    def start_log_capture(self, stop_text, result_text):
        """Start capturing console"""
        self.consolelog = 'HELLO FROM CONSOLE\nEnd of Diagnostics\nReturn Code : 67' + stop_text
        result = result_text + ' 67'
        try:
            log_capture_thread = Thread(target=self._write_to_datastore(self.consolelog))
            log_capture_thread.start()
        except Exception as ex:
            self.logger.debug("Unable to create new thread. Console logs "
                              "will not be collected\n Received Error:"
                              + str(ex), self.node_name)
        self.stop_log_capture()
        return self.consolelog, result


    def stop_log_capture(self):
        """Stop capture"""
        self.consolelog = None
        self._write_to_datastore('Console_log_complete')

    def _write_to_datastore(self, raw_data):
        """Write logs to datastore"""
        self.logger.journal(self.cmd, None, self.node_name, raw_data)
