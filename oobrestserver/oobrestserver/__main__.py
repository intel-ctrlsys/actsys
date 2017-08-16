#!/usr/bin/env python
"""
Application entry point for NC REST API. Parses arguments, creates the
services, and starts the API server.
"""

import sys
import json
import argparse

import cherrypy

from Application import Application


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
        config = json.load(open(options.config_file))

    if options.host is not None:
        split_hostname = options.host.split(':')
        cherrypy.config.update({'server.socket_port': int(split_hostname[1])})
        cherrypy.config.update({'server.socket_host': split_hostname[0]})

    ssl_enabled = False
    if options.cert and options.key:
        cherrypy.server.ssl_certificate = options.cert
        cherrypy.server.ssl_private_key = options.key
        ssl_enabled = True
    elif options.cert or options.key:
        print("ERROR: Both --cert and --key are needed to enable SSL.")
        sys.exit(0)

    app = Application(config)

    if options.auth_file:
        if not ssl_enabled:
            print("ERROR: Auth without SSL means passwords are sent in "
                  "plaintext! I'm putting a stop to this right now!")
            sys.exit(0)
        app.enable_auth(options.hashes_file)

    app.mount()
    cherrypy.engine.start()
    cherrypy.engine.block()
    app.cleanup()

if __name__ == '__main__':
    sys.exit(main() or 0)
