"""
Installation script for the NC REST Client API Wrapper
"""

from setuptools import setup

setup(name="oob_rest_client",
      version="0.3.0",
      packages=['oobrestclient'],
      install_requires=['requests'],
      author="Jonathan Smith",
      author_email="jonathan.d.smith@intel.com",
      description="Mock REST API client for BKY board OOB operations")
