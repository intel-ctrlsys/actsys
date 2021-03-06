import os
import sys
import json

from cherrypy.test import helper

from oobrestserver.Application import Application


class TestServer(helper.CPWebCase):

    app = None

    @staticmethod
    def setup_server():

        app_path = os.path.dirname(os.path.realpath(__file__))
        if app_path not in sys.path:
            sys.path.append(app_path)

        TestServer.app = Application({})
        TestServer.app.mount()

    def teardown_class(cls):
        super(TestServer, cls).teardown_class()

    def setUp(self):
        config = {
            "node1": {
                "FooString": {
                    "_attach_plugins": [
                        {
                            "module":"oob_rest_default_providers.StringDevice",
                            "args": ["Foo"]
                        }
                    ]
                },
                "BarString": {
                    "_attach_plugins": [
                        {
                            "module":"oob_rest_default_providers.StringFolderDevice",
                            "args": ["Bar"],
                            "url_mods": {
                                "strings/*": ""
                            }
                        }
                    ]
                },
                "HelloDevice": {
                    "_attach_plugins": [
                        {
                            "module": "oob_rest_default_providers.HelloSensor"
                        }
                    ]
                },
                "folder": {
                    "InsideString": {
                        "_attach_plugins": [
                            {
                                "module":"oob_rest_default_providers.StringDevice",
                                "args": ["Inside"]
                            }
                        ]
                    }
                },
                "exception_thrower": {
                    "_attach_plugins": [
                        {
                            "module": "oob_rest_default_providers.ExceptionThrower"
                        }
                    ]
                },
                "no_config_exception" : {
                    "_attach_plugins":[
                        {
                          "module": "BadPlugins.NoConfigPlugin"
                        }
                    ]
                }
            },
            "node2": {
                "FooString": {
                    "_attach_plugins": [
                        {
                            "module": "oob_rest_default_providers.StringDevice",
                            "args": ["Foo"]
                        }
                    ]
                },
                "HelloDevice": {
                    "_attach_plugins": [
                        {
                            "module":"oob_rest_default_providers.HelloSensor"
                        }
                    ]
                },
                "folder": {
                    "InsideString": {
                        "_attach_plugins": [
                            {
                                "module": "oob_rest_default_providers.StringDevice",
                                "args": "Inside"
                            }
                        ]
                    }
                },
                "exception_thrower": {
                    "_attach_plugins": [
                        {
                            "module": "oob_rest_default_providers.ExceptionThrower"
                        }
                    ]
                },
                "non_string_obj": {
                    "_attach_plugins": [
                        {
                            "module": None,
                            "args": [17]
                        }
                    ]
                }
            },
            "bad_noclass": {
                '_attach_plugins': [
                    {
                        "module": ''
                    }
                ]
            },
            "good_short": {
                "_attach_plugins": [
                    {
                        "module": 'oob_rest_default_providers.HelloSensor'
                    }
                ]
            },
            "bad_ctor": {
                "_attach_plugins": [
                    {
                        "module": "oob_rest_default_providers.StringDevice",
                        "args": ['too', 'many', 'args']
                    }
                ]
            },
            "uncallable_getter_config_exception": {
                "#getter": "Not a callable, certainly!"
            },
            "uncallable_getter_object_exception": {
                "_attach_plugins": [
                    {
                        "module": "BadPlugins.NotCallableGetter"
                    }
                ]
            },
            "kw": {
                "_attach_plugins": [
                    {
                        "module": "oob_rest_default_providers.EchoKwargs"
                    }
                ]
            },
            "_define_plugins": {
                "my_prefab": {
                    "module": "oob_rest_default_providers.StringDevice",
                    "args": ["Predefined!"]
                },
                "non_buildable": {
                    "module": "BadPlugins.NotCallableGetter"
                },
                "bad_desc_type": None
            },
            "pre": {"de": {"fined": {"_attach_plugins": ["my_prefab"]}}},
            "not_predefined": {"_attach_plugins": ["no_such_plugin"]},
            "unbuildable": {"_attach_plugins": ["non_buildable"]}
        }
        json_config = json.dumps(config)
        headers = [('Content-Type', 'application/json'),
                   ('Content-Length', str(len(json_config)))]
        self.getPage('/api', headers=headers, method='PUT', body=json_config)

    def test_prefabs(self):
        self.check_in_all_samples('/api/pre/de/fined/string', 'Predefined!')
        self.getPage('/api/not_predefined/*')
        self.assertBody('{}')
        self.getPage('/api/unbuildable/*')
        self.assertBody('{}')
        self.getPage('/api/bad_desc_type/*')
        self.assertBody('{}')

    def test_moved_resources(self):
        self.getPage('/api/node1/BarString')
        print (self.body)
        for url in [
            '/api/node1/BarString/string_one',
            '/api/node1/BarString/string_two',
            '/api/node1/BarString/string_three'
        ]:
            self.getPage(url)
            doc = json.loads(self.body.decode('utf-8'))
            res_key = '/'.join(url.split('/')[2:])
            response = doc[res_key]
            samples = response['samples']
            self.assertIn('Bar', samples)
        for url in [
            '/api/node1/BarString/strings/string_one',
            '/api/node1/BarString/strings/string_two',
            '/api/node1/BarString/strings/string_three'
        ]:
            self.getPage(url)
            self.assertStatus('200 OK')
            self.assertBody('{}')

    def check_exception_free_body(self):
        doc = json.loads(self.body.decode('utf-8'))
        for url in [url for url in doc if 'children' not in doc[url]]:
            if "exception" not in url:
                self.assertEqual(0, len(doc[url]['exceptions']))

    def check_in_all_samples(self, url, string):
        self.getPage(url)
        doc = json.loads(self.body.decode('utf-8'))
        for record in doc:
            self.assertIn(string, doc[record]['samples'])

    def test_json_urls(self):
        for url in [
                '/api/',
                '/api/node1/',
                '/api/node1/folder/',
                '/api/node1/folder/InsideString/',
                '/api/node1/folder/InsideString/string/',
                '/gui/']:
            print('getting'+url)
            self.getPage(url)
            self.assertStatus('200 OK')

    def test_delete(self):
        self.getPage('/api/node1/folder/')
        self.assertStatus('200 OK')
        self.assertNotEqual(self.body, '{}')
        self.getPage('/api/node1', method='DELETE')
        self.assertStatus('200 OK')
        self.getPage('/api/node1/folder/')
        self.assertStatus('200 OK')
        self.assertBody('{}')
        self.getPage('/api', method='DELETE')
        self.assertStatus('200 OK')

    def test_leaves_only(self):
        self.getPage('/api/**')
        everything = json.loads(self.body.decode('utf-8'))
        self.getPage('/api/**?leaves_only=1')
        only_leaves = json.loads(self.body.decode('utf-8'))
        self.assertGreater(len(everything), len(only_leaves))

    def test_response_fields(self):
        self.getPage('/api/node1/folder/InsideString/string/')
        full_response = json.loads(self.body.decode('utf-8'))
        response = full_response['node1/folder/InsideString/string']
        self.assertIn('exceptions', response)
        self.assertIn('samples', response)

    def test_simple_post(self):
        json_post = json.dumps('Barbar!')
        json_length = str(len(json_post))
        headers = [('Content-Type', 'application/json'),
                   ('Content-Length', json_length)]
        self.getPage('/api/node1/folder/InsideString/string', headers,
                     'POST', json_post)
        self.assertStatus('200 OK')
        self.check_exception_free_body()
        self.check_in_all_samples('/api/node1/folder/InsideString/string', 'Barbar!')

    def test_set_unsettable(self):
        json_post = json.dumps('Barbar!')
        json_length = str(len(json_post))
        headers = [('Content-Type', 'application/json'),
                   ('Content-Length', json_length)]
        self.getPage('/api/node1/HelloDevice/hello', headers,
                     'POST', json_post)
        self.assertStatus('200 OK')
        doc = json.loads(self.body.decode('utf-8'))
        for key in doc:
            self.assertIn('Method not supported', doc[key]['exceptions'])

    def test_search_globstar(self):
        self.getPage('/api/node1**/string')
        self.assertStatus('200 OK')
        responses = json.loads(self.body.decode('utf-8'))
        self.assertIn('node1/FooString/string', responses)
        self.assertIn('node1/folder/InsideString/string', responses)
        self.assertEqual(len(responses), 2)

    def test_search_star(self):
        self.getPage('/api/node1/*/string')
        self.assertStatus('200 OK')
        responses = json.loads(self.body.decode('utf-8'))
        self.assertIn('node1/FooString/string', responses)
        self.assertNotIn('node1/folder/InsideString/string', responses)
        self.assertEqual(len(responses), 1)

    def test_search_brackets(self):
        self.getPage('/api/node[12]/FooString/string')
        self.assertStatus('200 OK')
        responses = json.loads(self.body.decode('utf-8'))
        self.assertIn('node1/FooString/string', responses)
        self.assertIn('node2/FooString/string', responses)
        self.assertEqual(len(responses), 2)

    def test_search_negate_brackets(self):
        self.getPage('/api/node[!2]/FooString/string')
        self.assertStatus('200 OK')
        responses = json.loads(self.body.decode('utf-8'))
        self.assertIn('node1/FooString/string', responses)
        self.assertNotIn('node2/FooString/string', responses)
        self.assertEqual(len(responses), 1)

    def test_search_qmark(self):
        self.getPage('/api/node%3F/HelloDevice/hello')
        self.assertStatus('200 OK')
        responses = json.loads(self.body.decode('utf-8'))
        self.assertIn('node1/HelloDevice/hello', responses)
        self.assertIn('node2/HelloDevice/hello', responses)
        self.assertEqual(len(responses), 2)

    def test_get_many_samples(self):
        self.getPage('/api/node1/folder/InsideString/string?sample_rate=100&duration=0.25')
        self.assertStatus('200 OK')
        samples = json.loads(self.body.decode('utf-8'))['node1/folder/InsideString/string']['samples']
        self.assertGreater(len(samples), 10)

    def test_get_rapid_samples(self):
        self.getPage('/api/node1/folder/InsideString/string?sample_rate=10000000&duration=0.25')
        self.assertStatus('200 OK')
        samples = json.loads(self.body.decode('utf-8'))['node1/folder/InsideString/string']['samples']
        self.assertLess(len(samples), 2500000)

    def test_glob_only_url(self):
        self.getPage('/api/**')
        self.assertStatus('200 OK')
        self.check_exception_free_body()

    def test_multi_post(self):
        json_post = json.dumps('TEST')
        headers = [('Content-Type', 'application/json'),
                   ('Content-Length', str(len(json_post)))]
        self.getPage('/api/(node1|node2)/FooString/string', headers=headers, method='POST', body=json_post)
        self.assertStatus('200 OK')
        self.check_exception_free_body()
        self.check_in_all_samples('/api/(node1|node2)/FooString/string', 'TEST')

    def test_single_post_list_syntax(self):
        json_post = json.dumps('TEST')
        headers = [('Content-Type', 'application/json'),
                   ('Content-Length', str(len(json_post)))]
        self.getPage('/api/(node1)/FooString/string', headers=headers, method='POST', body=json_post)
        self.assertStatus('200 OK')
        self.check_exception_free_body()
        self.check_in_all_samples('/api/(node1)/FooString/string', 'TEST')

    def test_get_many_values_many_samples(self):
        self.getPage('/api/node1/**/string?sample_rate=100&duration=0.25')
        self.assertStatus('200 OK')
        responses = json.loads(self.body.decode('utf-8'))
        self.assertEqual(len(responses), 2)
        for path in responses:
            self.assertGreater(len(responses[path]['samples']), 10)

    def test_exception_in_result(self):
        self.getPage('/api/node2/exception_thrower/exception')
        self.assertStatus('200 OK')
        exceptions = json.loads(self.body.decode('utf-8'))['node2/exception_thrower/exception']['exceptions']
        self.assertIn('Example Exception', exceptions)
        self.getPage('/api/node2/exception_thrower/exception?sample_rate=10&duration=0.25')
        self.assertStatus('200 OK')
        exceptions = json.loads(self.body.decode('utf-8'))['node2/exception_thrower/exception']['exceptions']
        self.assertIn('Example Exception', exceptions)

    def test_good_config(self):
        self.getPage('/api/good_short/hello')
        self.assertStatus('200 OK')
        self.assertIn('Hello World!', self.body.decode('utf-8'))

    def test_echo_kwargs(self):
        self.getPage('/api/kw/kwargs?foo=bar')
        self.assertEqual("{'foo': 'bar'}", json.loads(self.body.decode('utf-8'))['kw/kwargs']['samples'][0])

    def test_bad_ctor(self):
        self.getPage('/api/bad_ctor/*')
        self.assertStatus("200 OK")
        self.assertBody('{}')

    def test_no_class_plugin(self):
        self.getPage('/api/bad_noclass')
        self.assertStatus("200 OK")
        self.check_exception_free_body()
        self.getPage('/api/bad_noclass/*')
        self.assertStatus("200 OK")
        self.assertBody('{}')

    def test_non_string_plugin(self):
        self.getPage('/api/node2/17')
        self.assertStatus("200 OK")
        self.assertBody('{}')

    def test_no_config_plugin(self):
        self.getPage('/api/node1/no_config_exception')
        self.assertStatus("200 OK")

    def test_no_resource(self):
        self.getPage('/api/foobar')
        self.assertStatus("200 OK")
        self.assertBody('{}')

    def test_uncallable_getter(self):
        self.getPage('/api/uncallable_getter_config_exception')
        self.assertStatus('200 OK')
        exceptions = json.loads(self.body.decode('utf-8'))['uncallable_getter_config_exception']['exceptions']
        self.assertIn('not callable', exceptions[0])

    def test_bad_glob(self):
        self.getPage('/api/100[1-4')
        self.assertStatus("200 OK")
        self.assertBody('{}')
