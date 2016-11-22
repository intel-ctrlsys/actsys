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

    FORMAT = "%(asctime)s %(levelname)-8s %(name)-6s: %(message)s"
    LOG_FILE = "/var/log/actsys.log"

    def __init__(self, name=None, level=logging.NOTSET):
        super(CtrlLogger, self).__init__(name, level)

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

    def journal(self, command, command_result):
        """ Logs the user's transactions, where transaction is the command
            isued by the user"""
        pass

def add_file_handler(logger):
    """Send the logs to a log file with the format specified"""
    handler = logging.handlers.RotatingFileHandler(CtrlLogger.LOG_FILE)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(CtrlLogger.FORMAT)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def get_ctrl_logger():
    """Returns a ctrl logger, all calls to this function will return the same
       instance"""
    logging.setLoggerClass(CtrlLogger)
    logger = logging.getLogger("actsys")

    if not logger.handlers:
        add_file_handler(logger)
        logger.setLevel(logging.INFO)

    return logger
