# -*- coding: utf-8 -*-
# !/usr/bin/env python
#
# Copyright (c) 2016      Intel Corporation.  All rights reserved.
#
# $COPYRIGHT$
#
# Additional copyrights may follow
#
# $HEADER$
#
"""
Main Module to call Control CLI.
"""


from cli.control_cli import CtrlCliExecutor

if __name__ == '__main__':
    CtrlCliExecutor.execute_cli_cmd()
