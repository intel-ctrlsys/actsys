# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Setup Module
"""
from setuptools import setup, find_packages

description = "A datastore for exascale clusters"
author = "Intel Corporation"
license = "Apache"
tests_require = ['pytest',
                 'pytest-cov',
                 'pylint',
                 'mock']

setup(name='cmm',
      version='0.2.1',
      description=description,
      author=author,
      license=license,
      packages=find_packages(),
      entry_points={
          'console_scripts': ['cmm = cmm.__main__:main']
      },
      install_requires=['inquirer', 'ipython'],
      test_suite='tests',
      tests_require=tests_require,
      extras_require={
          'testing': tests_require
      })
