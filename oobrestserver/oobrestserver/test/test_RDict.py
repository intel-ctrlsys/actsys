
from oobrestserver.RDict import RDict

from unittest import TestCase


class TestRDict(TestCase):

    def test_get_set_shallow(self):
        rd = RDict()
        rd[['a']] = 'hello world'
        self.assertEqual('hello world', rd[['a']].raw())

    def test_get_set_two_step(self):
        rd = RDict()
        rd[['a', 'b']] = 'hello world'
        self.assertEqual('hello world', rd[['a', 'b']].raw())

    def test_get_set(self):
        rd = RDict()
        rd[['a', 'b', 'c']] = 'hello world'
        self.assertEqual('hello world', rd[['a', 'b', 'c']].raw())

    def test_get_set_dict(self):
        rd = RDict({'a': {'b': 'ab'}})
        self.assertEqual(rd[['a', 'b']].raw(), 'ab')

    def test_set_dict(self):
        rd = RDict()
        rd[[]] = {'a': {'b': 'ab'}}
        self.assertEqual(rd[['a', 'b']].raw(), 'ab')
        rd.rename(['a', 'b'], ['b', 'a'])
        self.assertEqual(rd[['b', 'a']].raw(), 'ab')
        self.assertEqual(rd.raw(), {'b': {'a': 'ab'}})
        rd[['b', 'b', 'c', 'f']] = 'foobar'
        self.assertEqual(rd.raw(), {'b': {'a': 'ab', 'b': {'c': {'f': 'foobar'}}}})
        try:
            rd['b'] = 'hello'
            self.fail()
        except TypeError:
            pass

    def test_move(self):
        rd = RDict()
        rd[[]] = {'a': {'b': 'ab'}}
        self.assertEqual(rd[['a', 'b']].raw(), 'ab')
        rd.move(['a', 'b'], ['b', 'a'])
        self.assertEqual(rd[['b', 'a', 'b']].raw(), 'ab')
        self.assertEqual(rd.raw(), {'b': {'a': {'b': 'ab'}}})
        rd.move([], [])
        self.assertEqual(rd.raw(), {'b': {'a': {'b': 'ab'}}})
        rd.move([], ['test'])
        self.assertEqual(rd.raw(), {'test': {'b': {'a': {'b': 'ab'}}}})

    def test_raw(self):
        example = {'a': {'a': 'aa', 'b': 'ab', 'c': 'ac'}}
        rd = RDict(example)
        self.assertEqual(rd.raw(), example)

    def check_key_raises_ex(self, rd, key, extype):
        try:
            print(rd[key].raw())
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
            self.assertEqual(len(rd), len(rd[[]]))
            self.assertEqual(rd[['a']].raw(), example['a'])
            self.assertEqual(rd[['a', 'a']].raw(), example['a']['a'])
            self.assertEqual(rd[['a', 'a']].raw(), 'aa')
        except Exception:
            self.fail()

    def test_simple_pop(self):
        example = {'a': {'a': 'aa', 'b': 'ab', 'c': 'ac'}}
        rd = RDict(example)
        popval = rd.pop(['a', 'a']).raw()
        self.assertEqual(popval, 'aa')
        try:
            rd.pop(['a', 'a'])
            self.fail()
        except KeyError:
            pass
        self.assertEqual(rd.raw(), {'a': {'b': 'ab', 'c': 'ac'}})
        popval = rd.pop([]).raw()
        self.assertEqual(popval, {'a': {'b': 'ab', 'c': 'ac'}})
        self.assertEqual(rd.raw(), {})
        rd = RDict('abc')
        popval = rd.pop([]).raw()
        self.assertEqual(popval, 'abc')
        self.assertEqual(rd.raw(), {})

    def test_root_data_obj(self):
        rd = RDict()
        rd[[]] = 'hello world'
        self.assertEqual(rd[[]].raw(), 'hello world')
        self.assertEqual(rd[[]].raw(), 'hello world')
        rd[['a']] = ['a']
        self.assertNotEqual(rd[[]].raw(), 'hello world')
        self.assertEqual(rd[[]].raw(), {'a': ['a']})
        rd[[]] = 'hello world'
        self.assertEqual(rd[[]].raw(), 'hello world')
        self.assertEqual(rd.raw(), 'hello world')
        try:
            print(rd[['a']].raw())
            self.fail()
        except KeyError:
            pass

    def test_keys(self):
        example = {'a': {'a': 'aa', 'b': 'ab', 'c': 'ac'}}
        rd = RDict(example)
        keys = rd.keys()
        self.assertIn(['a', 'a'], keys)
        self.assertIn(['a', 'b'], keys)
        self.assertIn(['a', 'c'], keys)
        self.assertEqual(len(keys), 3)
        self.assertEqual(len(rd), 3)

    def test_edge_keys(self):
        example = {'a': {}}
        rd = RDict(example)
        self.assertIn(['a'], rd.keys())
        self.assertEqual(len(rd), 1)
        self.assertEqual(len(rd.keys()), 1)
        rd = RDict()
        self.assertEqual(rd.keys(), [])
        self.assertEqual(len(rd), 0)
        self.assertEqual(len(rd.keys()), 0)
        rd = RDict('hello')
        self.assertEqual(rd.keys(), [])
        self.assertEqual(len(rd), 0)
        self.assertEqual(len(rd.keys()), 0)

    def test_edge_search(self):
        rd = RDict('hello')
        self.assertEqual(rd.search([]), [])
        self.assertEqual(rd.search(['hello']), [])
        self.assertEqual(rd.search(['']), [])
        try:
            print(rd.search([None]))
            self.fail()
        except TypeError:
            pass

    def test_del(self):
        example = {'a': {'a': 'aa', 'b': 'ab', 'c': 'ac'}}
        rd = RDict(example)
        del rd[['a', 'a']]
        self.assertEqual(rd.raw(), {'a': {'b': 'ab', 'c': 'ac'}})
        try:
            del rd[['a', 'a']]
            self.fail()
        except KeyError:
            pass
        del rd[[]]
        self.assertEqual(rd.raw(), {})
        rd = RDict('abc')
        self.assertEqual(rd.raw(), 'abc')
        del rd[[]]
        self.assertEqual(rd.raw(), {})
