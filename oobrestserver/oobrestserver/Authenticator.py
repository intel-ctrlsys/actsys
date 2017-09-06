# -*- coding: utf-8 -*-
"""
Provides the Authenticator class, supporting all authentication services used
by the server.
"""
import hashlib
import hmac
import os
import pickle
import re


class Authenticator(object):
    """
    Provides basic authentication services with respect to the usernames and
    salted, hashed passwords stored in a given file.
    """

    def __init__(self):
        self.users = {}

    def save(self, auth_file_name):
        with open(auth_file_name, 'wb') as auth_file:
            pickle.dump(self.users, auth_file)

    def load(self, auth_file_name):
        with open(auth_file_name, 'rb') as auth_file:
            self.users = pickle.load(auth_file)

    @staticmethod
    def create_empty_auth_file(auth_file_name):
        with open(auth_file_name, 'wb') as auth_file:
            pickle.dump({}, auth_file)
        os.chmod(os.path.abspath(auth_file_name), 0o600)

    @staticmethod
    def compute_hash(password, salt):
        return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 5000)

    def add_user(self, user_name, password):
        """Add a new username:password to the authenticator"""
        if user_name in self.users:
            return False
        if not Authenticator.check_password_complexity(password):
            return False
        new_salt = os.urandom(32)
        new_hash = self.compute_hash(password, new_salt)
        self.users[user_name] = (new_hash, new_salt)
        return True

    def del_user(self, user_name, password):
        if not self.authenticate(user_name, password):
            return False
        del self.users[user_name]
        return True

    def reset_password(self, user_name, old_password, new_password):
        """Reset the password for a user."""
        if not self.authenticate(user_name, old_password):
            return False
        if not Authenticator.check_password_complexity(new_password):
            return False
        self.del_user(user_name, old_password)
        self.add_user(user_name, new_password)
        return True

    def authenticate(self, user_name, password):
        correct_hash, salt = self.users.get(user_name, (None, None))
        if correct_hash is None or salt is None:
            return False
        computed_hash = self.compute_hash(password, salt)
        return hmac.compare_digest(computed_hash, correct_hash)

    @staticmethod
    def check_password_complexity(password):
        try:
            password.encode('utf-8')
        except (AttributeError, UnicodeEncodeError):
            return False
        return re.search('[A-Z]', password) and \
               re.search('[a-z]', password) and \
               re.search('[0-9]', password) and \
               re.search('[^0-9A-Za-z]', password) and \
               len(password) >= 8
