class HelloSensor(object):
    """Device plugin that allows getting the string 'Hello World!'."""

    def __init__(self):
        self.config = {
            "hello": {
                '#getter': lambda: "Hello World!",
                '#units': 'string'
            }
        }

