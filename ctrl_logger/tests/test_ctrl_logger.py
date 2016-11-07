# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Tests for the CrtlLogger class
"""
import unittest
from ctrl.ctrl_logger.ctrl_logger import CtrlLogger


class TestCtrlLogger(unittest.TestCase):
    """Tests for logging functionality"""
    def test_ctrl_logger(self):
        """All Tests."""
        log = CtrlLogger()
        log.info("Dummy info message")
        log.warning("Dummy warning message")
        log.debug("Dummy debug message")
        log.error("Dummy error message")
        log.critical("Dummy critical message")


if __name__ == '__main__':
    unittest.main()
