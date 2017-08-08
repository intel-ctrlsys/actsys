# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Tests for the FileStore class
"""
from __future__ import print_function
import unittest
import tempfile
import os
import sys
import StringIO
import json
import logging
from mock import Mock, patch
from ..datastore import DataStore, get_logger
from ..datastore_cli import DataStoreCLI, ParseOptionsException
from ..filestore import FileStore
from ..utilities import FileNotFound


class TestDataStoreCLI(unittest.TestCase):
    def setUp(self):
        self.mockDS = Mock(spec=DataStore)
        self.dscli = DataStoreCLI(self.mockDS)

    def test_via_sysargs(self):
        sys.argv = ['datastore', 'device', '-h']
        try:
            self.dscli.parse_and_run()
            self.fail()
        except SystemExit:
            pass

    def test_datastoreCLI_init(self):
        result = DataStoreCLI(self.mockDS)
        self.assertIsNotNone(result)

    def test_device_list(self):
        self.mockDS.list_devices.return_value = [{'hostname': 'node1'}]
        with patch('sys.stdout', new_callable=StringIO.StringIO) as output:
            result = self.dscli.parse_and_run(['device', 'list'])
            self.assertEqual(output.getvalue(), '--- node1 ---\nhostname             : node1\n')

    def test_device_bad_options(self):
        result = self.dscli.parse_and_run(['device', 'list', 'll'])
        self.assertEqual(result, 1)

        result = self.dscli.parse_and_run(['device', 'list', 'll', 'll'])
        self.assertEqual(result, 1)

    def test_device_get(self):
        # print('execute_devices')
        self.mockDS.get_device.return_value = [{'device_type': 'compute node'}]
        with patch('sys.stdout', new_callable=StringIO.StringIO) as output:
            result = self.dscli.parse_and_run(['device', 'get', 'node1'])
            self.assertEqual(output.getvalue(), '--- None ---\ndevice_type          : compute node\n')

        self.mockDS.list_devices.return_value = [{'device_type': 'node', 'debug_ip': '127.0.0.111'}]
        with patch('sys.stdout', new_callable=StringIO.StringIO) as output:
            result = self.dscli.parse_and_run(['device', 'list', 'debug_ip=127.0.0.111'])
            self.assertEqual(output.getvalue(),
                             '--- None ---\ndebug_ip             : 127.0.0.111\ndevice_type          : node\n')

    def test_device_get_no_options_allowed(self):
        with patch('sys.stdout', new_callable=StringIO.StringIO) as output:
            result = self.dscli.parse_and_run(['device', 'get', 'test1', 'option=opt'])
            # self.assertEqual(output.getvalue(), 'device get does not accept additional options.')
            self.assertEqual(result, 1)

    def test_device_get_only_one_device(self):
        with patch('sys.stdout', new_callable=StringIO.StringIO) as output:
            result = self.dscli.parse_and_run(['device', 'get', 'test[1-10]'])
            self.assertEqual(result, 1)

    def test_device_get_no_match(self):
        # print('execute_devices')
        self.mockDS.list_devices.return_value = []
        result = self.dscli.parse_and_run(['device', 'list', 'ham=node1'])
        self.assertEqual(result, 0)

    def test_device_set_no_existing_device(self):
        # print('execute_devices')
        self.mockDS.get_device.return_value = None
        result = self.dscli.parse_and_run(['device', 'set', 'hostname=node1', 'device_type=noe'])
        self.assertEqual(result, 0)

    def test_device_neg(self):
        # print('execute_devices')
        self.mockDS.list_devices.return_value = [{'hostname': 'node1', 'device_type': 'compute node'}]
        result = self.dscli.parse_and_run(['device', 'get'])
        self.assertEqual(result, 1)

    def test_device_upsert(self):
        self.mockDS.get_device.return_value = {'hostname': 'node1', 'device_type': 'node'}
        result = self.dscli.parse_and_run(['device', 'set', 'hostname=node1', 'ip_address=127.0.0.1'])
        self.assertEqual(result, 0)

        self.mockDS.get_device.return_value = {'hostname': 'node1', 'device_type': 'node'}
        result = self.dscli.parse_and_run(['device', 'set', 'hostname=node1', 'ip_address=UNDEF'])
        self.assertEqual(result, 0)

        self.mockDS.get_device.return_value = {'hostname': 'node1'}
        result = self.dscli.parse_and_run(['device', 'set', 'hostname=node1', 'ip_address=UNDEF'])
        self.assertEqual(1, result)

    def test_device_delete(self):
        self.mockDS.list_devices.return_value = [{'hostname': 'node1'}]
        result = self.dscli.parse_and_run(['device', 'delete', 'hostname=node'])
        self.assertEqual(result, 0)

        self.mockDS.list_devices.return_value = [{'hostname': 'node'}]
        result = self.dscli.parse_and_run(['device', 'delete', 'hostname=node'])
        self.assertEqual(result, 0)

    def test_profiles(self):
        self.mockDS.list_profiles.return_value = [{'profile_name': 'compute node'}]
        result = self.dscli.parse_and_run(['profile', 'list'])
        self.assertEqual(result, 0)

    def test_profiles_list_filter(self):
        self.mockDS.list_profiles.return_value = [{'profile_name': 'compute_node'}]
        result = self.dscli.parse_and_run(['profile', 'list', "profile_name=compute_node"])
        self.assertEqual(result, 0)

    def test_profile_bad_options(self):
        result = self.dscli.parse_and_run(['profile', 'list', 'll'])
        self.assertEqual(result, 1)

        result = self.dscli.parse_and_run(['profile', 'list', 'll', 'll'])
        self.assertEqual(result, 1)

    def test_profiles_delete(self):
        self.mockDS.list_profiles.return_value = [{'profile_name': 'compute node'}]
        result = self.dscli.parse_and_run(['profile', 'delete', 'profile_name=compute node'])
        self.assertEqual(result, 0)

    def test_profiles_upsert(self):
        self.mockDS.get_profile.return_value = {'profile_name': 'compute node'}
        result = self.dscli.parse_and_run(['profile', 'set', 'profile_name=compute node'])
        self.assertEqual(result, 0)

    def test_profile_get_no_match(self):
        self.mockDS.list_profiles.return_value = [{'profile_name': 'compute node'}]
        result = self.dscli.parse_and_run(['profile', 'get', 'profile_name=compute node'])
        self.assertEqual(result, 0)

    def test_profile_get_no_match2(self):
        self.mockDS.get_profile.return_value = None
        result = self.dscli.parse_and_run(['profile', 'get', 'profile_name=node'])
        self.assertEqual(result, 1)

    def test_profile_set_no_existing_profile(self):
        # print('execute_devices')
        self.mockDS.get_profile.return_value = None
        result = self.dscli.parse_and_run(['profile', 'set', 'profile_name=node'])
        self.assertEqual(result, 0)

    def test_profile_neg(self):
        # print('execute_devices')
        self.mockDS.list_profiles.return_value = [{'profile_name': 'compute node'}]
        result = self.dscli.parse_and_run(['profile', 'get'])
        self.assertEqual(result, 1)

    def test_configuration_list(self):
        self.mockDS.list_configuration.return_value = [{'key': 'key1', "value": "value1"}]
        with patch('sys.stdout', new_callable=StringIO.StringIO) as output:
            result = self.dscli.parse_and_run(['config', 'list'])
            self.assertEqual(output.getvalue(), "key1                           : value1\n")

    def test_configuration_get(self):
        # print('execute_configurations')
        self.mockDS.get_configuration_value.return_value = [{'key': 'key1'}]
        with patch('sys.stdout', new_callable=StringIO.StringIO) as output:
            result = self.dscli.parse_and_run(['config', 'get', 'key1'])
            self.assertEqual(output.getvalue(), "key1 : [{'key': 'key1'}]\n")

    def test_configuration_get_no_match(self):
        # print('execute_configurations')
        self.mockDS.get_configuration_value.return_value = None
        result = self.dscli.parse_and_run(['config', 'get', 'key1'])
        self.assertEqual(result, 1)

    def test_configuration_set_no_existing_configuration(self):
        # print('execute_configurations')
        self.mockDS.get_configuration_value.return_value = []
        result = self.dscli.parse_and_run(['config', 'set', 'key1'])
        self.assertEqual(result, 1)

    def test_configuration_neg(self):
        # print('execute_configurations')
        self.mockDS.get_configuration_value.return_value = [{'hostname': 'node1', 'key': 'key1'}]
        result = self.dscli.parse_and_run(['config', 'get'])
        self.assertEqual(result, 1)

    def test_configuration_upsert(self):
        self.mockDS.get_configuration_value.return_value = [{'key': 'key1'}]
        result = self.dscli.parse_and_run(['config', 'set', 'key4', 'value1'])
        self.assertEqual(result, 0)

    def test_configuration_upsert_none(self):
        self.mockDS.get_configuration_value.return_value = [{'key': 'key1'}]
        result = self.dscli.parse_and_run(['config', 'set'])
        self.assertEqual(result, 1)

    def test_configuration_delete(self):
        self.mockDS.get_configuration_value.return_value = [{'key': 'key1'}]
        result = self.dscli.parse_and_run(['config', 'delete', 'key1'])
        self.assertEqual(result, 0)

    def test_configuration_delete_none(self):
        self.mockDS.get_configuration_value.return_value = [{'key': 'key1'}]
        result = self.dscli.parse_and_run(['config', 'delete'])
        self.assertEqual(result, 1)

    def test_log_begin_end(self):
        self.mockDS.list_logs_between_timeslice.return_value = [{'foo': 'foovalue'}]
        result = self.dscli.parse_and_run(['log', '--begin', '01/01/2017', '--end', '03/01/2017', 'get'])
        self.assertEqual(result, 0)

    def test_log_begin_none(self):
        self.mockDS.list_logs_between_timeslice.return_value = [{'foo': 'foovalue'}]
        result = self.dscli.parse_and_run(['log', '--end', '03/01/2017', 'get'])
        self.assertEqual(result, 0)

    def test_log_begin_end_none(self):
        self.mockDS.list_logs_between_timeslice.return_value = [{'foo': 'foovalue'}]
        result = self.dscli.parse_and_run(['log', '--begin', '03/01/2017', 'get'])
        self.assertEqual(result, 0)

    def test_log_end_none(self):
        self.mockDS.list_logs_between_timeslice.return_value = [{'foo': 'foovalue'}]
        result = self.dscli.parse_and_run(['log', 'get'])
        self.assertEqual(result, 0)


class TestGroupCLI(unittest.TestCase):
    group_name = "test"
    device_list = "c[1-10]"
    group = {group_name: device_list}
    group_list = [group, group]

    def setUp(self):
        self.mockDS = Mock(spec=DataStore)
        self.dscli = DataStoreCLI(self.mockDS)

    def test_group_get(self):
        self.mockDS.get_group_devices.return_value = self.device_list
        self.mockDS.expand_device_list.return_value = [self.group_name]
        with patch('sys.stdout', new_callable=StringIO.StringIO) as output:
            result = self.dscli.parse_and_run(['group', 'get', 'test'])
            self.assertEqual(output.getvalue(), "{} - {}\n".format(self.group_name, self.device_list))
            self.assertEqual(result, 0)
        self.mockDS.get_group_devices.assert_called_once_with("test")

    def test_group_expand(self):
        self.mockDS.expand_device_list.return_value = self.device_list
        with patch('sys.stdout', new_callable=StringIO.StringIO) as output:
            result = self.dscli.parse_and_run(['group', 'expand', '@test'])
            self.assertEqual(output.getvalue(), self.device_list + '\n')
            self.assertEqual(result, 0)
        self.mockDS.expand_device_list.assert_called_once_with("@test")

    def test_group_fold(self):
        self.mockDS.fold_devices.return_value = self.device_list
        with patch('sys.stdout', new_callable=StringIO.StringIO) as output:
            result = self.dscli.parse_and_run(['group', 'fold', 'c1,c2,c3,c4,c5'])
            self.assertEqual(output.getvalue(), self.device_list + '\n')
            self.assertEqual(result, 0)
        self.mockDS.fold_devices.assert_called_once_with("c1,c2,c3,c4,c5")

    def test_group_list(self):
        self.mockDS.list_groups.return_value = {"a": "1", "b": "1", "c": "1"}
        with patch('sys.stdout', new_callable=StringIO.StringIO) as output:
            result = self.dscli.parse_and_run(['group', 'list'])
            self.assertEqual(output.getvalue(),  'a\nb\nc\n')
            self.assertEqual(result, 0)
        self.mockDS.list_groups.assert_called_once()
        self.mockDS.reset_mock()

        self.mockDS.list_groups.return_value = {}
        with patch('sys.stdout', new_callable=StringIO.StringIO) as output:
            result = self.dscli.parse_and_run(['group', 'list'])
            self.assertEqual(output.getvalue(), 'No groups found.\n')
            self.assertEqual(result, 0)
        self.mockDS.list_groups.assert_called_once()

    def test_group_add(self):
        self.mockDS.add_to_group.return_value = self.device_list
        with patch('sys.stdout', new_callable=StringIO.StringIO) as output:
            result = self.dscli.parse_and_run(['group', 'add', self.device_list, self.group_name])
            self.assertEqual(output.getvalue(), "Group {} has been updated to {}\n".format(self.group_name, self.device_list))
            self.assertEqual(result, 0)
        self.mockDS.add_to_group.assert_called_once_with(self.device_list, self.group_name)

    def test_group_add_exception(self):
        self.mockDS.add_to_group.side_effect = FileNotFound("File not found\n")
        self.dscli.parse_and_run(['group', 'add', self.device_list, self.group_name])

    def test_group_remove(self):
        self.mockDS.remove_from_group.return_value = self.device_list
        with patch('sys.stdout', new_callable=StringIO.StringIO) as output:
            result = self.dscli.parse_and_run(['group', 'remove', 'foo', self.group_name])
            self.assertEqual(output.getvalue(), "Group {} has been updated to {}\n".format(self.group_name, self.device_list))
            self.assertEqual(result, 0)
        self.mockDS.remove_from_group.assert_called_once_with('foo', self.group_name)

    def test_unknown_group_remove(self):
        self.mockDS.remove_from_group.return_value = None
        with patch('sys.stdout', new_callable=StringIO.StringIO) as output:
            result = self.dscli.parse_and_run(['group', 'remove', 'foo', self.group_name])
            self.assertEqual(result, 0)
        self.mockDS.remove_from_group.assert_called_once_with('foo', self.group_name)

    def test_group_remove_exception(self):
        self.mockDS.remove_from_group.side_effect = FileNotFound("File not found\n")
        self.dscli.parse_and_run(['group', 'remove', self.device_list, self.group_name])

    def test_group_groups(self):
        self.mockDS.get_device_groups.return_value = ["a", "b"]
        with patch('sys.stdout', new_callable=StringIO.StringIO) as output:
            result = self.dscli.parse_and_run(['group', 'groups', 'foo'])
            self.assertEqual(output.getvalue(), "foo is a member of groups:\na\nb\n")
            self.assertEqual(result, 0)
        self.mockDS.get_device_groups.assert_called_once_with('foo')

        # No group arg given
        self.mockDS.get_device_groups.return_value = ["a", "b"]
        try:
            self.dscli.parse_and_run(['group', 'groups'])
            self.fail("Invalid group args shouldn't pass")
        except SystemExit:
            pass

        # Device arg not allowed
        self.mockDS.get_device_groups.return_value = ["a", "b"]
        try:
            self.dscli.parse_and_run(['group', 'groups', 'foo', 'bar'])
            self.fail("Invalid group args shouldn't pass")
        except SystemExit:
            pass

        self.mockDS.get_device_groups.return_value = []
        with patch('sys.stdout', new_callable=StringIO.StringIO) as output:
            result = self.dscli.parse_and_run(['group', 'groups', 'foo'])
            self.assertEqual(result, 0)


class TestsDataStoreCLIOptions(unittest.TestCase):
    def test_no_options(self):
        result = DataStoreCLI.parse_options(None)
        self.assertEqual(result, dict())

        result = DataStoreCLI.parse_options([])
        self.assertEqual(result, dict())

    def test_valid_strings(self):
        result = DataStoreCLI.parse_options(['foo=bar', 'b=c', 'hold=on'])
        self.assertEqual(result, {'foo': 'bar', 'b': 'c', 'hold': 'on'})

        result = DataStoreCLI.parse_options(['asdfghjkl=qwertyuiop'])
        self.assertEqual(result, {'asdfghjkl': 'qwertyuiop'})

    def test_valid_lists(self):
        result = DataStoreCLI.parse_options(["mylist=[foo,bar,baz]", "join=me"])
        self.assertEqual(result, {"mylist": ['foo', 'bar', 'baz'], "join": "me"})

        result = DataStoreCLI.parse_options(["mylist=[foo,  bar, baz]", "join=me"])
        self.assertEqual(result, {"mylist": ['foo', 'bar', 'baz'], "join": "me"})

        result = DataStoreCLI.parse_options(["mylist=[ foo,bar,baz ]", "join=me"])
        self.assertEqual(result, {"mylist": ['foo', 'bar', 'baz'], "join": "me"})

        result = DataStoreCLI.parse_options(["mylist=[ 1, bar ]", "join=me"])
        self.assertEqual(result, {"mylist": [1, 'bar'], "join": "me"})

        result = DataStoreCLI.parse_options(["mylist=[foo, 1]", "join=me"])
        self.assertEqual(result, {"mylist": ['foo', 1], "join": "me"})

    def test_no_empty_options(self):
        with self.assertRaises(ParseOptionsException):
            result = DataStoreCLI.parse_options(["empty=", "not=allowed"])
        with self.assertRaises(ParseOptionsException):
            result = DataStoreCLI.parse_options(["=bar", "not=allowed"])

        with self.assertRaises(ParseOptionsException):
            result = DataStoreCLI.parse_options(["not=allowed", "foo"])
        with self.assertRaises(ParseOptionsException):
            result = DataStoreCLI.parse_options(["bar", "not=allowed"])

    def test_integers(self):
        result = DataStoreCLI.parse_options(["arg=1", "5=2"])
        self.assertEqual(result, {"arg": 1, 5: 2})

        result = DataStoreCLI.parse_options(["1=arg"])
        self.assertEqual(result, {1: "arg"})

    def test_equal_in_options(self):
        result = DataStoreCLI.parse_options(["f=b", "kargs=console=tty0,115280"])
        self.assertEqual(result, {"f": "b", "kargs": "console=tty0,115280"})

        result = DataStoreCLI.parse_options(["f=b", "kargs=console=tty0,115280 Addl args"])
        self.assertEqual(result, {"f": "b", "kargs": "console=tty0,115280 Addl args"})

    def test_no_duplicate_keys(self):
        with self.assertRaises(ParseOptionsException):
            result = DataStoreCLI.parse_options(["a=b", "a=b"])

        try:
            result = DataStoreCLI.parse_options(["a=b", "a=b"])
            self.fail()
        except ParseOptionsException as poe:
            self.assertEqual(poe.message, "Key `a` was found more than once. Please make sure your keys "
                                          "in the options list are unique.")

        with self.assertRaises(ParseOptionsException):
            result = DataStoreCLI.parse_options(["a=b", "foo=bar", "1=2", "a=b"])


class TestFunctionalReturnCodes(unittest.TestCase):
    FILE_STRING = "unknown, to be contrusted in setup()"
    FILE_CONFIG = """{
  "configuration_variables": {
    "log_file_path": "/tmp/ctrl.log",
    "provisioning_agent_software": "warewulf"
  },
  "device": [
   {
      "device_id": 1,
      "device_type": "test_dev_type_test",
      "hostname": "test_hostname",
      "ip_address": "127.0.0.1",
      "mac_address": "AA:GG:PP",
      "profile_name": "compute_node"
    },
    {
      "device_id": 2,
      "device_type": "test_dev_type_test",
      "hostname": "test_hostname2",
      "ip_address": "127.0.0.2",
      "mac_address": "AA:GG:22",
      "profile_name": "compute_node",
      "tests": "are_awesome"
    }
  ],
  "profile": [
    {
      "password": "test_pass",
      "port": 22,
      "profile_name": "compute_node"
    }
  ]
}"""
    LOG_FILENAME = "unknown, setup in setUPCLass(cls)"
    LOG_FILE = """2017-02-22 09:18:54,432 / INFO / DataStore / BATS / None / Does this work?
2017-01-01 09:18:54,433 / WARNING / DataStore / BATS / None / Does this work?
2017-01-01 09:18:54,433 / ERROR / DataStore / BATS / None / Does this work?
2017-01-01 09:18:54,433 / CRITICAL / DataStore / BATS / None / Does this work?
2017-01-01 09:18:54,434 / INFO / DataStore / None / None / Does this work?
2017-01-01 09:18:54,434 / WARNING / DataStore / None / None / Does this work?
2017-01-01 09:18:54,434 / ERROR / DataStore / BATS / None / Does this work?
2017-01-01 09:18:54,435 / CRITICAL / DataStore / None / None / Does this work?
2016-01-01 10:25:18,042 / DEBUG / DataStore / BATS / 1 / Does this work?
2016-01-01 10:25:18,042 / WARNING / DataStore / BATS / 2 / Does this work?
2015-01-01 10:25:18,042 / ERROR / DataStore / BATS / 1 / Does this work?
2017-01-01 10:25:18,042 / ERROR / DataStore / Does this work?"""

    def setUp(self):
        temp_log_file = tempfile.NamedTemporaryFile("w", delete=False)
        temp_log_file.write(self.LOG_FILE)
        temp_log_file.close()
        self.LOG_FILENAME = temp_log_file.name

        config = json.loads(self.FILE_CONFIG)
        config["configuration_variables"]["log_file_path"] = self.LOG_FILENAME

        temp_file = tempfile.NamedTemporaryFile("w", delete=False)
        temp_file.write(json.dumps(config))
        temp_file.close()
        self.FILE_STRING = temp_file.name

        logger = get_logger()
        logger.handlers = []
        DataStore.LOG_LEVEL = logging.DEBUG

        self.fs = FileStore(self.FILE_STRING, None)
        self.dscli = DataStoreCLI(self.fs)

    def tearDown(self):
        os.remove(self.FILE_STRING)
        os.remove(self.LOG_FILENAME)

    def test_return_codes(self):
        """
        You'll also get an error for tracebacks!
        :return:
        """
        commands = [
            {"cmd": ['device', 'list'], "out": 0},
            {"cmd": ['device', 'get', 'test_hostname'], "out": 0},
            {"cmd": ['device', 'set', 'test_hostname'], "out": 0},
            {"cmd": ['device', 'set', 'test_hostname', 'port=23'], "out": 0},
            {"cmd": ['device', 'set', 'test_hostname', 'test=foo'], "out": 0},
            {"cmd": ['device', 'get', 'new_hostname'], "out": 1},
            {"cmd": ['device', 'set', 'new_hostname', 'foo=node'], "out": 1},
            {"cmd": ['device', 'set', 'new_hostname', 'device_type=node'], "out": 0},
            {"cmd": ['device', 'get', 'new_hostname'], "out": 0},
            {"cmd": ['device', 'list', 'mac_address=AA:GG:PP'], "out": 0},
            {"cmd": ['device', 'list', 'mac_address=AA:GG:111'], "out": 0},
            {"cmd": ['device', 'delete', 'test_hostname2'], "out": 0},
            {"cmd": ['device', 'delete', 'not_valid_name'], "out": 0},
            {"cmd": ['profile', 'get', 'compute_node'], "out": 0},
            {"cmd": ['profile', 'get'], "out": 1},
            {"cmd": ['profile', 'get', 'invalid'], "out": 1},
            {"cmd": ['profile', 'set', 'compute_node', 'my=profile_value'], "out": 0},
            {"cmd": ['profile', 'delete', 'compute_node'], "out": 1},
            {"cmd": ['profile', 'list'], "out": 0},
            {"cmd": ['profile', 'set', 'compute_node2', 'my=profile_value'], "out": 0},
            {"cmd": ['profile', 'delete', 'compute_node2'], "out": 0},
            {"cmd": ['config', 'get'], "out": 1},
            {"cmd": ['config', 'get', 'log_file_path'], "out": 0},
            {"cmd": ['config', 'get', 'not_found'], "out": 1},
            {"cmd": ['config', 'set', 'log_file_path2'], "out": 1},
            {"cmd": ['config', 'set', 'log_file_path2', 'foo'], "out": 0},
            {"cmd": ['config', 'delete', 'log_file_path2'], "out": 0},
            {"cmd": ['config', 'delete', 'log_file_path2'], "out": 0},
            {"cmd": ['config', 'set', 'log_file_path', 'foo'], "out": 0},
            {"cmd": ['config', 'set', 'log_file_path', 'bar'], "out": 0},
            {"cmd": ['config', 'set', 'log_file_path', 'test'], "out": 0},
            {"cmd": ['config', 'get', 'log_file_path'], "out": 0},
            {"cmd": ['config', 'get', 'log_file_path123'], "out": 1},
            {"cmd": ['device', 'list', 'mac_address=AA:GG:PP'], "out": 0},
            {"cmd": ['device', 'list', 'mac_address=AA:GG:PP'], "out": 0}
        ]

        for command in commands:
            result = self.dscli.parse_and_run(command["cmd"])
            self.assertEqual(result, command["out"], "Failed to execute command '{}'. Actual: {} Expected: {}"
                             .format(command["cmd"], result, command["out"]))


if __name__ == '__main__':
    unittest.main()
