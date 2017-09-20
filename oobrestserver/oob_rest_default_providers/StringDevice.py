import threading


class StringDevice(object):
    """Device plugin that allows getting and setting a file-backed string"""

    def __init__(self, default_value=''):
        self.lock = threading.Lock()
        self.set_value(default_value)
        self.config = {
            "string": {
                '#getter': self.get_value,
                '#setter': self.set_value,
                '#units': 'string'
            }
        }

    def get_value(self):
        with self.lock:
            return self.value

    def set_value(self, value):
        with self.lock:
            self.value = value
