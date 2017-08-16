"""
Installation script for the NC REST API server application
"""

from setuptools import setup
from setuptools import find_packages


setup(name="oob_rest_server",
      version="0.1.0",
      packages=find_packages(),
      install_requires=['cherrypy'],
      entry_points={'console_scripts': ['oob-rest=app.__main__:main']},
      author="Jonathan Smith",
      author_email="jonathan.d.smith@intel.com",
      description="REST API server for server board OOB operations")
