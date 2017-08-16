import os
import uuid


class StringDevice(object):
    """Device plugin that allows getting and setting a file-backed string"""

    def __init__(self, default_string=''):

        self.filename = 'test_file_' + str(uuid.uuid4())

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
        with open(self.filename, 'r') as state_file:
            state = state_file.read()
        return state

    def set_string(self, value):
        with open(self.filename, 'w+') as state_file:
            state_file.write(value)

    def rm_file(self):
        print ('deleting ' + self.filename)
        if os.path.exists(self.filename):
            os.remove(self.filename)
