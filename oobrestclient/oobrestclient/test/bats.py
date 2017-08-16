"""Long, slow BAT tests for the whole BKY-REST stack: Server, client, plugins"""
import os
import re
import subprocess
import time
from unittest import TestCase

import requests
from mock import patch

from ..nc_api import NodeController, ConnectError


class TestBushKeyStack(TestCase):
    """Single test suite containing all BAT tests for the BKY stack"""

    def setUp(self):
        self.bat_path = os.path.dirname(os.path.realpath(__file__))
        self.setup_test_values()
        self.setup_server_process()

    def setup_test_values(self):
        self.board = NodeController('localhost:8080')
        self.bogus_nc = NodeController('0.0.0.0:0000')
        bios_path = os.path.join(self.bat_path, 'bios_images')
        self.bios_file_name = os.path.join(bios_path, 'test_bios_image.bin')

    def setup_server_process(self):
        cmd = self.server_command()
        env = self.get_modded_env()
        self.server_process = subprocess.Popen(cmd, env=env,
                                               stderr=subprocess.PIPE)
        time.sleep(2.0)

    def get_modded_env(self):
        """return the modded env used for the server process"""
        env = os.environ.copy()
        if 'PYTHONPATH' not in env:
            env['PYTHONPATH'] = ''
        dev_path = os.path.join(self.bat_path, '../../../hardware')
        dev_abs_path = os.path.abspath(dev_path)
        pypath = env['PYTHONPATH'] + ':' + dev_abs_path
        env['PYTHONPATH'] = pypath
        return env

    def server_command(self):
        app_path = os.path.join(self.bat_path, '../../../server/app/')
        return ['python', os.path.join(app_path, '__main__.py'),
                '--host=127.0.0.1:8080', '--config-file',
                os.path.join(self.bat_path, 'config.json')]

    def tearDown(self):
        for filename in os.listdir(self.bat_path):
            if re.match('mock_state', filename):
                os.remove(filename)
        self.server_process.terminate()

    def test_get_boot_state(self):
        self.board.set_value('1001/node_boot/state', False)
        states = self.board.get_value('1001/node_boot/state')
        self.assertFalse(states['1001/node_boot/state']['samples'][0])

    def test_get_boot_state_group(self):
        """test sampling once from many nodes concurrently"""
        self.board.set_value('1001/node_boot/state', False)
        states = self.board.get_value('100[0-7]/node_boot/state')
        self.assertEqual(len(states), 8)
        for path in states:
            self.assertFalse(states[path]['samples'][0])

    def test_set_boot_state(self):
        """test single-node boot state toggling"""
        states = self.board.set_value('1001/node_boot/state', True)
        self.assertEqual(0, len(states['1001/node_boot/state']['exceptions']))
        states = self.board.get_value('1001/node_boot/state')
        self.assertEqual(0, len(states['1001/node_boot/state']['exceptions']))
        self.assertTrue(states['1001/node_boot/state']['samples'][0])
        states = self.board.set_value('1001/node_boot/state', False)
        self.assertEqual(0, len(states['1001/node_boot/state']['exceptions']))
        self.assertFalse(states['1001/node_boot/state']['samples'][0])

    def test_set_boot_state_group(self):
        """test value toggling on a group of nodes concurrently"""
        for bool_val in [True, False]:
            states = self.board.set_value('100[0-7]/node_boot/state', bool_val)
            print 'set 1-7 to '+str(bool_val)
            for path in [str(i)+'/node_boot/state' for i in range(1000, 1008)]:
                self.assertEqual(0, len(states[path]['exceptions']))
                get = self.board.get_value(path)
                self.assertEqual(0, len(get[path]['exceptions']))
                sample = get[path]['samples'][0]
                print path+':'+str(sample)
                self.assertEqual(sample, bool_val)

    def test_get_boot_state_over_time(self):
        states = self.board.get_value_over_time('1001/node_boot/state', 1, 10)
        response = states['1001/node_boot/state']
        self.assertEqual(10, len(response['samples']))

    def test_get_boot_state_over_time_group(self):
        """test repeated state samples on a concurrent group of nodes"""
        states = self.board.get_value_over_time('*/node_boot/state', 1, 10)
        self.assertEqual(8, len(states))
        for path in states:
            response = states[path]
            self.assertEqual(10, len(response['samples']))
            for sample in response['samples']:
                self.assertFalse(sample)

    def test_api_raises(self):
        """Test that the client api wrapper fails to connect to missing hosts"""
        try:
            self.bogus_nc.get_value('1000/node_boot/state')
            self.fail()
        except ConnectError:
            pass
        try:
            self.bogus_nc.set_value('1000/node_boot/state', True)
            self.fail()
        except ConnectError:
            pass

    @patch.object(requests, "get")
    @patch.object(requests, "post")
    def test_invalid_nc_responses(self, mock_get, mock_post):
        """Test that failed gets and posts propagate to the client correctly"""
        mock_get.return_value = None
        try:
            self.board.get_value('1001/node_boot/state')
            self.fail()
        except ConnectError:
            pass

        mock_post.return_value = None
        try:
            self.board.set_value('1001/node_boot/state', True)
            self.fail()
        except ConnectError:
            pass

    def test_set_bad_value(self):
        """test that nonexistent values don't have URLs at the host"""
        for path in ['1000/bogus', 'bogus/node_vr/temp']:
            try:
                self.board.get_value(path)
                self.fail()
            except ConnectError:
                pass

    def test_set_garbage_values(self):
        states = self.board.set_value('100[0-7]/node_vr/voltage', '@!$bad(bad)')
        for i in range(1000, 1008):
            ex_count = len(states[str(i) + '/node_vr/voltage']['exceptions']),
            self.assertGreater(ex_count, 0)

    def test_set_read_only(self):
        states = self.board.set_value('1001/node_vr/temp', 7)
        print states
        self.assertGreater(len(states['1001/node_vr/temp']['exceptions']), 0)

    def test_flash_bios(self):
        """test single-node bios flash operations"""
        states = self.board.set_value('1000/bios_rom/image',
                                      self.bios_file_name)
        exceptions = states['1000/bios_rom/image']['exceptions']
        self.assertEqual(exceptions, [])
        states = self.board.get_value('1000/bios_rom/image')
        sample = states['1000/bios_rom/image']['samples'][0]
        self.assertEquals(sample['image-file-name'], 'test_bios_image.bin')
        self.assertNotEquals(sample['last-update-time'], None)
        self.assertNotEquals(sample['image-md5'], None)

    def test_flash_bios_group(self):
        """test bios flash operations on multiple nodes concurrently"""
        states = self.board.set_value('100[0-7]/bios_rom/image',
                                      self.bios_file_name)
        for url in states:
            exceptions = states[url]['exceptions']
            self.assertEqual(0, len(exceptions))
        states = self.board.get_value('100[0-7]/bios_rom/image')
        for url in states:
            self.assertEquals(states[url]['samples'][0]['image-file-name'],
                              'test_bios_image.bin')
            self.assertNotEquals(states[url]['samples'][0]['last-update-time'],
                                 None)
            self.assertNotEquals(states[url]['samples'][0]['image-md5'], None)

    def test_flash_missing_bios_file(self):
        states = self.board.set_value('1000/bios_rom/image', 'bogus_garbage')
        self.assertGreater(len(states['1000/bios_rom/image']['exceptions']), 0)

    def test_boot_mechanism(self):
        """Test that a node boot toggles correctly"""
        states = self.board.get_value('1000/node_boot/state')
        self.assertFalse(states['1000/node_boot/state']['samples'][0])
        self.board.set_value('1000/node_boot/state', True)
        states = self.board.get_value('1000/node_boot/state')
        self.assertTrue(states['1000/node_boot/state']['samples'][0])
