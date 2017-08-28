# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Test the ServicesCheckCommand Plugin.
"""
import unittest
from mock import patch, MagicMock
from ..prompts import prompt, confirm


class TestPrompts(unittest.TestCase):
    """Test case for the ServicesCheckCommand class."""

    # def setUp(self):
    #     self.mock_prompt = mock_inquirer_prompt

    @patch("cmm.prompts.inquirer.prompt")
    def test_confirm(self, mock_prompt):
        mock_prompt.return_value = {"res": "foo"}

        ans = confirm("what is the counterpart to bar?")
        self.assertEqual(ans, "foo")

    @patch("cmm.prompts.inquirer.prompt")
    def test_prompt_text(self, mock_prompt):
        mock_prompt.return_value = {"res": "foo"}

        ans = prompt("what is the counterpart to bar?")
        self.assertEqual(ans, "foo")

    @patch("cmm.prompts.inquirer.prompt")
    def test_prompt_choices(self, mock_prompt):
        mock_prompt.return_value = {"res": "foo"}

        ans = prompt("what is the counterpart to bar?", choices=["foo", "baz", "har"])
        self.assertEqual(ans, "foo")

    @patch("cmm.prompts.inquirer.prompt")
    def test_prompt_multiselect(self, mock_prompt):
        mock_prompt.return_value = {"res": ["foo", "baz"]}

        ans = prompt("what is the counterpart to bar?", choices=["foo", "baz", "har"], multiselect=True)
        self.assertEqual(ans, ["foo", "baz"])

    @patch("cmm.prompts.inquirer.prompt")
    def test_prompt_validate(self, mock_prompt):
        mock_prompt.return_value = {"res": 1}

        validate_me = lambda x: True
        ans = prompt("what is the counterpart to bar?", validate=validate_me)
        self.assertEqual(ans, 1)

if __name__ == '__main__':
    unittest.main()
