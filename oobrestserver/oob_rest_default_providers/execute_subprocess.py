# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Intel Corp.
#

import os
import subprocess


class Output(object):
    """Subprocess output class"""
    def __init__(self, command, return_code, stdout, stderr):
        self.command = ' '.join(command)
        self.return_code = return_code
        self.stdout = stdout
        self.stderr = stderr

    def __str__(self):
        template = "command: {} return: {} stdout: {} stderr: {}"
        return template.format(self.command, self.return_code, self.stdout, self.stderr)

def without_capture(command, shell=False):
    with open(os.devnull, 'w') as dev_null:
        code = subprocess.call(command, stderr=dev_null, stdout=dev_null, shell=shell)
        return Output(command, code, None, None)

def with_capture(command, shell=False):
    pipe = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell)
    stdout, stderr = pipe.communicate()
    return Output(command, pipe.returncode, stdout.decode('utf-8'), stderr.decode('utf-8'))

def capture_to_line(command, stop_line, halt_input=None, shell=False):
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE, shell=shell)
    console_lines = []
    while not proc.poll():
        line = str(proc.stdout.readline()).strip('\n')
        console_lines.append(line)
        if stop_line in line:
            if halt_input:
                proc.communicate(input=halt_input, timeout=.1)
            proc.terminate()
    return console_lines
