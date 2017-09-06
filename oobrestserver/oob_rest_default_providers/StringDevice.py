import os
import uuid
import threading


class StringDevice(object):
    """Device plugin that allows getting and setting a file-backed string"""

    def __init__(self, default_string=''):

        self.filename = 'test_file_' + str(uuid.uuid4())
        self.lock = threading.Lock()

        self.config = {
            "string": {
                '#getter': self.get_string,
                '#setter': self.set_string,
                '#units': 'string',
                '#cleanup': self.rm_file
            }
        }

        self.set_string(default_string)

    def get_string(self):
        with self.lock:
            with open(self.filename, 'r') as state_file:
                state = state_file.read()
            return state

    def set_string(self, value):
        self.atomic_write_file(value)

    def rm_file(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def atomic_write_file(self, value):
        with self.lock:
            tmp_name = 'tmp_'+str(uuid.uuid4())
            with open(tmp_name, 'w') as tmp_file:
                tmp_file.write(value)
                tmp_file.flush()
                os.fsync(tmp_file.fileno())
            os.rename(tmp_name, self.filename)
