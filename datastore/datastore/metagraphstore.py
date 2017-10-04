# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
For handling the DataStore interface using MetaGraph
"""

# import json
# import copy
import logging
# import datetime
# import psycopg2
# from ClusterShell.NodeSet import NodeSet, RESOLVER_NOGROUP
import json
from .datastore import DataStore, DataStoreException
from .utilities import DataStoreUtilities
from metagraph.graph_tools.create_graph import create_graph
from metagraph.graph_tools.remove_graph import remove_graph
from metagraph.mg_handler.mg_handler import MGNode
from metagraph.match_nodes.mg_match_nodes import MGNodeMatcher
from metagraph.match_nodes.mg_search_operators import AllOf


unique_id = 0


# TODO: fix this: devices need a unique link name (device_id) to be added
def make_new_unique_id():
    global unique_id
    unique_id += 1
    return str(unique_id)


class MetagraphStore(DataStore):
    """
    Data Store interface.
    """

    def __init__(self, location, log_level=None):
        """
        Creates the object with parameters passed in.
        :param location:
        :param log_level:
        """
        super(MetagraphStore, self).__init__()

        # TODO: create or connect to graph
        # TODO: what arguments are needed here?
        self.graph_name = "DataStore"
        try:
            self.root = MGNode(self.graph_name)
        except:
            create_graph(self.graph_name)
            self.root = MGNode(self.graph_name)
        self.matcher = MGNodeMatcher(self.graph_name)

        self.log_level = log_level if log_level is not None else DataStore.LOG_LEVEL

    def get_device(self, device_name):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(MetagraphStore, self).get_device(device_name)
        results = self.matcher.match_nodes_using_operators(AllOf({"hostname": device_name, "type": "device"}))

        if len(results) == 0:
            return None
        if len(results) > 1:
            raise DataStoreException("Found duplicate device for hostname: " + device_name)

        return results[0].get_properties()

    def list_devices(self, filters=None):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(MetagraphStore, self).list_devices(filters)
        props = {"type": "device"}
        if filters is not None:
            props.update(filters)
        results = self.matcher.match_nodes_using_operators(AllOf(props))
        return [r.get_properties() for r in results]

    def set_device(self, device_info_list):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(MetagraphStore, self).set_device(device_info_list)

        if not isinstance(device_info_list, list):
            device_info_list = [device_info_list]

        set_ids = list()
        for dev in device_info_list:
            dev["type"] = "device"
            matches = []
            dev_id = make_new_unique_id()
            if "device_id" in dev:
                dev_id = dev["device_id"]
                # look up device
                matches = self.matcher.match_nodes_using_operators(AllOf({"device_id": dev_id}))
                set_ids.append(dev_id)
            if matches:
                # update existing
                # TODO: throw if duplicates
                for m in matches:
                    m.set_properties(dev)
            else:
                # TODO: add to a better place than just the root
                self.root.add_node(link_name=dev_id, back_link_name="root", properties=dev)

        return set_ids

    def delete_device(self, device_list):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(MetagraphStore, self).delete_device(device_list)
        if not isinstance(device_list, list):
            device_list = [device_list]

        deleted_device_ids = list()

        for dev in device_list:
            stmt = AllOf({"type": "device", "device_id": device_list})  # use AND/OR to check id/name
            matches = self.matcher.match_nodes_using_operators(stmt)
            for m in matches:
                dev_id = m.get_properties()["device_id"]
                deleted_device_ids.append(int(dev_id))
                self.root.remove_node(dev_id)
        return deleted_device_ids

    def get_device_history(self, device_name=None):
        super(MetagraphStore, self).list_devices(device_name)
        raise NotImplementedError

    def get_profile(self, profile_name):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(MetagraphStore, self).get_profile(profile_name)
        stmt = AllOf({"type": "profile", "profile_name": profile_name})
        profiles = self.matcher.match_nodes_using_operators(stmt)

        if len(profiles) < 1:
            return None
        return profiles[0].get_properties()

    def list_profiles(self, filters=None):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(MetagraphStore, self).list_profiles(filters)
        stmt = AllOf({"type": "profile"})
        profiles = self.matcher.match_nodes_using_operators(stmt)

        return [p.get_properties() for p in profiles]

    def set_profile(self, profile_info):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(MetagraphStore, self).set_profile(profile_info)
        prof_name = profile_info["profile_name"]

        stmt = AllOf({"type": "profile", "profile_name": prof_name})
        profiles = self.matcher.match_nodes_using_operators(stmt)

        if profiles:
            for p in profiles:
                p.set_properties(profile_info)
        else:
            profile_info["type"] = "profile"  # TODO: is this safe? necessary?  maybe have a bucket of profiles instead
            self.root.add_node(link_name=prof_name, back_link_name="root", properties=profile_info)
        return prof_name

    def delete_profile(self, profile_name):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(MetagraphStore, self).delete_profile(profile_name)

        stmt = AllOf({"type": "profile", "profile_name": profile_name})
        profiles = self.matcher.match_nodes_using_operators(stmt)

        # TODO: should only be one match
        if len(profiles) < 1:
            return None
        else:
            self.root.remove_node(profile_name)
            return profile_name

    def list_logs(self, device_name=None, limit=100):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(MetagraphStore, self).list_logs(device_name, limit)
        raise NotImplementedError

    def list_logs_between_timeslice(self, begin, end, device_name=None, limit=100):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(MetagraphStore, self).list_logs_between_timeslice(begin, end, device_name, limit)
        raise NotImplementedError

    def add_log(self, level, msg, device_name=None, process=None):
        """
        See @DataStore for function description. Only implementation details here.

        No logging should happen inside this function... or it would be a recersive loop.
        """
        super(MetagraphStore, self).add_log(level, msg, device_name, process)
        raise NotImplementedError

    def get_configuration_value(self, key):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(MetagraphStore, self).get_configuration_value(key)
        # TODO: should all config be saved in the same place? or separate nodes for each?
        try:
            config = self.root.get_node("config")
            raw_config = config.get_properties()[key]
            try:
                return json.loads(raw_config)
            except:
                return raw_config
        except BaseException as ex:
            print(ex)
            return None

    def list_configuration(self):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(MetagraphStore, self).list_configuration()
        try:
            config = self.root.get_node("config")
            return [config.get_properties()]
        except:
            return []

    def set_configuration(self, key, value):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(MetagraphStore, self).set_configuration(key, value)
        try:
            config = self.root.get_node("config")
        except:
            config = self.root.add_node("config", "root")

        value = json.dumps(value)  # TODO: how to deal with nested configs
        print(value, type(value))
        config.set_properties({key: value})
        return key

    def delete_configuration(self, key):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(MetagraphStore, self).delete_configuration(key)

        # There is no way to remove a property completely in MG. If the schema for
        # storing config changes, this could work, or if MG adds an API for removing properties.
        raise NotImplementedError

    def list_groups(self):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(MetagraphStore, self).list_groups()
        groups = self.matcher.match_nodes_using_operators(AllOf({"type": "group"}))
        return groups

    def get_group_devices(self, group):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(MetagraphStore, self).get_group_devices(group)
        groups = self.matcher.match_nodes_using_operators(AllOf({"type": "group", "group_name": group}))
        # TODO: check for duplicates
        if len(groups) < 1:
            return None
        group = groups[0]
        # TODO: need to filter out devices only
        nodes = group.get_linked_nodes()
        return nodes

    def add_to_group(self, device_list, group):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(MetagraphStore, self).add_to_group(device_list, group)

        groups = self.matcher.match_nodes_using_operators(AllOf({"type": "group", "group_name": group}))
        print(groups)
        # TODO: check for duplicates
        if len(groups) < 1:
            raise DataStoreException("no group with name "+group)
        group = groups[0]
        updated_devices = []
        links = group.get_linked_nodes()
        in_group = [n.get_properties()["device_id"] for n in links]
        print(in_group)
        for dev in device_list:
            if dev in in_group:
                pass
            else:
                devices = self.matcher.match_nodes_using_operators(AllOf({"device_id": dev}))
                for d in devices:
                    pass
            updated_devices.append(dev)

        return updated_devices

    def remove_from_group(self, device_list, group):
        """
        See @DataStore for function description. Only implementation details here.
        """
        super(MetagraphStore, self).remove_from_group(device_list, group)
        groups = self.matcher.match_nodes_using_operators(AllOf({"type": "group", "name": group}))
        # TODO: expect only one match
        if len(groups) < 1:
            raise DataStoreException("Group {} doesn't exist".format(group))
        group = groups[0]
        nodes_in_group = group.get_linked_nodes()
        remaining = []
        for n in nodes_in_group:
            nid = n.get_properties()["device_id"]
            if nid in device_list:
                group.remove_link(nid)
            else:
                remaining.append(nid)

        return remaining

    # CANNED QUERIES
    def get_devices_by_type(self, device_type, device_name=None):
        """
                See @DataStore for function description. Only implementation details here.
        """
        super(MetagraphStore, self).get_devices_by_type(device_type, device_name)
        props = {"type": device_type}
        if device_name is not None:
            props["name"] = device_name
        devices = self.matcher.match_nodes_using_operators(AllOf(props))
        return [d.get_properties() for d in devices]

    def get_profile_devices(self, profile_name):
        """
        Overrides base class implementation.
        A list of devices that have a given profile.
        :param profile_name:
        :return:
        """
        profiles = self.matcher.match_nodes_using_operators(AllOf({"profile_name": profile_name}))

        # TODO: handle multiple matches
        if len(profiles) < 1:
            raise DataStoreException("no profile with name {}".format(profile_name))
        # TODO: only match connected devices
        devices = profiles[0].get_linked_nodes()
        return [d.get_properties() for d in devices]

    def export_to_file(self, file_location):
        """
        See @DataStore for function description. Only implementation details here.

        Exporting from the database to a file uses the filestore.
        """
        from .filestore import FileStore

        file = open(file_location, 'w')
        file.write('{ "configuration_variables": { "log_file_path": "' + file_location + '.log" } }')
        file.close()
        export_fs = FileStore(file_location, self.log_level)

        configuration = self.list_configuration()
        for config in configuration:
            for k, v in config.items():
                export_fs.set_configuration(k, v)

        profiles = self.list_profiles()
        for profile in profiles:
            export_fs.set_profile(profile)

        devices = self.list_devices()
        for device in devices:
            # Removing device_history artifact
            device.pop("sys_period", None)
            export_fs.set_device(device)

        export_fs.save_file()

    def import_from_file(self, file_location):
        """
        See @DataStore for function description. Only implementation details here.

        Importing from a file uses the filestore to collect valid items.
        """
        from .filestore import FileStore

        # Check that we can parse and use this file for importing
        fs = FileStore(file_location, self.log_level)

        # Delete everything from current DB
        self.logger.info("Importing from file: Deleting old info")
        old_config, old_devices, old_profiles = self._delete_database()

        # import the new stuff
        try:
            self.logger.info("Importing from file: Importing File info")
            config_list = fs.list_configuration()
            for config in config_list:
                self.set_configuration(config["key"], config["value"])

            profiles = fs.list_profiles()
            for profile in profiles:
                self.set_profile(profile)

            devices = fs.list_devices()
            for device in devices:
                self.set_device(device)
        except Exception as ex:
            # Rollback any changes by closing the cursor / connection
            self.connect()
            # revert!
            self.logger.info("Importing from file: Reverting actions due to: {}".format(ex))
            self.logger.info("Importing from file: Clearing the database")
            self._delete_database()
            self.logger.info("Importing from file: Reverting config")
            for config in old_config:
                self.set_configuration(config["key"], config["value"])

            self.logger.info("Importing from file: Reverting profiles:")
            for profile in old_profiles:
                self.set_profile(profile)

            self.logger.info("Importing from file: Reverting devices:")
            for device in old_devices:
                self.set_device(device)

            # raise the exception that happened earlier
            raise

    def _delete_database(self):
        old_config = self.list_configuration()
        old_devices = self.list_devices()
        old_profiles = self.list_profiles()
        remove_graph(self.graph_name)
        return old_config, old_devices, old_profiles
