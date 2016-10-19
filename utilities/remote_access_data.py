"""
Class used to hold username, password, address, and port for remote access.
"""


class RemoteAccessData(object):
    """Class to store common data for remote OS access."""
    def __init__(self, address, port, user, identifier):
        self.address = address
        self.port = port
        self.username = user
        self.identifier = identifier

    def get_authority(self):
        """Return the network authority for this object."""
        return '{}:{}'.format(self.address, self.port)

    def get_credentials(self):
        """Return the username:identifier for this object."""
        return '{}:{}'.format(self.username, self.identifier)
