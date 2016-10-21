"""
TBD
"""
from ctrl.commands import Command, CommandResult


class PowerRebootCommand(Command):
    """Power reboot command"""

    def __init__(self, node_name, args=None):
        """Retrieve dependencies and prepare for power reboot"""
        super(PowerRebootCommand, self).__init__(node_name, args)

        self.node_name = node_name
        self.args = args

    def execute(self):
        """Execute the command"""
        return CommandResult(0, "Success: Power Reboot {}".format(self.node_name))
