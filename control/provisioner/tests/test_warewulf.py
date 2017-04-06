# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Test the mock_resource_control plugin implementation.
"""
import unittest
import textwrap
from mock import patch
from ..provisioner import ProvisionerException, Provisioner
from ..warewulf_provisioner import Warewulf
from ...utilities import Utilities, SubprocessOutput


class TestWarewulfProvisioner(unittest.TestCase):

    def setUp(self):
        # self.self.mock_esub = mock_execute_subprocess
        self.mock_deip_patcher = patch.object(Warewulf, "device_exists_in_provisioner")
        self.mock_deip = self.mock_deip_patcher.start()
        self.mock_esub_patcher = patch.object(Utilities, "execute_subprocess")
        self.mock_esub = self.mock_esub_patcher.start()
        self.warewulf = Warewulf()

    def tearDown(self):
        self.mock_deip_patcher.stop()
        self.mock_esub_patcher.stop()

    def test_init(self):
        Warewulf()

    def test_list_images(self):
        # textwrap.dedent magic: http://stackoverflow.com/a/1412728/1767377
        expected_output = textwrap.dedent("""\
        VNFS NAME            SIZE (M) CHROOT LOCATION
        custom               16.1     /root/imgs/custom
        redhat7.3            1672.2   /opt/intel/hpc-orchestrator/admin/images/redhat7.3
        centos7.3            407.1    /opt/intel/hpc-orchestrator/admin/images/centos7.3
        sles12sp1            1217.4   /opt/intel/hpc-orchestrator/admin/images/sles12sp1""")
        self.mock_esub.return_value = SubprocessOutput(0, expected_output, None)
        self.assertListEqual(self.warewulf.list_images(), ['custom', 'redhat7.3', 'centos7.3', 'sles12sp1'])

    def test_list(self):
        expected_output = textwrap.dedent("""\
        NAME                GROUPS              IPADDR              HWADDR
        ================================================================================
        test1               NodePool            192.168.1.11        00:1e:67:f9:ba:35
        test2               NodePool            192.168.1.50,192.168.2.50 00:1e:67:f9:ca:4d
        test3               UNDEF""")
        self.mock_esub.return_value = SubprocessOutput(0, expected_output, None)
        self.assertListEqual(self.warewulf.list(), ['test1', 'test2', 'test3'])

    def test_set_image(self):
        device = {"hostname": "test-1"}

        # device not known to warewulf
        self.mock_deip.return_value = False
        with self.assertRaises(ProvisionerException):
            self.warewulf.set_image(device, "foo")

        self.mock_deip.return_value = True
        expected_output = "ERROR:  No VNFS named: <image>"
        self.mock_esub.return_value = SubprocessOutput(1, None, expected_output)
        with self.assertRaises(ProvisionerException):
            self.warewulf.set_image(device, "foo")

        expected_output = textwrap.dedent("""\
        DBD::mysql::st execute failed: UPDATE command denied to user 'user'@'localhost' for table 'datastore' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 447.
        DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'lookup' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 450.
        DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'lookup' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 472.
        DBD::mysql::st execute failed: UPDATE command denied to user 'user'@'localhost' for table 'datastore' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 447.
        DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'lookup' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 450.
        DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'lookup' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 472.
        DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'binstore' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 600.
        DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'binstore' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 604.
        ERROR:  put_chunk() failed with error:  INSERT command denied to user 'user'@'localhost' for table 'binstore'
        WARNING:  Could not open /etc/hosts: Permission denied""")
        self.mock_esub.return_value = SubprocessOutput(0, None, expected_output)
        with self.assertRaises(ProvisionerException):
            self.warewulf.set_image(device, "foo")

        self.mock_esub.return_value = SubprocessOutput(0, None, None)
        self.warewulf.set_image(device, "some_image")
        self.assertEqual(device.get(Provisioner.PROVISIONER_IMAGE_KEY), "some_image")

        device.pop(Provisioner.PROVISIONER_IMAGE_KEY)

        self.mock_esub.return_value = SubprocessOutput(0, '', None)
        self.warewulf.set_image(device, "some_image2")
        self.assertEqual(device.get(Provisioner.PROVISIONER_IMAGE_KEY), "some_image2")

        self.mock_esub.return_value = SubprocessOutput(0, None, None)
        self.warewulf.set_image(device, None)
        self.assertIsNone(device.get(Provisioner.PROVISIONER_IMAGE_KEY))

    def test_set_ip_address(self):
        device = {"hostname": "test-1", "mac_address": "00:00:00:00:00:01"}

        # No hostname
        with self.assertRaises(ProvisionerException):
            self.warewulf.set_ip_address({}, "foo")

        # device not known to warewulf
        self.mock_deip.return_value = False
        with self.assertRaises(ProvisionerException):
            self.warewulf.set_ip_address(device, "foo")

        # Invalid IP Address
        with self.assertRaises(ProvisionerException):
            self.warewulf.set_ip_address(device, "invalid_ip")

        self.mock_deip.return_value = True
        self.mock_esub.return_value = SubprocessOutput(0, None, None)
        self.warewulf.set_ip_address(device, "127.0.0.1")
        self.assertEqual(device.get("ip_address"), "127.0.0.1", device)

        self.mock_deip.return_value = True
        self.mock_esub.return_value = SubprocessOutput(0, None, None)
        self.warewulf.set_ip_address(device, None)
        self.assertIsNone(device.get("ip_address"))
        self.assertIsNotNone(device.get("mac_address"))

        self.mock_esub.return_value = SubprocessOutput(0, '', '')
        self.warewulf.set_ip_address(device, "127.0.0.2")
        self.assertEqual(device.get("ip_address"), "127.0.0.2", device)

        self.mock_esub.return_value = SubprocessOutput(0, None, None)
        self.warewulf.set_ip_address(device, "127.0.0.11", "ensp6f0")
        self.assertEqual(device.get("ensp6f0_ip_address"), "127.0.0.11")

        expected_output = """\
        NAME                       NETDEVS.ETH0.IPADDR
        ======================================================
        test-1                     UNDEF

        About to apply 1 action(s) to 1 object(s):

             DEL: NETDEVS.eth0.IPADDR  = [ALL]

        Proceed?
        """
        expected_stderr = """\
        DBD::mysql::st execute failed: UPDATE command denied to user 'user'@'localhost' for table 'datastore' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 447.
        DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'lookup' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 450.
        DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'lookup' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 472.
        DBD::mysql::st execute failed: UPDATE command denied to user 'user'@'localhost' for table 'datastore' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 447.
        DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'lookup' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 450.
        DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'lookup' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 472.
        DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'binstore' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 600.
        DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'binstore' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 604.
        ERROR:  put_chunk() failed with error:  INSERT command denied to user 'user'@'localhost' for table 'binstore'
        WARNING:  Could not open /etc/hosts: Permission denied"""
        self.mock_esub.return_value = SubprocessOutput(0, expected_output, expected_stderr)
        with self.assertRaises(ProvisionerException):
            self.warewulf.set_ip_address(device, "127.0.0.11", "ensp6f0")

        self.mock_esub.return_value = SubprocessOutput(1, None, None)
        with self.assertRaises(ProvisionerException):
            self.warewulf.set_ip_address(device, "127.0.0.11", "ensp6f0")

    def test_delete(self):
        self.mock_deip.return_value = True
        expected_output = textwrap.dedent("""\
        About to apply 1 action(s) to 1 node(s):

             DEL: NODE test1

        Proceed?
        Deleted 1 nodes.""")
        self.mock_esub.return_value = SubprocessOutput(0, expected_output, None)
        result = self.warewulf.delete({"hostname": "test1", Provisioner.DEVICE_ADDED_TO_PROVISIONER_KEY: True})
        self.assertEqual({"hostname": "test1"}, result)

        expected_output = textwrap.dedent("""\
        About to apply 1 action(s) to 1 node(s):

             DEL: NODE test1

        Proceed?
        Deleted 2 nodes.""")
        self.mock_esub.return_value = SubprocessOutput(0, expected_output, None)
        with self.assertRaises(ProvisionerException):
            result = self.warewulf.delete({"hostname": "test1", Provisioner.DEVICE_ADDED_TO_PROVISIONER_KEY: True})

        self.mock_deip.return_value = False
        self.mock_esub.return_value = SubprocessOutput(1, '', None)
        result = self.warewulf.delete({"hostname": "test1", Provisioner.DEVICE_ADDED_TO_PROVISIONER_KEY: True})
        self.assertEqual({"hostname": "test1"}, result)

    def test_set_bootstrap(self):
        device = {"hostname": "test-1"}

        # Device not known to warewulf
        self.mock_deip.return_value = False
        with self.assertRaises(ProvisionerException):
            self.warewulf.set_bootstrap(device, "foo")

        self.mock_deip.return_value = True
        expected_output = "ERROR:  No bootstrap named: foo"
        self.mock_esub.return_value = SubprocessOutput(1, None, expected_output)
        with self.assertRaises(ProvisionerException):
            self.warewulf.set_bootstrap(device, "foo")

        expected_output = textwrap.dedent("""\
                DBD::mysql::st execute failed: UPDATE command denied to user 'user'@'localhost' for table 'datastore' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 447.
                DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'lookup' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 450.
                DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'lookup' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 472.
                DBD::mysql::st execute failed: UPDATE command denied to user 'user'@'localhost' for table 'datastore' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 447.
                DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'lookup' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 450.
                DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'lookup' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 472.
                DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'binstore' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 600.
                DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'binstore' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 604.
                ERROR:  put_chunk() failed with error:  INSERT command denied to user 'user'@'localhost' for table 'binstore'
                WARNING:  Could not open /etc/hosts: Permission denied""")
        self.mock_esub.return_value = SubprocessOutput(0, None, expected_output)
        with self.assertRaises(ProvisionerException):
            self.warewulf.set_bootstrap(device, "foo")

        self.mock_esub.return_value = SubprocessOutput(0, None, None)
        self.warewulf.set_bootstrap(device, "some_bootstrap")
        self.assertEqual(device.get(Provisioner.PROVISIONER_BOOTSTRAP_KEY), "some_bootstrap")

        self.mock_esub.return_value = SubprocessOutput(0, '', None)
        self.warewulf.set_bootstrap(device, "some_bootstrap2")
        self.assertEqual(device.get(Provisioner.PROVISIONER_BOOTSTRAP_KEY), "some_bootstrap2")

        self.mock_esub.return_value = SubprocessOutput(0, None, None)
        self.warewulf.set_bootstrap(device, None)
        self.assertIsNone(device.get(Provisioner.PROVISIONER_BOOTSTRAP_KEY))

    def test_set_hardware_address(self):
        device = {"hostname": "test-1", "ip_address": "192.168.123.123"}

        # No hostname
        with self.assertRaises(ProvisionerException):
            self.warewulf.set_hardware_address({}, "foo")

        # device not known to warewulf
        self.mock_deip.return_value = False
        with self.assertRaises(ProvisionerException):
            self.warewulf.set_hardware_address(device, "foo")

        self.mock_deip.return_value = True

        # Invalid HW Address
        self.mock_esub.return_value = SubprocessOutput(1, None, "ERROR:  Option 'hwaddr' has invalid characters")
        with self.assertRaises(ProvisionerException):
            self.warewulf.set_hardware_address(device, "invalid_hardware_address")

        self.mock_esub.return_value = SubprocessOutput(0, None, None)
        self.warewulf.set_hardware_address(device, "00:00:00:00:00:00")
        self.assertEqual(device.get("mac_address"), "00:00:00:00:00:00", device)

        self.mock_esub.return_value = SubprocessOutput(0, None, None)
        self.warewulf.set_hardware_address(device, None)
        self.assertIsNone(device.get("mac_address"))
        self.assertEqual(device.get("ip_address"), "192.168.123.123")

        self.mock_esub.return_value = SubprocessOutput(0, '', '')
        self.warewulf.set_hardware_address(device, "00:00:00:00:00:01")
        self.assertEqual(device.get("mac_address"), "00:00:00:00:00:01", device)

        self.mock_esub.return_value = SubprocessOutput(0, None, None)
        self.warewulf.set_hardware_address(device, "00:00:00:00:00:11", "ensp6f0")
        self.assertEqual(device.get("ensp6f0_mac_address"), "00:00:00:00:00:11")

        expected_output = """\
        NAME                       NETDEVS.ETH0.HWADDR
        ======================================================
        test-1                     UNDEF

        About to apply 1 action(s) to 1 object(s):

             DEL: NETDEVS.eth0.HWADDR  = [ALL]

        Proceed?
        """
        expected_stderr = """\
        DBD::mysql::st execute failed: UPDATE command denied to user 'user'@'localhost' for table 'datastore' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 447.
        DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'lookup' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 450.
        DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'lookup' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 472.
        DBD::mysql::st execute failed: UPDATE command denied to user 'user'@'localhost' for table 'datastore' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 447.
        DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'lookup' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 450.
        DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'lookup' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 472.
        DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'binstore' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 600.
        DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'binstore' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 604.
        ERROR:  put_chunk() failed with error:  INSERT command denied to user 'user'@'localhost' for table 'binstore'
        WARNING:  Could not open /etc/hosts: Permission denied"""
        self.mock_esub.return_value = SubprocessOutput(0, expected_output, expected_stderr)
        with self.assertRaises(ProvisionerException):
            self.warewulf.set_hardware_address(device, "00:00:00:00:00:00", "ensp6f0")

        self.mock_esub.return_value = SubprocessOutput(1, None, None)
        with self.assertRaises(ProvisionerException):
            self.warewulf.set_hardware_address(device, "00:00:00:00:00:00", "ensp6f0")

    def test_add(self):
        self.mock_deip.return_value = False
        # Negative case
        self.mock_esub.return_value = SubprocessOutput(1, None, None)
        with self.assertRaises(ProvisionerException):
            self.warewulf.add({"hostname": "test-1"})

        # Negative case
        self.mock_esub.return_value = SubprocessOutput(56, 'foo', 'bar')
        with self.assertRaises(ProvisionerException):
            self.warewulf.add({"hostname": "test-1"})

        # Negative case
        expected_output = textwrap.dedent("""\
        DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'datastore' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 434.
        DBD::mysql::st execute failed: UPDATE command denied to user 'user'@'localhost' for table 'datastore' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 447.
        DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'lookup' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 450.
        DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'lookup' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 472.
        DBD::mysql::st execute failed: UPDATE command denied to user 'user'@'localhost' for table 'datastore' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 447.
        DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'lookup' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 450.
        DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'lookup' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 472.
        DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'binstore' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 600.
        DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'binstore' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 604.
        ERROR:  put_chunk() failed with error:  INSERT command denied to user 'user'@'localhost' for table 'binstore'
        WARNING:  Could not open /etc/hosts: Permission denied""")
        self.mock_esub.return_value = SubprocessOutput(0, None, expected_output)
        with self.assertRaises(ProvisionerException):
            self.warewulf.add({"hostname": "test-1"})

        # Positive case
        self.mock_esub.return_value = SubprocessOutput(0, '', '')
        device = self.warewulf.add({"hostname": "test-1"})
        self.assertTrue(device.get(Provisioner.DEVICE_ADDED_TO_PROVISIONER_KEY))

        # Positive case
        self.mock_esub.return_value = SubprocessOutput(0, None, None)
        device = self.warewulf.add({"hostname": "test-1"})
        self.assertTrue(device.get(Provisioner.DEVICE_ADDED_TO_PROVISIONER_KEY))

        self.mock_deip.return_value = True

        # Positive case
        self.mock_esub.return_value = SubprocessOutput(0, '', '')
        device = self.warewulf.add({"hostname": "test-1"})
        self.assertTrue(device.get(Provisioner.DEVICE_ADDED_TO_PROVISIONER_KEY))

        # Positive case
        self.mock_esub.return_value = SubprocessOutput(0, None, None)
        device = self.warewulf.add({"hostname": "test-1"})
        self.assertTrue(device.get(Provisioner.DEVICE_ADDED_TO_PROVISIONER_KEY))

    def test_set_files(self):
        device = {"hostname": "test-1"}

        # device not known to warewulf
        self.mock_deip.return_value = False
        with self.assertRaises(ProvisionerException):
            self.warewulf.set_files(device, "foo")

        self.mock_deip.return_value = True
        expected_output = "ERROR:  No file found for name: foo"
        self.mock_esub.return_value = SubprocessOutput(1, None, expected_output)
        with self.assertRaises(ProvisionerException):
            self.warewulf.set_files(device, "foo")

        expected_output = textwrap.dedent("""\
        DBD::mysql::st execute failed: UPDATE command denied to user 'user'@'localhost' for table 'datastore' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 447.
        DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'lookup' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 450.
        DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'lookup' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 472.
        DBD::mysql::st execute failed: UPDATE command denied to user 'user'@'localhost' for table 'datastore' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 447.
        DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'lookup' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 450.
        DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'lookup' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 472.
        DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'binstore' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 600.
        DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'binstore' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 604.
        ERROR:  put_chunk() failed with error:  INSERT command denied to user 'user'@'localhost' for table 'binstore'
        WARNING:  Could not open /etc/hosts: Permission denied""")
        self.mock_esub.return_value = SubprocessOutput(0, None, expected_output)
        with self.assertRaises(ProvisionerException):
            self.warewulf.set_files(device, "foo")

        self.mock_esub.return_value = SubprocessOutput(0, None, None)
        self.warewulf.set_files(device, "some_file")
        self.assertEqual(device.get(Provisioner.PROVISIONER_FILE_KEY), "some_file")

        self.mock_esub.return_value = SubprocessOutput(0, '', None)
        self.warewulf.set_files(device, "some_file,some_file2")
        self.assertEqual(device.get(Provisioner.PROVISIONER_FILE_KEY), "some_file,some_file2")

        self.mock_esub.return_value = SubprocessOutput(0, None, None)
        self.warewulf.set_files(device, None)
        self.assertIsNone(device.get(Provisioner.PROVISIONER_FILE_KEY))

    def test_set_kernel_args(self):
        device = {"hostname": "test-1"}

        # device not known to warewulf
        self.mock_deip.return_value = False
        with self.assertRaises(ProvisionerException):
            self.warewulf.set_kernel_args(device, "foo")

        self.mock_deip.return_value = True
        expected_output = textwrap.dedent("""\
        DBD::mysql::st execute failed: UPDATE command denied to user 'user'@'localhost' for table 'datastore' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 447.
        DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'lookup' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 450.
        DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'lookup' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 472.
        DBD::mysql::st execute failed: UPDATE command denied to user 'user'@'localhost' for table 'datastore' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 447.
        DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'lookup' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 450.
        DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'lookup' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 472.
        DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'binstore' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 600.
        DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'binstore' at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 604.
        ERROR:  put_chunk() failed with error:  INSERT command denied to user 'user'@'localhost' for table 'binstore'
        WARNING:  Could not open /etc/hosts: Permission denied""")
        self.mock_esub.return_value = SubprocessOutput(0, None, expected_output)
        with self.assertRaises(ProvisionerException):
            self.warewulf.set_kernel_args(device, "foo")

        self.mock_esub.return_value = SubprocessOutput(0, None, None)
        self.warewulf.set_kernel_args(device, "some_arg")
        self.assertEqual(device.get(Provisioner.PROVISIONER_KARGS_KEY), "some_arg")

        self.mock_esub.return_value = SubprocessOutput(0, '', None)
        self.warewulf.set_kernel_args(device, "console=tty01,1153295")
        self.assertEqual(device.get(Provisioner.PROVISIONER_KARGS_KEY), "console=tty01,1153295")

        self.mock_esub.return_value = SubprocessOutput(0, None, None)
        self.warewulf.set_kernel_args(device, None)
        self.assertIsNone(device.get(Provisioner.PROVISIONER_KARGS_KEY))
