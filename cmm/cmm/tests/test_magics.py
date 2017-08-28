# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Test the magics.
"""
import unittest
from mock import patch, MagicMock
from ..magics import ShellCommands
from datastore import DataStoreBuilder


class TestMagics(unittest.TestCase):
    """Test case for the <name> class."""

    def setUp(self):
        self.datastore = DataStoreBuilder.get_datastore_from_string('/tmp/test_cmm', 50)
        self.ip_shell = MagicMock()
        self.sc = ShellCommands(self.ip_shell, self.datastore)

    def test_view_magic(self):
        self.assertIsInstance(self.sc, ShellCommands)

        self.sc.view(None)
        self.sc.view("rocky")

    # @patch("cmm.magics.prompts.confirm")
    # def test_delete(self, mock_confirm):
    #     mock_confirm.return_value = True
    #     self.sc.delete("-d boikfg")

if __name__ == '__main__':
    unittest.main()
