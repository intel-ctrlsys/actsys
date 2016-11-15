#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
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

    CtrlCliExecutor().execute_cli_cmd()
