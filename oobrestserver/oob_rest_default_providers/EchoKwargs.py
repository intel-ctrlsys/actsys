class EchoKwargs(object):
    """Device plugin that prints kwargs from its GET method."""

    def __init__(self):
        self.config = {
            "kwargs": {
                '#getter': self.echo_kwargs,
                '#units': 'string'
            }
        }

    def echo_kwargs(self, **kwargs):
        return str(kwargs)

