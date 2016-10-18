"""
Defines the interface for remote OS access execution of processes.
"""


class Interface(object):
    """Interface for remote process execution."""
    def __init__(self, options=None):
        pass

    def execute(self, cmd, remote_access_data, capture=False, other=None):
        """Using address and credentials, execute the cmd remotely."""
        pass
