# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""cmm.__main__: executed when bootstrap directory is called as script."""

import sys
from sys import exit
from .shell import start_ipython_shell

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ret_val = start_ipython_shell(sys.argv[1])
    else:
        ret_val = start_ipython_shell()
    exit(ret_val)
