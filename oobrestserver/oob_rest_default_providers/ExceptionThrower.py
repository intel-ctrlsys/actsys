class ExceptionThrower(object):
    """Device that throws an exception upon calling its #getter method."""

    def __init__(self):
        self.config = {
            "exception": {
                '#getter': self.fail_read,
                '#units': 'string'
            }
        }

    def fail_read(self):
        raise Exception('Example Exception')
