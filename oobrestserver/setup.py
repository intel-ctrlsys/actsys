"""
Installation script for the NC REST API server application
"""

from setuptools import setup
from setuptools import find_packages


setup(name="bky-rest",
      version="0.3.0",
      packages=find_packages(),
      install_requires=['cherrypy'],
      entry_points={'console_scripts': ['bky-rest=oobrestserver.__main__:main']},
      author="Jonathan Smith",
      author_email="jonathan.d.smith@intel.com",
      description="REST API server for server board OOB operations")
