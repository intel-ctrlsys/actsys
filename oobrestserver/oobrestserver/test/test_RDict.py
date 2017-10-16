
from oobrestserver.RDict import RDict

from unittest import TestCase


class TestRDict(TestCase):

    def test_get_set_shallow(self):
        rd = RDict()
        rd[['a']] = 'hello world'
        self.assertEqual('hello world', rd[['a']])

    def test_get_set_two_step(self):
        rd = RDict()
        rd[['a', 'b']] = 'hello world'
        self.assertEqual('hello world', rd[['a', 'b']])

    def test_get_set(self):
        rd = RDict()
        rd[['a', 'b', 'c']] = 'hello world'
        self.assertEqual('hello world', rd[['a', 'b', 'c']])

    def test_get_set_dict(self):
        rd = RDict({'a': {'b': 'ab'}})
        self.assertEqual(rd[['a', 'b']], 'ab')

    def test_set_dict(self):
        rd = RDict()
        rd[[]] = {'a': {'b': 'ab'}}
        self.assertEqual(rd[['a', 'b']], 'ab')
        rd.move(['a', 'b'], ['b', 'a'])
        self.assertEqual(rd[['b', 'a']], 'ab')
        self.assertEqual(rd.raw(), {'b': {'a': 'ab'}})
        rd[['b', 'b', 'c', 'f']] = 'foobar'
        self.assertEqual(rd.raw(), {'b': {'a': 'ab', 'b': {'c': {'f': 'foobar'}}}})

    def test_raw(self):
        example = {'a': {'a': 'aa', 'b': 'ab', 'c': 'ac'}}
        rd = RDict(example)
        self.assertEqual(rd.raw(), example)

    def check_key_raises_ex(self, rd, key, extype):
        try:
            print(rd[key])
            self.fail()
        except extype:
            return
        except Exception:
            self.fail()

    def test_bad_key_types(self):
        example = {'a': {'a': 'aa', 'b': 'ab', 'c': 'ac'}}
        rd = RDict(example)
        self.check_key_raises_ex(rd, None, TypeError)
        self.check_key_raises_ex(rd, 'a', TypeError)
        self.check_key_raises_ex(rd, [[]], TypeError)
        self.check_key_raises_ex(rd, {}, TypeError)
        self.check_key_raises_ex(rd, RDict(), TypeError)

    def test_missing_keys(self):
        example = {'a': {'a': 'aa', 'b': 'ab', 'c': 'ac'}}
        rd = RDict(example)
        self.check_key_raises_ex(rd, ['b'], KeyError)
        self.check_key_raises_ex(rd, [0], KeyError)
        self.check_key_raises_ex(rd, ['a', 'a', 'b'], KeyError)

    def test_strange_good_keys(self):
        example = {'a': {'a': 'aa', 'b': 'ab', 'c': 'ac'}}
        rd = RDict(example)
        try:
            self.assertEqual(rd[[]].raw(), example)
            self.assertEqual(len(rd), len(rd[[]].raw()))
            self.assertEqual(rd[['a']].raw(), example['a'])
            self.assertEqual(rd[['a', 'a']], example['a']['a'])
            self.assertEqual(rd[['a', 'a']], 'aa')
        except Exception:
            self.fail()


    def test_simple_pop(self):
        example = {'a': {'a': 'aa', 'b': 'ab', 'c': 'ac'}}
        rd = RDict(example)
        popval = rd.pop(['a', 'a'])
        self.assertEqual(popval, 'aa')
        try:
            rd.pop(['a', 'a'])
            self.fail()
        except KeyError:
            pass
        self.assertEqual(rd.raw(), {'a': {'b': 'ab', 'c': 'ac'}})
        popval = rd.pop([])
        self.assertEqual(popval.raw(), {'a': {'b': 'ab', 'c': 'ac'}})
        self.assertEqual(rd.raw(), {})
        rd = RDict('abc')
        popval = rd.pop([])
        self.assertEqual(popval, 'abc')
        self.assertEqual(rd.raw(), {})

    def test_root_data_obj(self):
        rd = RDict()
        rd[[]] = 'hello world'
        self.assertEqual(rd[[]], 'hello world')
        self.assertEqual(rd[[]], 'hello world')
        rd[['a']] = ['a']
        self.assertNotEqual(rd[[]], 'hello world')
        self.assertEqual(rd[[]].raw(), {'a': ['a']})
        rd[[]] = 'hello world'
        self.assertEqual(rd[[]], 'hello world')
        self.assertEqual(rd.raw(), 'hello world')
        try:
            print(rd[['a']])
            self.fail()
        except KeyError:
            pass
