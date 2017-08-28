# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
import sys
from IPython import get_ipython, start_ipython
from traitlets.config.loader import Config
from .magics import ShellCommands
from datastore import DataStoreBuilder


def start_ipython_shell(datastore_connection='/tmp/cmm'):
    cfg = Config()
    cfg.IPCompleter.merge_completions = False
    cfg.InteractiveShellApp.exec_lines = ['from cmm.shell import register_magics\n',
                                          'register_magics("{}")\n'.format(datastore_connection)]
    cfg.TerminalInteractiveShell.banner1 = '\x1b[2J\x1b[H\n' \
                                           '*************************************************************\n' \
                                           'Configuration Manifest Management (CMM)'
    cfg.TerminalInteractiveShell.banner2 = '\n\n'
    start_ipython(argv=[], config=cfg)


def register_magics(datastore_connection: str):
    datastore = DataStoreBuilder.get_datastore_from_string(datastore_connection, 50)
    try:
        IPYTHON_ID = get_ipython()
        MAGICS = ShellCommands(IPYTHON_ID, datastore)
        IPYTHON_ID.register_magics(MAGICS)
        cmm_in_argv_list_index_place = 0
        try:
            cmm_in_argv_list_index_place = sys.argv.index("cmm")
        except ValueError:
            # cmm is not found in the argv list, no big deal.
            pass

        if sys.argv[cmm_in_argv_list_index_place + 1:]:
            print((sys.argv[cmm_in_argv_list_index_place + 1:]))
            runnable_function = getattr(MAGICS, sys.argv[cmm_in_argv_list_index_place + 1], None)
            if runnable_function:
                runnable_function(' '.join(sys.argv[cmm_in_argv_list_index_place + 2:]))
                sys.exit(0)
            else:
                print("Detected extra args on the command line, but couldn't determine how to parse them.")
        else:
            MAGICS.view(None)
    except AttributeError as ae:
        print("Failed to start up CMM due to the following error:")
        print(ae)
        return 1
