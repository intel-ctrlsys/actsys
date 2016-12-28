# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#

"""control.__main__: executed when bootstrap directory is called as script."""

from .cli.control_cli import ControlCommandLineInterface


ControlCommandLineInterface().execute_cli_cmd()
