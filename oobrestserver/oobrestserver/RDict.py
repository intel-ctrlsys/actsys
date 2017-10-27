# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Intel Corp.
#

"""
Defines the RDict class, which is a tree data structure accessed like a Python dictionary.
Instead of single keys, RDict users provide a list of keys that describe a path through layered dictionaries.
The raw() method returns a traditional, pure-python object, usually a dictionary.
"""


from collections import Hashable
from oobrestserver import GlobTools


class RDict(object):

    """
    Recursively-defined, filesystem-like dictionary data type. Keys are "paths" through a hierarchy of dicts
    containing other dicts, and so on, down to leaf objects.

    Initialize with any python object. Input dictionaries will be traversed and rebuilt as RDicts recursively.
    Item access with [] returns either an RDict or an object, but never a Python dict.
    Setting items with [] creates RDicts recursively.
    Supports move and rename operations.
    Use raw() to recover a primitive Python dictionary. This will traverse and replace RDicts with dicts.
    """

    def __init__(self, obj=None):
        self.data_object = {}
        self[[]] = obj

    def __getitem__(self, keys):
        return self.pop(keys, remove=False)

    def __delitem__(self, keys):
        self.pop(keys)

    def __len__(self):
        return len(self.keys())

    def __setitem__(self, keys, value):
        """Set the value at a key recursively. Will create RDicts recursively to the identified key."""
        RDict.__check_key_type(keys)
        if not keys:
            if value is None:
                self.data_object = {}
            elif isinstance(value, RDict):
                self.data_object = value.data_object
            elif not isinstance(value, dict):
                self.data_object = value
            else:
                self.data_object = {k: RDict(v) if isinstance(v, dict) else v for k, v in value.items()}
            return
        if not isinstance(self.data_object, dict):
            self.data_object = {}
        if len(keys) == 1:
            self.data_object[keys[0]] = RDict(value)
            return
        if keys[0] not in self.data_object or not isinstance(self.data_object[keys[0]], RDict):
            self.data_object[keys[0]] = RDict()
        self.data_object[keys[0]][keys[1:]] = value

    def pop(self, keys, remove=True):
        """Return the value at at the key list. Optionally delete the value from this RDict."""
        RDict.__check_key_type(keys)
        if not keys:
            if not remove:
                return self
            copy = self.data_object
            self.data_object = {}
            return RDict(copy)
        if not isinstance(self.data_object, dict):
            raise KeyError(keys)
        try:
            if len(keys) == 1:
                result = self.data_object[keys[0]]
                if remove:
                    del self.data_object[keys[0]]
                return RDict(result)
            child = self.data_object[keys[0]]
            if not isinstance(child, RDict):
                raise KeyError(keys)
            result = child.pop(keys[1:], remove=remove)
            if remove and not child.data_object:
                del self.data_object[keys[0]]
            return RDict(result)
        except KeyError:
            raise KeyError(keys)

    def move(self, source_path, dest_path):
        RDict.__check_key_type(source_path)
        RDict.__check_key_type(dest_path)
        if source_path:
            self[dest_path + [source_path[-1]]] = self.pop(source_path)
        else:
            self[dest_path] = self.pop(source_path)

    def rename(self, source_path, dest_path):
        RDict.__check_key_type(source_path)
        RDict.__check_key_type(dest_path)
        self[dest_path] = self.pop(source_path)

    def search(self, search_path):
        RDict.__check_key_type(search_path)
        return self.recursive_search(search_path)

    def keys(self):
        return self.recursive_keys()

    def raw(self):
        if not isinstance(self.data_object, dict):
            return self.data_object
        return {k: RDict.raw(v) if isinstance(v, RDict) else v for k, v in self.data_object.items()}

    def recursive_search(self, search_path, path_here=None):
        """Recursively search for all valid (filled) key paths identified by a search path using glob semantics."""
        if path_here is None:
            path_here = []
        if search_path == []:
            if not path_here:
                return []
            return [path_here]
        matches = self.__matching_children(search_path[0])
        child_search = search_path[1:]
        results = [child.recursive_search(child_search, path_here + [key]) for key, child in matches.items()]
        return sum(results, [])

    def recursive_keys(self, path_here=None):
        """recursively list out every valid (filled) key path in this RDict."""
        if path_here is None:
            path_here = []
        if not isinstance(self.data_object, dict):
            return []
        rdict_children = {}
        obj_children = {}
        for key, child in self.data_object.items():
            if isinstance(child, RDict):
                rdict_children[key] = child
            else:
                obj_children[key] = child
        results = sum([child.recursive_keys(path_here + [key]) for key, child in rdict_children.items()], [])
        results += [path_here + [key] for key in obj_children]
        if not results:
            if not path_here:
                return []
            return [path_here]
        return results

    @staticmethod
    def __check_key_type(key):
        if not isinstance(key, list) or any([not isinstance(elt, Hashable) or elt is None for elt in key]):
            raise TypeError('RDict keys must be lists of hashable, non-None objects.')

    def __matching_children(self, glob):
        if not isinstance(self.data_object, dict):
            return {}
        return {k: v for k, v in self.data_object.items() if GlobTools.glob_match(k, glob) and not k.startswith('#')}
