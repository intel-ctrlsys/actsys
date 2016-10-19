"""
This defines the interface for BMC objects.
"""


class Interface(object):
    """Interface class for bmc classes."""
    def __init__(self, options=None):
        pass

    def get_chassis_state(self, address, username, password):
        """Get the current chassis state for a node."""
        pass

    def set_chassis_state(self, address, username, password, new_state):
        """Set the target chassis state for a node."""
        pass
