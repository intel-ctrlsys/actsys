from io import BytesIO
from subprocess import TimeoutExpired

class FakeSubProcess(object):
    def __init__(self, stdout, stderr, ret_code):
        if isinstance(stdout, bytes):
            self.stdout = BytesIO(stdout)
        else:
            self.stdout = stdout
        self.stderr = BytesIO(stderr)
        self.ret_code = ret_code
        self.term = False

    def poll(self):
        return self.term

    def terminate(self):
        self.term = True

    def communicate(self, input=None, timeout=None):
        return self.stdout.read(), self.stderr.read()

    def returncode(self):
        return self.ret_code

    def kill(self):
        self.term = True

    def wait(self, timeout=None):
        if timeout == 0:
            raise TimeoutExpired()
        self.term = True
