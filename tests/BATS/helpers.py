# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
    High Level OS Utilities for Validation.
"""
import subprocess
import os


def execute_without_capture(command):
    """Execute a command list suppressing output and returning the return
       code."""
    file_desc = open(os.devnull)
    result = subprocess.call(command, stderr=file_desc, stdout=file_desc)
    file_desc.close()
    return result


def execute_with_capture(command):
    """
    Execute a command list capturing output and returning the stdout,
    stderr or None, None
    """
    pipe = subprocess.Popen(command, stdout=subprocess.PIPE)
    out = pipe.communicate()
    if pipe.returncode == 0:
        return out[0], out[1]
    else:
        return None, None
