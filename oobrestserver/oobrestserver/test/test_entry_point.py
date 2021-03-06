# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Intel Corp.
#

from unittest import TestCase
from unittest import mock

import cherrypy

from oobrestserver.__main__ import main


class FakeOptions(object):

    def __init__(self, config_file=None, host=None, key=None, cert=None, auth_file=None,
                 log_level=None, log_file=None, log_file_size=None, log_file_count=None):
        self.config_file = config_file
        self.host = host
        self.key, self.cert = key, cert
        self.auth_file = auth_file
        self.log_level = log_level
        self.log_file = log_file
        self.log_file_size = log_file_size
        self.log_file_count = log_file_count


class FakeRotatingFileHandler(object):

    def __init__(self, file=None, count=None, size=None):
        self.formatter = None
        pass

    def setLevel(self, level):
        pass


class TestEntryPoint(TestCase):

    def setUp(self):
        mock.patch('argparse.ArgumentParser.add_argument', return_value=None).start()
        mock.patch('yaml.load', return_value={}).start()
        mock.patch('oobrestserver.Application.Application.enable_auth', return_value=None).start()
        mock.patch('oobrestserver.Application.Application.mount', return_value=None).start()
        mock.patch('oobrestserver.Application.Application.__init__', return_value=None).start()
        mock.patch('cherrypy.engine.start', return_value=None).start()
        mock.patch('cherrypy.engine.block', return_value=None).start()
        mock.patch('cherrypy.config.update', return_value=None).start()
        mock.patch('logging.config.dictConfig', return_value=None).start()

    def tearDown(self):
        cherrypy.server.ssl_certificate = None
        cherrypy.server.ssl_private_key = None
        mock.patch.stopall()

    def test_main(self):
        mock.patch('argparse.ArgumentParser.parse_args', return_value=FakeOptions()).start()
        self.assertEqual(main(), 0)

    def test_with_config(self):
        mock.patch('argparse.ArgumentParser.parse_args', return_value=FakeOptions(config_file='foobar')).start()
        mock.patch('builtins.open', return_value=None).start()
        self.assertEqual(main(), 0)

    def test_with_host(self):
        mock.patch('argparse.ArgumentParser.parse_args', return_value=FakeOptions(host='foobar')).start()
        self.assertEqual(main(), 0)

    def test_with_host_and_port(self):
        mock.patch('argparse.ArgumentParser.parse_args', return_value=FakeOptions(host='foobar:00')).start()
        self.assertEqual(main(), 0)

    def test_with_bad_host(self):
        mock.patch('argparse.ArgumentParser.parse_args', return_value=FakeOptions(host='foobar:00:more:bad')).start()
        self.assertEqual(main(), 1)

    def test_cert_no_key(self):
        mock.patch('argparse.ArgumentParser.parse_args', return_value=FakeOptions(cert='foobar')).start()
        self.assertEqual(main(), 1)

    def test_key_no_cert(self):
        mock.patch('argparse.ArgumentParser.parse_args', return_value=FakeOptions(key='foobar')).start()
        self.assertEqual(main(), 1)

    def test_key_and_cert(self):
        mock.patch('argparse.ArgumentParser.parse_args', return_value=FakeOptions(key='foobar', cert='barfoo')).start()
        self.assertEqual(main(), 0)

    def test_auth_no_ssl(self):
        mock.patch('argparse.ArgumentParser.parse_args', return_value=FakeOptions(auth_file='foobar')).start()
        self.assertEqual(main(), 1)

    def test_auth_with_ssl(self):
        mock.patch('argparse.ArgumentParser.parse_args', return_value=FakeOptions(auth_file='foobar', key='foobar', cert='barfoo')).start()
        self.assertEqual(main(), 0)

    def test_log_file(self):
        mock.patch('argparse.ArgumentParser.parse_args', return_value=FakeOptions(log_file='foobar')).start()
        self.assertEqual(main(), 0)
