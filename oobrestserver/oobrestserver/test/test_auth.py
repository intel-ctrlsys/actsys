
import os
import uuid
from oobrestserver.Authenticator import Authenticator
from unittest import TestCase


class TestAuthenticator(TestCase):

    def setUp(self):
        self.auth = Authenticator()

    def test_no_user(self):
        self.assertFalse(self.auth.authenticate('username','password_1A'))

    def test_add_user(self):
        self.assertTrue(self.auth.add_user('username','password_1A'))
        self.assertFalse(self.auth.add_user('username', 'password_1A'))
        self.assertTrue(self.auth.authenticate('username','password_1A'))
        self.assertFalse(self.auth.authenticate('username','wrong_password_1A'))

    def test_change_pass(self):
        self.auth.add_user('username','password_1A')
        self.assertTrue(self.auth.authenticate('username','password_1A'))
        self.assertFalse(self.auth.reset_password('username', 'wrongword_1A', 'diff_password_1A'))
        self.assertTrue(self.auth.authenticate('username','password_1A'))
        self.assertFalse(self.auth.authenticate('username','diff_password_1A'))
        self.assertTrue(self.auth.reset_password('username', 'password_1A', 'diff_password_1A'))
        self.assertFalse(self.auth.authenticate('username','password_1A'))
        self.assertTrue(self.auth.authenticate('username','diff_password_1A'))

    def test_file_persist(self):

        passwords = {
            'user1': 'Pass_1fjsdkl',
            'fjdask': 'fh1!dvdjDDew',
            'qwerty': 'uIop12!fsdj',
            'hello': 'W0r1d!dd'
        }

        for user in passwords:
            self.auth.add_user(user, passwords[user])

        filename = 'temp_auth_file_'+str(uuid.uuid4())
        self.auth.save(filename)
        other_auth = Authenticator()
        other_auth.load(filename)
        os.remove(os.path.abspath(filename))

        for auth in [self.auth, other_auth]:
            for user in passwords:
                auth.add_user(user, passwords[user])

            for user in passwords:
                for other in passwords:
                    if other != user:
                        result = auth.authenticate(user, passwords[other])
                        self.assertFalse(result)
                        result = auth.authenticate(user, passwords[user])
                        self.assertTrue(result)

    def test_del_user(self):
        self.assertTrue(self.auth.add_user('username', 'password_1A'))
        self.assertTrue(self.auth.authenticate('username', 'password_1A'))
        self.assertFalse(self.auth.del_user('username', 'wrongword_1A'))
        self.assertTrue(self.auth.authenticate('username', 'password_1A'))
        self.assertTrue(self.auth.del_user('username', 'password_1A'))
        self.assertFalse(self.auth.authenticate('username','password_1A'))

    def test_complexity_checker(self):
        self.assertFalse(self.auth.add_user('username', 'password'))
        self.assertFalse(self.auth.add_user('username', 'password1'))
        self.assertFalse(self.auth.add_user('username', 'password1!'))
        self.assertFalse(self.auth.add_user('username', 'password!'))
        self.assertFalse(self.auth.add_user('username', 'Password1'))
        self.assertFalse(self.auth.add_user('username', 'Password!'))

        self.assertTrue(self.auth.add_user('username', 'PassW0rd!'))

        self.assertFalse(self.auth.reset_password('username', 'PassW0rd!', 'password'))
        self.assertFalse(self.auth.reset_password('username', 'PassW0rd!', 'password1'))
        self.assertFalse(self.auth.reset_password('username', 'PassW0rd!', 'password1!'))
        self.assertFalse(self.auth.reset_password('username', 'PassW0rd!', 'password!'))
        self.assertFalse(self.auth.reset_password('username', 'PassW0rd!', 'Password1'))
        self.assertFalse(self.auth.reset_password('username', 'PassW0rd!', 'Password!'))

        self.assertTrue(self.auth.reset_password('username', 'PassW0rd!', 'n3w_p455w0Rd'))

        self.assertFalse(self.auth.check_password_complexity(TestAuthenticator))
