from io import StringIO

class FakeSubProcess(object):
    def __init__(self, stdout, stderr, ret_code):
        self.stdout_lines = stdout.splitlines()
        self.stderr_lines = stderr.splitlines()
        self.stdout = StringIO(stdout)
        self.stderr = StringIO(stderr)
        self.ret_code = ret_code
        self.term = False

    def poll(self):
        return self.term

    def terminate(self):
        self.term = True

    def communicate(self, input=None, timeout=None):
        return self.stdout.read().encode('utf-8'), self.stderr.read().encode('utf-8')

    def returncode(self):
        return self.ret_code

    def kill(self):
        self.term = True

    def wait(self):
        self.term = True
