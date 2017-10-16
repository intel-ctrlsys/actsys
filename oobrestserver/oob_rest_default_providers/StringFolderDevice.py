import threading


class StringFolderDevice(object):
    """Device plugin that allows getting and setting a file-backed string"""

    def __init__(self, default_value=''):
        self.lock = threading.Lock()
        self.value1 = default_value
        self.value2 = default_value
        self.value3 = default_value
        self.set_value1(default_value)
        self.set_value2(default_value)
        self.set_value3(default_value)
        self.config = {
            "strings": {
                "string_one": {
                    '#getter': self.get_value1,
                    '#setter': self.set_value1,
                    '#units': 'string'
                },
                "string_two": {
                    '#getter': self.get_value2,
                    '#setter': self.set_value2,
                    '#units': 'string'
                },
                "string_three": {
                    '#getter': self.get_value3,
                    '#setter': self.set_value3,
                    '#units': 'string'
                },
            }
        }

    def get_value1(self):
        with self.lock:
            return self.value1

    def set_value1(self, value):
        with self.lock:
            self.value1 = value

    def get_value2(self):
        with self.lock:
            return self.value2

    def set_value2(self, value):
        with self.lock:
            self.value2 = value

    def get_value3(self):
        with self.lock:
            return self.value3

    def set_value3(self, value):
        with self.lock:
            self.value3 = value
