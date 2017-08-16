import os
import sys
import base64
import uuid

from cherrypy.test import helper

from  ..Application import Application
from ..Authenticator import Authenticator


class TestServer(helper.CPWebCase):

    app = None

    @staticmethod
    def setup_server():

        test_path = os.path.dirname(os.path.realpath(__file__))
        app_path = os.path.join(test_path, '..')
        if app_path not in sys.path:
            sys.path.append(app_path)

        config = {
            "node1": {
                "FooString": {
                    "#obj": ["DefaultProviders.StringDevice", "Foo"]
                },
                "HelloDevice": {
                    "#obj": ["DefaultProviders.HelloSensor"]
                },
                "folder": {
                    "InsideString": {
                        "#obj": ["DefaultProviders.StringDevice", "Inside"]
                    }
                }
            }
        }

        TestServer.app = Application(config)
        auth = Authenticator()
        filename = 'temp_auth_file_'+str(uuid.uuid4())
        auth.add_user('test_user', 'Test_Pass_01')
        auth.save(filename)
        TestServer.app.enable_auth(filename)
        os.remove(os.path.abspath(filename))
        TestServer.app.mount()

    def test_auth_file_created(self):
        my_app = Application({})
        filename = 'temp_auth_file_'+str(uuid.uuid4())
        self.assertFalse(os.path.exists(os.path.abspath(filename)))
        my_app.enable_auth(filename)
        self.assertTrue(os.path.exists(os.path.abspath(filename)))
        os.remove(os.path.abspath(filename))

    def teardown_class(cls):
        TestServer.app.cleanup()
        super(TestServer, cls).teardown_class()

    def test_no_auth(self):
        self.getPage('/api/node1/FooString/string/')
        self.assertStatus('401 Unauthorized')
    
    def test_auth(self):
        b64_value = base64.b64encode('test_user:Test_Pass_01')
        self.getPage('/api/node1/FooString/string/',
                     headers=[('Authorization', 'Basic %s' % b64_value)])
        self.assertStatus('200 OK')
