"""
Test the Command and CommandResult.
"""
import unittest
from ctrl.commands import Command, CommandResult


class TestCommandResult(unittest.TestCase):
    """Test case for the RemoteSshPlugin class."""

    def setUp(self):
        self.result = 0
        self.message = "The strangest return message ever.!/@3<>-+="
        self.command_result = CommandResult(self.result, self.message)

    def test_str(self):
        """Stub test, please update me"""

        self.assertEqual(self.command_result.__str__(), "%i - %s".format(self.result, self.message))


def concreter(abclass):
    """
    From Stack overflow: http://stackoverflow.com/a/37574495/1767377 AND http://stackoverflow.com/a/9759329/1767377

    >>> import abc
    >>> class Abstract(metaclass=abc.ABCMeta):
    ...     @abc.abstractmethod
    ...     def bar(self):
    ...        return None

    >>> c = concreter(Abstract)
    >>> c.__name__
    'dummy_concrete_Abstract'
    >>> c().bar() # doctest: +ELLIPSIS
    (<abc_utils.Abstract object at 0x...>, (), {})
    """
    class concreteCls(abclass):
        pass

    concreteCls.__abstractmethods__ = frozenset()
    return type('DummyConcrete' + abclass.__name__, (concreteCls,), {})


class TestCommand(unittest.TestCase):
    def test(self):
        self.instance = concreter(Command)("node_name")
        self.instance.execute()


if __name__ == '__main__':
    unittest.main()
