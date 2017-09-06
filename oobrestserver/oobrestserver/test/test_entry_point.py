
from unittest import TestCase
from unittest import mock

import cherrypy

from oobrestserver.__main__ import main

class TestEntryPoint(TestCase):

    class FakeOptions(object):
        def __init__(self,
                     config_file=None,
                     host=None,
                     key=None,
                     cert=None,
                     auth_file=None):
            self.config_file = config_file
            self.host = host
            self.key = key
            self.cert = cert
            self.auth_file = auth_file


    def setUp(self):
        self.add_argument_patcher = mock.patch(
            'argparse.ArgumentParser.add_argument',
            return_value=None)
        self.json_load_patcher = mock.patch('json.load', return_value={})
        self.app_init_patcher = mock.patch('oobrestserver.Application.__init__', return_value=None)
        self.app_mount_patcher = mock.patch('oobrestserver.Application.mount', return_value=None)
        self.app_enable_auth_patcher = mock.patch('oobrestserver.Application.enable_auth', return_value=None)
        self.app_cleanup_patcher = mock.patch('oobrestserver.Application.cleanup', return_value=None)
        self.chp_start_patcher = mock.patch('cherrypy.engine.start', return_value=None)
        self.chp_block_patcher = mock.patch('cherrypy.engine.block', return_value=None)
        self.chp_conf_update_patcher = mock.patch('cherrypy.config.update', return_value=None)

        self.add_argument_patcher.start()
        self.json_load_patcher.start()
        self.app_init_patcher.start()
        self.app_mount_patcher.start()
        self.app_enable_auth_patcher.start()
        self.app_cleanup_patcher.start()
        self.chp_start_patcher.start()
        self.chp_block_patcher.start()
        self.chp_conf_update_patcher.start()

    def tearDown(self):
        cherrypy.server.ssl_certificate = None
        cherrypy.server.ssl_private_key = None
        self.add_argument_patcher.stop()
        self.json_load_patcher.stop()
        self.app_init_patcher.stop()
        self.app_mount_patcher.stop()
        self.app_enable_auth_patcher.stop()
        self.app_cleanup_patcher.stop()
        self.chp_start_patcher.stop()
        self.chp_block_patcher.stop()
        self.chp_conf_update_patcher.stop()
        mock.patch.stopall()


    def test_main(self):
        options_patcher = mock.patch('argparse.ArgumentParser.parse_args',
                                     return_value=TestEntryPoint.FakeOptions())
        options_patcher.start()
        self.assertEqual(main(), 0)
        options_patcher.stop()

    def test_with_config(self):
        options_patcher = mock.patch('argparse.ArgumentParser.parse_args',
                                     return_value=TestEntryPoint.FakeOptions(
                                         config_file='foobar'
                                     ))
        open_patcher = mock.patch('builtins.open', return_value=None)
        options_patcher.start()
        open_patcher.start()
        self.assertEqual(main(), 0)
        options_patcher.stop()
        open_patcher.stop()

    def test_with_host(self):
        options_patcher = mock.patch('argparse.ArgumentParser.parse_args',
                                     return_value=TestEntryPoint.FakeOptions(
                                         host='foobar'
                                     ))
        options_patcher.start()
        self.assertEqual(main(), 0)
        options_patcher.stop()

    def test_with_host_and_port(self):
        options_patcher = mock.patch('argparse.ArgumentParser.parse_args',
                                     return_value=TestEntryPoint.FakeOptions(
                                         host='foobar:00'
                                     ))
        options_patcher.start()
        self.assertEqual(main(), 0)
        options_patcher.stop()

    def test_with_bad_host(self):
        options_patcher = mock.patch('argparse.ArgumentParser.parse_args',
                                     return_value=TestEntryPoint.FakeOptions(
                                         host='foobar:00:more:bad'
                                     ))
        options_patcher.start()
        self.assertEqual(main(), 1)
        options_patcher.stop()

    def test_cert_no_key(self):
        options_patcher = mock.patch('argparse.ArgumentParser.parse_args',
                                     return_value=TestEntryPoint.FakeOptions(
                                         cert='foobar'
                                     ))
        options_patcher.start()
        self.assertEqual(main(), 1)
        options_patcher.stop()

    def test_key_no_cert(self):
        options_patcher = mock.patch('argparse.ArgumentParser.parse_args',
                                     return_value=TestEntryPoint.FakeOptions(
                                         key='foobar'
                                     ))
        options_patcher.start()
        self.assertEqual(main(), 1)
        options_patcher.stop()

    def test_key_and_cert(self):
        options_patcher = mock.patch('argparse.ArgumentParser.parse_args',
                                     return_value=TestEntryPoint.FakeOptions(
                                         key='foobar',
                                         cert='barfoo'
                                     ))
        options_patcher.start()
        self.assertEqual(main(), 0)
        options_patcher.stop()

    def test_auth_no_ssl(self):
        options_patcher = mock.patch('argparse.ArgumentParser.parse_args',
                                     return_value=TestEntryPoint.FakeOptions(
                                         auth_file='foobar'
                                     ))
        options_patcher.start()
        self.assertEqual(main(), 1)
        options_patcher.stop()

    def test_auth_with_ssl(self):
        options_patcher = mock.patch('argparse.ArgumentParser.parse_args',
                                     return_value=TestEntryPoint.FakeOptions(
                                         auth_file='foobar',
                                         key='foobar',
                                         cert='barfoo'
                                     ))
        options_patcher.start()
        self.assertEqual(main(), 0)
        options_patcher.stop()

