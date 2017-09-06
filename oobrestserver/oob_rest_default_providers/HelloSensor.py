class HelloSensor(object):
    """Device plugin that allows getting the string 'Hello World!'."""

    def __init__(self):
        self.greeting = "Hello World!"
        self.config = {
            "hello": {
                '#getter': self.hello,
                '#units': 'string'
            }
        }

    def hello(self):
        return self.greeting

