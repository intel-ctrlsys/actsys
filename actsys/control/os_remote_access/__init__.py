# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Remote OS access module.
"""
from .mock.os_remote_access import OsRemoteAccessMock
from .telnet.telnet import RemoteTelnetPlugin
from .ssh.ssh import RemoteSshPlugin
from .parallel_ssh.parallel_ssh import ParallelSshPlugin
