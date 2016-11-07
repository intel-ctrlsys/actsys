# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
    Support for logging.
"""
import logging
import logging.handlers


class CtrlLogger(logging.getLoggerClass()):
    """Extended class of python logging module."""
    def __init__(self, file_location="/var/log/", log_file_max_bytes=0,
                 retention_period_in_days=0):
        pass

    def info(self, message):
        """Confirmation that things are working as expected."""
        self.root.info(message)

    def debug(self, message):
        """Detailed information, typically of interest only when diagnosing
           problems."""
        self.root.debug(message)

    def warning(self, message):
        """An indication that something unexpected happened, or indicative of
           some problem in the near future. The softwware is still working as
           expected."""
        self.root.warning(message)

    def error(self, message):
        """Due to a more serious problem, the software has not been able to
           perform some function."""
        self.root.error(message)

    def critical(self, message):
        """A serious problem, indication that the program itself may be unable
           to continue."""
        self.root.critical(message)

    def journal(self, command, command_result):
        """ Logs the user's transactions, where transaction is the command
            isued by the user"""
        pass

