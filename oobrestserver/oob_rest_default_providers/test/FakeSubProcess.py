from io import BytesIO

class FakeSubProcess(object):
    def __init__(self, stdout, stderr, ret_code):
        self.stdout = BytesIO(stdout)
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

    def wait(self):
        self.term = True
