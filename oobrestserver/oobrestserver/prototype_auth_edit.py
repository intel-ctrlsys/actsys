# -*- coding: utf-8 -*-
"""Prototype command-line tool for server credential management"""

import argparse
import getpass
import sys

from Authenticator import Authenticator

PARSER = argparse.ArgumentParser()
PARSER.add_argument('--auth-file', help='user:password:salt to edit')
PARSER.add_argument('--add-user', help='User name to add')
PARSER.add_argument('--change-pass', help='User name whose password to change')
PARSER.add_argument('--remove-user', help='User name to remove')
OPTIONS = PARSER.parse_args()

if not OPTIONS.auth_file:
    print("Specify an auth file to edit!")
    sys.exit(0)

AUTH = Authenticator()
AUTH.load(OPTIONS.auth_file)

if OPTIONS.add_user and OPTIONS.remove_user:
    print("Only add or remove a user - don't do both. I'm a prototype tool.")

if OPTIONS.add_user:
    PASSWORD = getpass.getpass(prompt='password: ')
    if AUTH.add_user(OPTIONS.add_user, PASSWORD):
        print('User ' + OPTIONS.add_user + ' added successfully')
    else:
        print('ERROR: User ' + OPTIONS.add_user + ' already exists')

if OPTIONS.change_pass:
    OLD_PASSWORD = getpass.getpass(prompt='old password: ')
    NEW_PASSWORD = getpass.getpass(prompt='new password: ')
    if AUTH.reset_password(OPTIONS.change_pass, OLD_PASSWORD, NEW_PASSWORD):
        print('Password updated successfully')
    else:
        print('ERROR: Password update failed')

if OPTIONS.remove_user:
    PASSWORD = getpass.getpass(prompt='password: ')
    if AUTH.del_user(OPTIONS.remove_user, PASSWORD):
        print('User ' + OPTIONS.remove_user + ' removed successfully')
    else:
        print('ERROR: User removal failed')

AUTH.save(OPTIONS.auth_file)
