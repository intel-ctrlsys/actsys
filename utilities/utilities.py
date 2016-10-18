"""
    High Level OS Utilities for Control.
"""
import subprocess
import os


class Utilities(object):
    """Class to hold low level system call helpers and mock-able objects."""
    def __init__(self):
        pass

    def execute_no_capture(self, command):
        """Execute a command list suppressing output and returning the return
           code."""
        file_desc = open(os.devnull)
        result = subprocess.call(command, stderr=file_desc, stdout=file_desc)
        file_desc.close()
        return result

    def execute_with_capture(self, command):
        """Execute a command list capturing output and returning the return
           code, stdout, stderr"""
        pipe = subprocess.Popen(command, stdout=subprocess.PIPE)
        out = pipe.communicate()
        if pipe.returncode == 0:
            return out[0]
        else:
            return None

    def ping_check(self, address):
        """Check if a network address has a OS responding to pings."""
        options = ['ping', '-c', '1', '-W', '1', '-q']
        result = self.execute_no_capture(options + [address])
        return result == 0
