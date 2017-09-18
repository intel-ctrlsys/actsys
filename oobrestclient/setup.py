# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Installation script for the NC REST Client API Wrapper
"""

from setuptools import setup

setup(name="oobrestclient",
      version="0.3.0",
      packages=['oobrestclient'],
      install_requires=['aiohttp', 'asyncio'],
      author="Intel Corporation",
      description="REST API client for OOB operations")
