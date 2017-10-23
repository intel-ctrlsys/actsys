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
import logging
import logging.handlers
import logging.config
import sys

import cherrypy
import yaml

from oobrestserver.Application import Application


def main():
    """Parse command-line arguments and start the server Application."""

    parser = argparse.ArgumentParser()

    parser_arguments = {
        '--config-file': 'JSON configuration file routing plugin methods to URLs.',
        '--host': 'Hostname in format ip:port for server.',
        '--key': 'Private key file for server. Required with --cert to enable SSL.',
        '--cert': 'OpenSSL cert file for server. Required with --key to enable SSL.',
        '--auth-file': 'Auth file name. Provide to enable basic auth. Requires SSL Enabled.',
        '--log-level': 'Application log level. Choose DEBUG, INFO, WARNING, ERROR, or CRITICAL. Defaults to WARNING.',
        '--log-file-size': 'Max size, in bytes, of rotating log files generated by the server. Defaults to 10 MiB.',
        '--log-file-count': 'Max number of rotating log files generated by the server. Defaults to 3.',
        '--log-file': 'Base name of rotating log files generated by the server. Defaults to server.log.'
    }

    for arg in parser_arguments:
        parser.add_argument(arg, help=parser_arguments[arg])

    options = parser.parse_args()

    try:
        log_level = getattr(logging, options.log_level.upper())
    except AttributeError:
        log_level = logging.WARNING

    try:
        log_file_count = int(options.log_file_count)
    except (ValueError, TypeError):
        log_file_count = 20

    try:
        log_file_size = int(options.log_file_size)
    except (ValueError, TypeError):
        log_file_size = 10485760

    log_file = options.log_file or 'server.log'

    logging.config.dictConfig({
        'version': 1,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': log_level,
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'standard',
                'filename': log_file,
                'maxBytes': log_file_size,
                'backupCount': log_file_count,
                'encoding': 'utf8'
            }
        },
        'loggers': {
            '': {
                'handlers': ['console', 'file'],
                'level': 'INFO'
            },
            'oob': {
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': False
            },
            'cherrypy.access': {
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': False
            },
            'cherrypy.error': {
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': False
            },
        }
    })

    logger = logging.getLogger('oob')

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
            logger.error('Host must be in format <ip>[:<port>]')
            return 1
        cherrypy.config.update({'server.socket_host': split_hostname[0]})

    ssl_enabled = False
    if options.cert and options.key:
        cherrypy.server.ssl_certificate = options.cert
        cherrypy.server.ssl_private_key = options.key
        ssl_enabled = True
    elif options.cert or options.key:
        logger.error("Both --cert and --key are needed to enable SSL.")
        return 1

    app = Application(config, logger)

    if options.auth_file:
        if not ssl_enabled:
            logger.error("Auth without SSL means passwords are sent in plaintext! Stop!")
            return 1
        app.enable_auth(options.auth_file)

    app.mount()
    cherrypy.engine.start()
    cherrypy.engine.block()
    return 0

if __name__ == '__main__':  # pragma: no cover
    sys.exit(main())
