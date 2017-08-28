# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""cmm.__main__: executed when bootstrap directory is called as script."""

from sys import exit
from .shell import start_ipython_shell

if __name__ == "__main__":
    ret_val = start_ipython_shell()
    exit(ret_val)
