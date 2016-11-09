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

if __name__ == '__main__':
    # If we are running this as a cli file, then edit the path to
    # contain the directory the file is in.
    if __package__ is None:
        import sys
        from os import path

        sys.path.append(path.dirname(path.dirname(path.realpath(__file__))))

    from cli.control_cli import CtrlCliExecutor

    CtrlCliExecutor.execute_cli_cmd()
