from distutils.core import setup

description="A control component for exascale clusters"
author="Intel Corporation"
license="Apache"

setup(name='ctrl',
      version='0.1.0',
      description=description,
      author=author,
      license=license,
      packages=['bmc', 'commands', 'os_remote_access', 'plugin', 'utilities'],
)

