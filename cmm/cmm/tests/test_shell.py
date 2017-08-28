# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Test the shell.
"""
import unittest
import sys
from mock import patch, MagicMock
from ..shell import start_ipython_shell, register_magics


class TestShell(unittest.TestCase):
    """Test case for the <name> class."""

    # def setUp(self):
    #     self.mock_prompt = mock_inquirer_prompt

    @patch("cmm.shell.get_ipython")
    @patch("cmm.shell.ShellCommands")
    @patch("cmm.shell.DataStoreBuilder")
    def test_register_magics(self, mock_dsb, mock_sc, mock_gi):
        with self.assertRaises(SystemExit):
            register_magics('/tmp/cmm_test')

        sys.argv = ["cmm", "add"]
        with self.assertRaises(SystemExit):
            register_magics('/tmp/cmm_test')

        sys.argv = []
        register_magics('/tmp/cmm_test')
        # mock_sc.view.assert_called_with(None)

    def test_register_magics_no_term(self):
        # Tests a normal failure, as a result that tests don't have a terminal
        ans = register_magics('/tmp/cmm_test')
        self.assertEqual(ans, 1)

    @patch("cmm.shell.start_ipython")
    def test_start_ipython(self, mock_si):
        start_ipython_shell('/tmp/cmm')


if __name__ == '__main__':
    unittest.main()
