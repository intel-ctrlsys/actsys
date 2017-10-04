# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Tests for the MetagraphStore class
"""

import os
import unittest
import tempfile
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

try:
    import metagraph
    from ..metagraphstore import MetagraphStore
except:
    raise unittest.SkipTest('Could not find metagraph library; skipping tests.')
from ..datastore import DataStoreException


def create_mock_graph_node(properties=None):
    mock_node = MagicMock(spec=metagraph.mg_handler.mg_handler.MGNode)
    if properties is not None:
        mock_node.get_properties.return_value = properties
    return mock_node


class TestMetagraphDB(unittest.TestCase):
    """Simple tests for a simple class."""

    CONNECTION_STRING = "localhost:8080"

    TEST_DEVICE = {
        "device_id": 1,
        "device_type": "test_device_type",
        "hostname": "test_hostname",
        "ip_address": "127.0.0.1",
        "mac_address": "AA:GG:11",
        "profile_name": "compute_node",
        "tests": "are_awesome",
        "password": "test_pass",
        "port": 22,
    }

    TEST_DEVICE2 = {
        "device_id": 2,
        "device_type": "test_device_type2",
        "hostname": "test_hostname2",
        "ip_address": "127.0.0.2",
        "mac_address": "AA:GG:22",
        "profile_name": "invalid_profile",
        "tests": "are_awesome2",
        "password": "test_pass2",
        "port": 222,
    }

    def setUp(self):
        # TODO: this should be before import of metagraph; where to put stop?
        # self.mock_database = patch('neo4j.v1.GraphDatabase.driver').start()
        self.mock_create_graph = patch('metagraph.graph_tools.create_graph.create_graph').start()
        self.mock_remove_graph = patch('metagraph.graph_tools.remove_graph.remove_graph').start()
        self.mock_match_nodes_ops = patch('metagraph.match_nodes.mg_match_nodes.MGNodeMatcher.match_nodes_using_operators').start()
        self.mock_get_linked_nodes = patch('metagraph.mg_handler.mg_handler.MGNode.get_linked_nodes').start()
        self.mock_add_node = patch('metagraph.mg_handler.mg_handler.MGNode.add_node').start()
        self.mock_remove_node = patch('metagraph.mg_handler.mg_handler.MGNode.remove_node').start()
        self.mock_get_node = patch('metagraph.mg_handler.mg_handler.MGNode.get_node').start()

        self.metagraph = MetagraphStore(self.CONNECTION_STRING, None)

    def tearDown(self):
        # self.mock_database.stop()
        self.mock_create_graph.stop()
        self.mock_remove_graph.stop()
        self.mock_match_nodes_ops.stop()
        self.mock_get_linked_nodes.stop()
        self.mock_add_node.stop()
        self.mock_remove_node.stop()
        self.mock_get_node.stop()
        # TODO: stop all

    def test_get_device_found(self):
        mock_node = create_mock_graph_node(self.TEST_DEVICE)
        self.mock_match_nodes_ops.return_value = [mock_node]
        result = self.metagraph.get_device(self.TEST_DEVICE["hostname"])
        self.assertEqual(result, self.TEST_DEVICE)

    def test_get_device_not_found(self):
        self.mock_match_nodes_ops.return_value = []
        result = self.metagraph.get_device(self.TEST_DEVICE["hostname"])
        self.assertIsNone(result)

    def test_get_device_found_multiple(self):
        mock_node = create_mock_graph_node(self.TEST_DEVICE)
        self.mock_match_nodes_ops.return_value = [mock_node, mock_node]
        with self.assertRaises(DataStoreException) as ex:
            self.metagraph.get_device(self.TEST_DEVICE["hostname"])
        self.assertIn("duplicate device", str(ex.exception))

    def test_list_devices_no_devices(self):
        self.mock_match_nodes_ops.return_value = []
        result = self.metagraph.list_devices()
        self.assertEqual([], result)

    def test_list_devices_two_devices(self):
        mock_node = create_mock_graph_node(self.TEST_DEVICE)
        self.mock_match_nodes_ops.return_value = [mock_node, mock_node]
        result = self.metagraph.list_devices()
        self.assertEqual(2, len(result))

    def test_list_devices_with_filter_no_matches(self):
        self.mock_match_nodes_ops.return_value = []
        result = self.metagraph.list_devices({"password": "test_pass"})
        self.assertEqual([], result)

    def test_list_devices_with_filter_two_matches(self):
        mock_node = create_mock_graph_node(self.TEST_DEVICE)
        self.mock_match_nodes_ops.return_value = [mock_node, mock_node]
        result = self.metagraph.list_devices({"password": "test_pass"})
        self.assertEqual(2, len(result))

    def test_set_device_empty_returns_empty_list(self):
        result = self.metagraph.set_device([])
        self.assertEqual([], result)

    def test_set_device_missing_type_raises_exception(self):
        with self.assertRaises(DataStoreException) as ex:
            self.metagraph.set_device([{"dummy": "device"}])
        self.assertIn("device_type", str(ex.exception))

    def test_set_device_missing_profile_raises_exception(self):
        with self.assertRaises(DataStoreException) as ex:
            self.metagraph.set_device([{"device_type": "device", "profile_name": "dummy"}])
        self.assertIn("profile does not exist", str(ex.exception))

    def test_set_device_new_device_added(self):
        mock_profile = create_mock_graph_node({"profile_name": self.TEST_DEVICE["profile_name"]})
        self.mock_match_nodes_ops.side_effect = [[mock_profile],  # returned by list_profiles
                                                 []]              # returned by existing node lookup
        result = self.metagraph.set_device([self.TEST_DEVICE])
        self.assertEqual(1, len(result))
        self.assertTrue(self.mock_add_node.called)

    def test_set_device_existing_device_updated(self):
        mock_profile = create_mock_graph_node({"profile_name": self.TEST_DEVICE["profile_name"]})
        mock_node = create_mock_graph_node(self.TEST_DEVICE)
        self.mock_match_nodes_ops.side_effect = [[mock_profile],  # returned by list_profiles
                                                 [mock_node]]     # returned by existing node lookup
        result = self.metagraph.set_device([self.TEST_DEVICE])
        self.assertEqual(1, len(result))
        self.assertTrue(mock_node.set_properties.called)
        self.assertFalse(self.mock_add_node.called)

    def test_list_profiles_no_profiles_returns_empty_list(self):
        self.mock_match_nodes_ops.return_value = []
        result = self.metagraph.list_profiles()
        self.assertEqual([], result)

    def test_list_profiles_two_profiles(self):
        mock_node = create_mock_graph_node()
        self.mock_match_nodes_ops.return_value = [mock_node, mock_node]
        result = self.metagraph.list_profiles()
        self.assertEqual(2, len(result))

    def test_delete_device_no_device_returns_empty_list(self):
        self.mock_match_nodes_ops.return_value = []
        result = self.metagraph.delete_device([])
        self.assertEqual([], result)

    def test_delete_device_no_matching_device_returns_empty_list(self):
        result = self.metagraph.delete_device([1])
        self.assertEqual([], result)

    def test_delete_device_matching_device_is_deletd(self):
        mock_node = create_mock_graph_node(self.TEST_DEVICE)
        self.mock_match_nodes_ops.return_value = [mock_node]
        result = self.metagraph.delete_device([self.TEST_DEVICE["device_id"]])
        self.assertEqual([self.TEST_DEVICE["device_id"]], result)
        self.assertTrue(self.mock_remove_node.called)

    def test_get_profile_name_not_found_returns_none(self):
        self.mock_match_nodes_ops.return_value = []
        result = self.metagraph.get_profile("prof1")
        self.assertIsNone(result)

    def test_get_profile_returns_one_profile(self):
        mock_profile = create_mock_graph_node({"profile_name": "prof1"})
        self.mock_match_nodes_ops.return_value = [mock_profile]
        result = self.metagraph.get_profile("prof1")
        self.assertEqual("prof1", result["profile_name"])

    def test_get_profile_multiple_matches_returns_first(self):
        mock_profile = create_mock_graph_node({"profile_name": "prof1"})
        self.mock_match_nodes_ops.return_value = [mock_profile, mock_profile]
        result = self.metagraph.get_profile("prof1")
        self.assertEqual("prof1", result["profile_name"])

    def test_set_profile_no_name_raises_error(self):
        with self.assertRaises(DataStoreException) as ex:
            self.metagraph.set_profile({"not": "profile"})
        self.assertIn("profile_name", str(ex.exception))

    def test_set_profile_add_new_profile(self):
        self.mock_match_nodes_ops.return_value = []
        result = self.metagraph.set_profile({"profile_name": "prof1"})
        self.assertEqual("prof1", result)
        self.assertTrue(self.mock_add_node.called)

    def test_set_profile_update_existing(self):
        mock_profile = create_mock_graph_node({"profile_name": "prof1"})
        self.mock_match_nodes_ops.return_value = [mock_profile]
        result = self.metagraph.set_profile({"profile_name": "prof1"})
        self.assertEqual("prof1", result)
        self.assertTrue(mock_profile.set_properties.called)
        self.assertFalse(self.mock_add_node.called)

    def test_delete_profile_not_found_raises_error(self):
        with self.assertRaises(DataStoreException) as ex:
            self.metagraph.delete_profile("myprof")
        self.assertIn("no profile", str(ex.exception))

    def test_delete_profile_one_found(self):
        mock_profile = create_mock_graph_node({"profile_name": "prof1"})
        self.mock_match_nodes_ops.return_value = [mock_profile]
        result = self.metagraph.delete_profile("prof1")
        self.assertEqual("prof1", result)
        self.assertTrue(self.mock_remove_node.called)

    def test_delete_profile_with_devices_raises_error(self):
        mock_profile = create_mock_graph_node({"profile_name": "prof1"})
        self.mock_match_nodes_ops.return_value = [mock_profile]
        mock_node = create_mock_graph_node()
        mock_profile.get_linked_nodes.return_value = [mock_node]
        with self.assertRaises(DataStoreException) as ex:
            self.metagraph.delete_profile("prof1")
        self.assertIn("cannot be deleted", str(ex.exception))

    def test_get_configuration_no_saved_config(self):
        self.mock_get_node.side_effect = BaseException
        result = self.metagraph.get_configuration_value("name1")
        self.assertIsNone(result)

    def test_get_configuration_key_not_found_returns_none(self):
        mock_config = create_mock_graph_node({"type": "config", "name1": "val1"})
        self.mock_get_node.side_effect = [mock_config]
        result = self.metagraph.get_configuration_value("name2")
        self.assertIsNone(result)

    def test_get_configuration_key_found(self):
        mock_config = create_mock_graph_node({"type": "config", "name1": "val1"})
        self.mock_get_node.side_effect = [mock_config]
        result = self.metagraph.get_configuration_value("name1")
        self.assertEqual("val1", result)

    def test_list_configuration_no_saved_config(self):
        self.mock_get_node.side_effect = BaseException
        result = self.metagraph.list_configuration()
        self.assertEqual([], result)

    def test_list_configuration_empty_config(self):
        mock_config = create_mock_graph_node({})
        self.mock_get_node.side_effect = [mock_config]
        result = self.metagraph.list_configuration()
        self.assertEqual([{}], result)

    def test_list_configuration_returns_lsit(self):
        configs = [{"type": "config", "name1": "val1", "name2": "val2"}]
        mock_config = create_mock_graph_node(configs[0])
        self.mock_get_node.side_effect = [mock_config]
        result = self.metagraph.list_configuration()
        self.assertEqual(configs, result)

    def test_set_configuration_no_saved_config_adds_node(self):
        self.mock_get_node.side_effect = BaseException
        result = self.metagraph.set_configuration("name1", "val1")
        self.assertEqual("name1", result)
        self.assertTrue(self.mock_add_node.called)

    def test_set_configuration_adds_to_config(self):
        # new or existing key adds to config
        mock_config = create_mock_graph_node({})
        self.mock_get_node.side_effect = [mock_config]
        result = self.metagraph.set_configuration("name1", "val1")
        self.assertEqual("name1", result)
        self.assertTrue(mock_config.set_properties.called)

    def test_delete_configuration(self):
        # TODO: this should be implemented, but some MG APIs are missing
        with self.assertRaises(NotImplementedError):
            self.metagraph.delete_configuration("key")

    def test_list_groups_no_groups_returns_empty_list(self):
        self.mock_match_nodes_ops.return_value = []
        result = self.metagraph.list_groups()
        self.assertEqual([], result)

    def test_list_groups_two_groups(self):
        mock_node = create_mock_graph_node({"type": "group"})
        self.mock_match_nodes_ops.return_value = [mock_node, mock_node]
        result = self.metagraph.list_groups()
        self.assertEqual(2, len(result))

    def test_get_group_devices_no_such_group(self):
        self.mock_match_nodes_ops.return_value = []
        result = self.metagraph.get_group_devices("group1")
        self.assertIsNone(result)

    def test_get_group_devices_no_devices_returns_empty_list(self):
        mock_group = create_mock_graph_node({"type": "group"})
        self.mock_match_nodes_ops.return_value = [mock_group]
        mock_group.get_linked_nodes.return_value = []
        result = self.metagraph.get_group_devices("group1")
        self.assertEqual([], result)

    # TODO: what about nested groups?
    def test_get_group_devices_two_devices(self):
        mock_group = create_mock_graph_node({"type": "group"})
        mock_node = create_mock_graph_node()
        self.mock_match_nodes_ops.return_value = [mock_group]
        mock_group.get_linked_nodes.return_value = [mock_node, mock_node]
        result = self.metagraph.get_group_devices("group1")
        self.assertEqual(2, len(result))

    def test_add_to_group_no_group_raises_error(self):
        self.mock_match_nodes_ops.return_value = []
        with self.assertRaises(DataStoreException) as ex:
            self.metagraph.add_to_group(["node1"], "group1")
        self.assertIn("no group", str(ex.exception))

    def test_add_to_group_no_node_skips_node(self):
        mock_group = create_mock_graph_node({"type": "group"})
        self.mock_match_nodes_ops.side_effect = [[mock_group],  # for group search
                                                 []]            # for node search
        result = self.metagraph.add_to_group([], "group1")
        self.assertEqual([], result)

    def test_add_to_group_empty_list_returns_empty_list(self):
        mock_group = create_mock_graph_node({"type": "group"})
        self.mock_match_nodes_ops.side_effect = [[mock_group]]
        result = self.metagraph.add_to_group([], "group1")
        self.assertEqual([], result)

    def test_add_to_group_two_new_members(self):
        mock_node1 = create_mock_graph_node({"device_id": "dev1"})
        mock_node2 = create_mock_graph_node({"device_id": "dev2"})
        mock_group = create_mock_graph_node({"type": "group"})
        self.mock_match_nodes_ops.side_effect = [[mock_group],
                                                 [mock_node1], [mock_node2]]
        mock_group.get_linked_nodes.return_value = []
        result = self.metagraph.add_to_group(["dev1", "dev2"], "group1")
        self.assertEqual(2, len(result))
        self.assertEqual(0, mock_group.link_to.call_count)

    def test_add_to_group_existing_members(self):
        mock_node1 = create_mock_graph_node({"device_id": "dev1"})
        mock_node2 = create_mock_graph_node({"device_id": "dev2"})
        mock_group = create_mock_graph_node({"type": "group"})
        self.mock_match_nodes_ops.side_effect = [[mock_group],
                                                 [mock_node1], [mock_node2]]
        mock_group.get_linked_nodes.return_value = [mock_node1, mock_node2]
        result = self.metagraph.add_to_group(["dev1", "dev2"], "group1")
        self.assertEqual(2, len(result))
        self.assertEqual(0, mock_group.link_to.call_count)

    def test_remove_from_group_no_such_group_raises_error(self):
        with self.assertRaises(DataStoreException) as ex:
            self.metagraph.remove_from_group(["one"], "group1")
        self.assertIn("doesn't exist", str(ex.exception))

    def test_remove_from_group_node_not_found(self):
        mock_group = create_mock_graph_node({"group_name": "group1"})
        self.mock_match_nodes_ops.return_value = [mock_group]
        mock_group.get_linked_nodes.return_value = []
        result = self.metagraph.remove_from_group(["one"], "group1")
        self.assertEqual([], result)

    def test_remove_from_group_removes_from_list(self):
        mock_group = create_mock_graph_node({"group_name": "group1"})
        mock_node1 = create_mock_graph_node({"device_id": "dev1"})
        mock_node2 = create_mock_graph_node({"device_id": "dev2"})
        self.mock_match_nodes_ops.return_value = [mock_group]
        mock_group.get_linked_nodes.return_value = [mock_node1, mock_node2]
        result = self.metagraph.remove_from_group(["dev1"], "group1")
        self.assertEqual(["dev2"], result)
        self.assertTrue(mock_group.remove_link.called)

    def test_get_devices_by_type_no_devices_returns_empty_list(self):
        result = self.metagraph.get_devices_by_type("mytype")
        self.assertEqual([], result)

    def test_get_devices_by_type_two_devices(self):
        mock_node = create_mock_graph_node()
        self.mock_match_nodes_ops.return_value = [mock_node, mock_node]
        result = self.metagraph.get_devices_by_type("mytype")
        self.assertEqual(2, len(result))

    def test_get_devices_by_type_match_device_name(self):
        mock_node = create_mock_graph_node()
        self.mock_match_nodes_ops.return_value = [mock_node]
        result = self.metagraph.get_devices_by_type("mytype", "name")
        self.assertEqual(1, len(result))

    def test_get_profile_devices_profile_not_found_raises_error(self):
        self.mock_match_nodes_ops.return_value = []
        with self.assertRaises(DataStoreException) as ex:
            self.metagraph.get_profile_devices("unknown")
        self.assertIn("no profile with name", str(ex.exception))

    def test_get_profile_devices_no_devices_returns_empty_list(self):
        mock_prof = create_mock_graph_node()
        self.mock_match_nodes_ops.return_value = [mock_prof]
        result = self.metagraph.get_profile_devices("prof1")
        self.assertEqual([], result)

    def test_get_profile_devices_two_devices(self):
        mock_prof = create_mock_graph_node()
        mock_node = create_mock_graph_node()
        self.mock_match_nodes_ops.return_value = [mock_prof]
        mock_prof.get_linked_nodes.return_value = [mock_node, mock_node]
        result = self.metagraph.get_profile_devices("prof1")
        self.assertEqual(2, len(result))

    def test_export_to_file(self):
        device_props = {'mac_address': '6', 'hostname': '4', 'ip_address': '5',
                        'device_type': {}, 'device_id': '1'}
        profile_props = {'profile_name': '1'}
        config_props = {
                '1': {},
                'log_file_path': '/tmp/datastore_export.json.log'
        }
        expected_export_json = {
            'device': [
                device_props
            ],
            'profile': [
                profile_props
            ],
            'configuration_variables': config_props
        }
        file_export_location = os.path.join(tempfile.gettempdir(), 'datastore_export.json')

        mock_device = create_mock_graph_node(device_props)
        mock_profile = create_mock_graph_node(profile_props)
        mock_config = create_mock_graph_node(config_props)
        self.mock_get_node.return_value = mock_config  # search for config
        self.mock_match_nodes_ops.side_effect = [
            [mock_profile],  # search for profiles
            [mock_device],   # search for devices
        ]

        self.metagraph.export_to_file(file_export_location)
        self.assertTrue(os.path.isfile(file_export_location))

        import json
        with open(file_export_location, 'r') as exported_file:
            exported_file_contents = json.load(exported_file)

        print(exported_file_contents)
        self.assertDictEqual(exported_file_contents, expected_export_json)
        os.remove(file_export_location)

    def test_import_from_file(self):
        import_file = tempfile.NamedTemporaryFile("w", delete=False)
        import_file.write("{}")
        import_file.close()
        self.metagraph.import_from_file(import_file.name)
        os.remove(import_file.name)

    def test_delete_database(self):
        self.metagraph._delete_database()
        # TODO
        # self.assertTrue(self.mock_remove_graph.called)

    # unimplemented functions
    # these could be implemented using extended get/set interface in MG (TBD)
    def test_get_device_history(self):
        with self.assertRaises(NotImplementedError):
            self.metagraph.get_device_history()

    def test_log_get(self):
        with self.assertRaises(NotImplementedError):
            self.metagraph.list_logs()

    def test_log_get_timeslice(self):
        with self.assertRaises(NotImplementedError):
            self.metagraph.list_logs_between_timeslice(datetime.utcnow(),
                                                       datetime.utcnow() - timedelta(days=1))

    def test_log_add(self):
        import logging
        with self.assertRaises(NotImplementedError):
            self.metagraph.add_log(logging.DEBUG, 'From BAT tests with love.', None, "BAT")
