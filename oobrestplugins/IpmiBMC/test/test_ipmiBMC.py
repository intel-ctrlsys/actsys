from unittest import TestCase

from oobrestserver.oobrestplugins.IpmiBMC.IpmiBMC import IpmiBMC

class TestIpmiBMC(TestCase):

    def setUp(self):
        self.bmc = IpmiBMC('127.0.0.1', '9001', 'test', 'password')

    def test_get_chassis_state(self):
        result = self.bmc.get_chassis_state()
        self.fail()

    def test_set_chassis_state(self):
        self.bmc.set_chassis_state('off')
        self.fail()

    def test_capture_to_line(self):
        self.fail()

    def test_get_sensor_by_name(self):
        self.fail()

    def test_get_sels(self):
        self.fail()
