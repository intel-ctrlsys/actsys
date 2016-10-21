"""
TBD
"""
from ctrl.commands import Command, CommandResult


class ResourcePoolAddCommand(Command):
    """ResourcePoolAddCommand"""

    def __init__(self, node_name, args=None):
        """Retrieve dependencies and prepare for power on"""
        super(ResourcePoolAddCommand, self).__init__(node_name, args)

        self.node_name = node_name
        self.args = args

    def execute(self):
        """Execute the command"""
        return CommandResult(0, "Success: Resource Pool Add {}".format(self.node_name))
