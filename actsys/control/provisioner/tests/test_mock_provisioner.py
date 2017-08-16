# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Test the mock_resource_control plugin implementation.
"""
import unittest
import tempfile
import os
from mock import patch
from ..provisioner import ProvisionerException, Provisioner
from ..mock_provisioner import MockProvisioner


class MockProvisionerBase(object):
    """Test the MockResource class."""
    TEST_DEVICE1 = {"hostname": "test1"}
    TEST_DEVICE2 = {"hostname": "test2"}
    TEST_DEVICE3 = {"hostname": "test3"}

    def test_add(self):
        self.mp.add(self.TEST_DEVICE1)
        self.mp.add(self.TEST_DEVICE1)
        self.mp.add(self.TEST_DEVICE2)
        result = self.mp.add(self.TEST_DEVICE3)
        self.assertListEqual(self.mp.list(), [self.TEST_DEVICE1.get("hostname"),
                                              self.TEST_DEVICE2.get("hostname"),
                                              self.TEST_DEVICE3.get("hostname")])
        self.assertTrue(result.get(self.mp.PROVISIONER_KEY))

    def test_list(self):
        self.mp.add(self.TEST_DEVICE1)
        self.assertEqual(self.mp.list(), [self.TEST_DEVICE1.get("hostname")])

    def test_remove(self):
        self.mp.add(self.TEST_DEVICE1)
        self.mp.add(self.TEST_DEVICE1)
        self.mp.add(self.TEST_DEVICE2)
        self.mp.add(self.TEST_DEVICE3)
        self.assertListEqual(self.mp.list(), [self.TEST_DEVICE1.get("hostname"),
                                              self.TEST_DEVICE2.get("hostname"),
                                              self.TEST_DEVICE3.get("hostname")])

        self.mp.delete(self.TEST_DEVICE2)
        self.assertListEqual(self.mp.list(), [self.TEST_DEVICE1.get("hostname"),
                                              self.TEST_DEVICE3.get("hostname")])

        self.mp.delete(self.TEST_DEVICE2)
        self.assertListEqual(self.mp.list(), [self.TEST_DEVICE1.get("hostname"),
                                              self.TEST_DEVICE3.get("hostname")])
        self.mp.delete(self.TEST_DEVICE3)
        self.assertListEqual(self.mp.list(), [self.TEST_DEVICE1.get("hostname")])

    def test_remove2(self):
        device = self.mp.delete(self.TEST_DEVICE1)
        self.assertEqual(device, self.TEST_DEVICE1)

    def test_set_network_interface(self):
        device = {}
        self.mp.set_ip_address(device, "ipa")
        self.assertEqual(device.get("ip_address"), "ipa")

        self.mp.set_ip_address(device, "ipa2", "enps606")
        self.assertEqual(device.get("enps606_ip_address"), "ipa2")

        self.mp.set_ip_address(device, "ipa")
        self.assertEqual(device.get("ip_address"), "ipa")

        self.mp.set_ip_address(device, None)
        self.assertIsNone(device.get("ip_address"))

        self.mp.set_ip_address(device, None, "interface2")
        self.assertIsNone(device.get("interface2_ip_address"))

    def test_set_hardware_address(self):
        device = {}
        self.mp.set_hardware_address(device, "00:00")
        self.assertEqual(device.get("mac_address"), "00:00")

        self.mp.set_hardware_address(device, "00:11", "interface2")
        self.assertEqual(device.get("interface2_mac_address"), "00:11")

        self.mp.set_hardware_address(device, None)
        self.assertIsNone(device.get("mac_address"))

        self.mp.set_hardware_address(device, None, "interface2")
        self.assertIsNone(device.get("interface2_mac_address"))

    def test_set_image(self):
        device = {}
        self.mp.set_image(device, "centos7.3")
        self.assertEqual(device.get(self.mp.PROVISIONER_IMAGE_KEY), "centos7.3")
        self.mp.set_image(device, "SLES12sp1")
        self.assertEqual(device.get(self.mp.PROVISIONER_IMAGE_KEY), "SLES12sp1")
        self.mp.set_image(device, None)
        self.assertIsNone(device.get(self.mp.PROVISIONER_IMAGE_KEY))

        with self.assertRaises(ProvisionerException):
            self.mp.set_image(device, "1invalid")

    def test_list_images(self):
        device = {}
        self.mp.set_image(device, "Centos7.3")
        self.assertListEqual(self.mp.list_images(), ["Centos7.3"])
        self.mp.set_image(device, "SLES12sp1")
        self.assertListEqual(self.mp.list_images(), ["Centos7.3", "SLES12sp1"])
        self.mp.set_image(device, None)
        self.assertListEqual(self.mp.list_images(), ["Centos7.3", "SLES12sp1"])

    def test_set_bootstrap(self):
        device = {}
        self.mp.set_bootstrap(device, "foo")
        self.assertEqual(device.get(self.mp.PROVISIONER_BOOTSTRAP_KEY), "foo")
        self.mp.set_bootstrap(device, "bar")
        self.assertEqual(device.get(self.mp.PROVISIONER_BOOTSTRAP_KEY), "bar")
        self.mp.set_bootstrap(device, None)
        self.assertIsNone(device.get(self.mp.PROVISIONER_BOOTSTRAP_KEY))

    def test_set_files(self):
        device = {}
        self.mp.set_files(device, "foo,hi,lo")
        self.assertEqual(device.get(self.mp.PROVISIONER_FILE_KEY), "foo,hi,lo")
        self.mp.set_files(device, "bar")
        self.assertEqual(device.get(self.mp.PROVISIONER_FILE_KEY), "bar")
        self.mp.set_files(device, None)
        self.assertIsNone(device.get(self.mp.PROVISIONER_FILE_KEY))

    def test_set_kernel_args(self):
        device = {}
        self.mp.set_kernel_args(device, "foo,hi,lo")
        self.assertEqual(device.get(self.mp.PROVISIONER_KARGS_KEY), "foo,hi,lo")
        self.mp.set_kernel_args(device, "bar")
        self.assertEqual(device.get(self.mp.PROVISIONER_KARGS_KEY), "bar")
        self.mp.set_kernel_args(device, None)
        self.assertIsNone(device.get(self.mp.PROVISIONER_KARGS_KEY))


class TestMockProvisioner(MockProvisionerBase, unittest.TestCase):

    def setUp(self):
        self.mp = MockProvisioner()

    def test_init(self):
        MockProvisioner()

class TestMockProvisionerWithFile(MockProvisionerBase, unittest.TestCase):

    def setUp(self):
        self.file = tempfile.NamedTemporaryFile("w", delete=False)
        self.file.write("{}")
        self.file.close()

        self.mp = MockProvisioner(file_location=self.file.name)

    def tearDown(self):
        os.remove(self.file.name)


class TestProvisioner(unittest.TestCase):

    def setUp(self):
        self.old_abstract_methods = Provisioner.__abstractmethods__ = set()
        self.provisioner = Provisioner()

    def tearDown(self):
        Provisioner.__abstractmethods__ = self.old_abstract_methods

    def test_patcher(self):
        self.assertTrue(isinstance(self.provisioner, Provisioner))

    def test_provisioner(self):
        self.provisioner.add({})
        self.provisioner.delete({})
        self.provisioner.set_ip_address(None, None)
        self.provisioner.set_hardware_address(None, None)
        self.provisioner.set_image(None, None)
        self.provisioner.set_bootstrap(None, None)
        self.provisioner.set_files(None, None)
        self.provisioner.set_kernel_args(None, None)
        self.provisioner.list()
        self.provisioner.list_images()

        try:
            raise ProvisionerException("Foo")
        except ProvisionerException as pe:
            self.assertEqual(str(pe), "'Foo'")
