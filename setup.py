# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 <company or person>
#
"""
setup.py: For installing via pip
"""

import re
from setuptools import setup, find_packages

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('actsys/actsys.py').read(),
    re.M
).group(1)

setup(
    name="actsys",
    version=version,
    description="A simple python...",
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=[],
    entry_points={
        "console_scripts": ['actsys = actsys.__main__:main']
    },
    test_suite='tests',
    tests_require=['pytest',
                   'pytest-cov',
                   'pylint',
                   'mock']
)
