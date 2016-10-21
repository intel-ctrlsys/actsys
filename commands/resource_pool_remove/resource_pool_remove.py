"""
TBD
"""
from ctrl.commands import Command, CommandResult


class ResourcePoolRemoveCommand(Command):
    """ResourcePoolRemoveCommand"""

    def __init__(self, node_name, args=None):
        """Retrieve dependencies and prepare for power on"""
        super(ResourcePoolRemoveCommand, self).__init__(node_name, args)

        self.node_name = node_name
        self.args = args

    def execute(self):
        """Execute the command"""
        return CommandResult(0, "Success: Resource Pool Remove {}".format(self.node_name))
