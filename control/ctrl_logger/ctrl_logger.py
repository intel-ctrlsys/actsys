# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
    Support for logging.
"""
import logging
import logging.handlers
import os
import re

JOURNAL = 35


class CtrlFormatter(logging.Formatter):
    """Special formatter to change depending of the log level, for now just
       Journal is different"""
    _format = '%(asctime)s %(levelname)-8s %(name)-6s: %(message)s'
    _journal_format = '%(asctime)s %(levelname)-8s %(name)-6s: %(cmd)s '\
                      '%(device)s, %(message)s'

    def format(self, record):
        """Helps to use a different format depending on log level"""
        if record.levelno == JOURNAL:
            self._fmt = self._journal_format
        else:
            self._fmt = self._format

        return super(CtrlFormatter, self).format(record)


class CtrlLogger(logging.getLoggerClass()):
    """Extended class of python logging module."""

    FORMAT = "%(asctime)s %(levelname)-8s %(name)-6s: %(message)s"
    LOG_FILE = os.path.expanduser('~/ctrl.log')

    def __init__(self, name=None, level=logging.NOTSET):
        super(CtrlLogger, self).__init__(name, level)
        logging.addLevelName(JOURNAL, "JOURNAL")

    def info(self, log_msg, *args, **kwargs):
        """Confirmation that things are working as expected."""
        if isinstance(log_msg, list):
            for msg in log_msg:
                super(CtrlLogger, self).info(msg)
        else:
            super(CtrlLogger, self).info(log_msg, *args, **kwargs)

    def debug(self, log_msg, *args, **kwargs):
        """Detailed information, typically of interest only when diagnosing
           problems."""
        if isinstance(log_msg, list):
            for msg in log_msg:
                super(CtrlLogger, self).debug(msg)
        else:
            super(CtrlLogger, self).debug(log_msg, *args, **kwargs)

    def warning(self, log_msg, *args, **kwargs):
        """An indication that something unexpected happened, or indicative of
           some problem in the near future. The software is still working as
           expected."""
        if isinstance(log_msg, list):
            for msg in log_msg:
                super(CtrlLogger, self).warning(msg)
        else:
            super(CtrlLogger, self).warning(log_msg, *args, **kwargs)

    def critical(self, log_msg, *args, **kwargs):
        """A serious problem, indication that the program itself may be unable
           to continue."""
        if isinstance(log_msg, list):
            for msg in log_msg:
                super(CtrlLogger, self).critical(msg)
        else:
            super(CtrlLogger, self).critical(log_msg, *args, **kwargs)

    def error(self, log_msg, *args, **kwargs):
        """Due to a more serious problem, the software has not been able to
           perform some function."""
        if isinstance(log_msg, list):
            for msg in log_msg:
                super(CtrlLogger, self).error(msg)
        else:
            super(CtrlLogger, self).error(log_msg, *args, **kwargs)

    def journal(self, command, command_result=None):
        """ Logs the user's transactions, where transaction is the command
            isued by the user"""
        start_msg = "Job Started"
        cmd_name = format_cmd_name(command.get_name())
        journal_args = {
            'cmd' : cmd_name,
            'device' : command.device_name,
            'cmdargs' : ''.join(command.command_args)
        }

        msg = start_msg if command_result is None else command_result.message
        super(CtrlLogger, self).log(JOURNAL, msg, extra=journal_args)

def format_cmd_name(cmd_name):
    """Format the command name"""
    cmd_name = re.sub("Command", "", cmd_name)
    cmd_name = re.sub(r"(\w)([A-Z])", r"\1 \2", cmd_name)
    cmd_name = cmd_name.lower()
    return cmd_name

def add_file_handler(logger):
    """Send the logs to a log file with the format specified"""
    handler = logging.handlers.RotatingFileHandler(CtrlLogger.LOG_FILE)
    handler.setLevel(logging.INFO)
    handler.setFormatter(CtrlFormatter())
    logger.addHandler(handler)


def get_ctrl_logger():
    """Returns a ctrl logger, all calls to this function will return the same
       instance"""
    logging.setLoggerClass(CtrlLogger)
    logger = logging.getLogger("ctrl")

    if not logger.handlers:
        add_file_handler(logger)
        logger.setLevel(logging.INFO)

    return logger