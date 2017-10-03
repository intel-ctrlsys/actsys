


from unittest import TestCase
from unittest import mock

from oob_rest_default_providers import execute_subprocess
from oob_rest_default_providers.test.FakeSubProcess import FakeSubProcess

class TestExecuteSubprocess(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        mock.patch.stopall()

    def test_with_capture(self):
        output = execute_subprocess.with_capture(['true'])
        self.assertEqual(output.stdout, b'')
        self.assertEqual(output.stderr, b'')
        self.assertEqual(output.command, 'true')
        self.assertEqual(output.return_code, 0)

    def test_echo_with_capture(self):
        output = execute_subprocess.with_capture(['echo', 'hello'])
        self.assertEqual(output.stdout, b'hello\n')
        self.assertEqual(output.stderr, b'')
        self.assertEqual(output.command, 'echo hello')
        self.assertEqual(output.return_code, 0)
        self.assertEqual(str(output), "command: echo hello return: 0 stdout: hello\n stderr: ")

    def test_errcode_with_capture(self):
        output = execute_subprocess.with_capture(['false'])
        self.assertEqual(output.stdout, b'')
        self.assertEqual(output.stderr, b'')
        self.assertEqual(output.command, 'false')
        self.assertEqual(output.return_code, 1)

    def test_no_capture(self):
        output = execute_subprocess.without_capture(['true'])
        self.assertEqual(output.stdout, None)
        self.assertEqual(output.stderr, None)
        self.assertEqual(output.command, 'true')
        self.assertEqual(output.return_code, 0)

    def test_echo_no_capture(self):
        output = execute_subprocess.without_capture(['echo', 'hello'])
        self.assertEqual(output.stdout, None)
        self.assertEqual(output.stderr, None)
        self.assertEqual(output.command, 'echo hello')
        self.assertEqual(output.return_code, 0)

    def test_errcode_no_capture(self):
        output = execute_subprocess.without_capture(['false'])
        self.assertEqual(output.stdout, None)
        self.assertEqual(output.stderr, None)
        self.assertEqual(output.command, 'false')
        self.assertEqual(output.return_code, 1)
