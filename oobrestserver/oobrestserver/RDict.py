class RDict(object):

    def __init__(self, obj=None):
        self.__set_data_object(obj)

    def __getitem__(self, keys):

        if not isinstance(keys, list):
            raise TypeError('RDict keys must be lists of hashable types.')

        if not keys:
            if isinstance(self.data_object, dict):
                return RDict(self.data_object)
            return self.data_object

        if not isinstance(self.data_object, dict):
            raise KeyError(keys)

        if len(keys) == 1:
            try:
                return self.data_object[keys[0]]
            except TypeError:
                raise TypeError('RDict keys must be lists of hashable types.')

        try:
            child = self.data_object[keys[0]]
            if isinstance(child, RDict):
                return child[keys[1:]]
            else:
                raise KeyError(keys)
        except KeyError:
            raise KeyError(keys)

    def __setitem__(self, keys, value):

        if not keys:
            self.__set_data_object(value)
            return

        if not isinstance(self.data_object, dict):
            self.__set_data_object({})

        if len(keys) == 1:
            self.__set_data_object({keys[0]: value})
            return

        if keys[0] not in self.data_object or not isinstance(self.data_object[keys[0]], RDict):
            self.data_object[keys[0]] = RDict()
        self.data_object[keys[0]][keys[1:]] = value

    def __len__(self):
        return len(self.data_object)

    def __set_data_object(self, obj):
        if obj is None:
            obj = {}
        if isinstance(obj, dict):
            self.data_object = {k: RDict(v) if isinstance(v, dict) else v for k, v in obj.items()}
        else:
            self.data_object = obj

    def move(self, source_path, dest_path):
        value = self.pop(source_path)
        self[dest_path] = value

    def pop(self, keys):

        if not keys:
            if isinstance(self.data_object, dict):
                copy = RDict(self.data_object)
            else:
                copy = self.data_object
            self.__set_data_object({})
            return copy

        key_piece = keys[0]
        if not isinstance(self.data_object, dict) or key_piece not in self.data_object:
            raise KeyError(key_piece)

        if len(keys) == 1:
            result = self.data_object[key_piece]
            del self.data_object[key_piece]
            return result

        try:
            result = self.data_object[key_piece].pop(keys[1:])
            if len(self.data_object[key_piece]) == 0:
                del self.data_object[key_piece]
            return result
        except KeyError:
            raise KeyError(keys)
    #
    # def get(self, key, default=None):
    #     try:
    #         return self[key]
    #     except KeyError:
    #         return default

    def raw(self):
        if isinstance(self.data_object, dict):
            return {k: v.raw() if isinstance(v, RDict) else v for k, v in self.data_object.items()}
        return self.data_object

    #
    # def __delitem__(self, keys):
    #
    #     if not isinstance(keys, list):
    #         raise TypeError('RDict keys must be lists of hashable types.')
    #
    #     if not keys:
    #         self.__set_data_object({})
    #
    #     if not isinstance(self.data_object, dict):
    #         raise KeyError(keys)
    #
    #     if len(keys) == 1:
    #         try:
    #             del self.data_object[keys[0]]
    #         except TypeError:
    #             raise TypeError('RDict keys must be lists of hashable types.')
    #
    #     try:
    #         child = self.data_object[keys[0]]
    #         if isinstance(child, RDict):
    #             del child[keys[1:]]
    #         else:
    #             raise KeyError(keys)
    #     except KeyError:
    #         raise KeyError(keys)
