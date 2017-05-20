# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
The DataStore Module
"""
from .datastore import DataStore, DataStoreException, DataStoreLogger, get_logger, add_stream_logger
from .datastore_builder import DataStoreBuilder
from .datastore_cli import DataStoreCLI
from .utilities import DeviceUtilities
