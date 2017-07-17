import unittest
from control.diagnostics.mock_diagnostics.mock_diagnostics import MockDiagnostics


class TestsMockDiagnostics(unittest.TestCase):
    """Unit tests for Mock Diagnostics"""

    def setUp(self):
        self.device = {
            "hostname": "test1"
        }
        self.bmc = {
            "ip_address": "localhost",
            }

    def test_launch_diags_positive(self):
        d1 = MockDiagnostics()
        result = d1.launch_diags(self.device, self.bmc)
        self.assertEqual('Diagnostics completed on node test1', result)
