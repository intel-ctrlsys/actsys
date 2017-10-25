from oobrestserver import GlobTools
from collections import Hashable


class RDict(object):

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
            if remove and len(self.data_object[keys[0]]) == 0:
                del self.data_object[keys[0]]
            return RDict(result)
        except KeyError:
            raise KeyError(keys)

    def move(self, source_path, dest_path):
        RDict.__check_key_type(source_path)
        RDict.__check_key_type(dest_path)
        if len(source_path) > 0:
            self[dest_path + [source_path[-1]]] = self.pop(source_path)
        else:
            self[dest_path] = self.pop(source_path)

    def rename(self, source_path, dest_path):
        RDict.__check_key_type(source_path)
        RDict.__check_key_type(dest_path)
        self[dest_path] = self.pop(source_path)

    def search(self, search_path):
        RDict.__check_key_type(search_path)
        return self.__search(search_path)

    def keys(self):
        return self.__keys()

    def raw(self):
        if not isinstance(self.data_object, dict):
            return self.data_object
        return {k: RDict.raw(v) if isinstance(v, RDict) else v for k, v in self.data_object.items()}

    def __search(self, search_path, path_here=None):
        if path_here is None:
            path_here = []
        if search_path == []:
            if not path_here:
                return []
            return [path_here]
        matches = self.__matching_children(search_path[0])
        child_search = search_path[1:]
        results = [child.__search(child_search, path_here + [key]) for key, child in matches.items()]
        return sum(results, [])

    def __keys(self, path_here=None):
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
        results = sum([child.__keys(path_here + [key]) for key, child in rdict_children.items()], [])
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
