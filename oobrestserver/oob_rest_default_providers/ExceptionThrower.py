class ExceptionThrower(object):
    """Device that throws an exception upon calling its #getter method."""

    def __init__(self):
        self.config = {
            "exception": {
                '#getter': ExceptionThrower.fail_read,
                '#units': 'string'
            }
        }

    @staticmethod
    def fail_read():
        raise Exception('Example Exception')
