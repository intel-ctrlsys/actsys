#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Intel Corp.
#

"""
Application entry point for NC REST API. Parses arguments, creates the
services, and starts the API server.
"""

import argparse
import sys

import cherrypy
import yaml

from oobrestserver.Application import Application


def main():
    """Parse command-line arguments and start the server Application."""

    parser = argparse.ArgumentParser()
    parser.add_argument('--config-file',
                        help='JSON configuration file routing plugin methods to'
                             ' URLs.')
    parser.add_argument('--host',
                        help='Hostname in format ip:port for server.')
    parser.add_argument('--key',
                        help='Private key file for server. Required with --cert'
                             ' to enable SSL.')
    parser.add_argument('--cert',
                        help='OpenSSL cert file for server. Required with --key'
                             ' to enable SSL.')
    parser.add_argument('--auth-file',
                        help='Auth file name. Provide to enable basic auth. '
                             'Requires SSL Enabled.')
    options = parser.parse_args()

    config = {}
    if options.config_file is not None:
        config = yaml.load(open(options.config_file))

    if options.host is not None:
        split_hostname = options.host.split(':')
        if len(split_hostname) == 1:
            cherrypy.config.update({'server.socket_port': 0})
        elif len(split_hostname) == 2:
            cherrypy.config.update({'server.socket_port': int(split_hostname[1])})
        else:
            print('ERROR: host must be in format <ip>[:<port>]')
            return 1
        cherrypy.config.update({'server.socket_host': split_hostname[0]})

    ssl_enabled = False
    if options.cert and options.key:
        cherrypy.server.ssl_certificate = options.cert
        cherrypy.server.ssl_private_key = options.key
        ssl_enabled = True
    elif options.cert or options.key:
        print("ERROR: Both --cert and --key are needed to enable SSL.")
        return 1

    app = Application(config)

    if options.auth_file:
        if not ssl_enabled:
            print("ERROR: Auth without SSL means passwords are sent in "
                  "plaintext! I'm putting a stop to this right now!")
            return 1
        app.enable_auth(options.auth_file)

    app.mount()
    cherrypy.engine.start()
    cherrypy.engine.block()
    app.cleanup()
    return 0

if __name__ == '__main__':  # pragma: no cover
    sys.exit(main())
