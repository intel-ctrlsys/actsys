

from unittest import TestCase
from unittest import mock

from oob_rest_default_providers.IpmiBMC import IpmiBMC
from oob_rest_default_providers import execute_subprocess
import oob_rest_default_providers.test.sample_output as samples
from oob_rest_default_providers.test.FakeSubProcess import FakeSubProcess

class TestIpmiBMC(TestCase):

    def setUp(self):
        mock.patch(
            "oob_rest_default_providers.IpmiBMC.capture_raw_sensor_table",
            return_value=samples.healthy_sdr_output
        ).start()
        self.bmc = IpmiBMC('bogus_host', None, None, None)
        mock.patch.stopall()

    def tearDown(self):
        mock.patch.stopall()

    def test_get_chassis_state(self):
        mock.patch(
            "oob_rest_default_providers.IpmiBMC.capture_raw_sensor_table",
            return_value=samples.healthy_sdr_output
        ).start()
        self.param_bmc_test_get_chassis_state(self.bmc)

    def test_alternate_bmc_setup(self):
        mock.patch(
            "oob_rest_default_providers.IpmiBMC.capture_raw_sensor_table",
            return_value=samples.healthy_sdr_output
        ).start()
        bmc = IpmiBMC(None, 7807, 'username', 'password')
        self.param_bmc_test_get_chassis_state(bmc)

    def param_bmc_test_get_chassis_state(self, bmc):
        mock.patch(
            "oob_rest_default_providers.execute_subprocess.with_capture",
            return_value=execute_subprocess.Output('command', 0, samples.healthy_chassis_status_output, '')
        ).start()
        result = bmc.get_chassis_state()
        self.assertEqual(result, 'on')

    def test_get_chassis_state_error(self):
        mock.patch(
            "oob_rest_default_providers.execute_subprocess.with_capture",
            return_value=execute_subprocess.Output('command', 1, samples.healthy_chassis_status_output, '')
        ).start()
        try:
            self.bmc.get_chassis_state()
            self.fail()
        except RuntimeError:
            pass

    def test_get_chassis_state_garbled(self):
        mock.patch(
            "oob_rest_default_providers.execute_subprocess.with_capture",
            return_value=execute_subprocess.Output('command', 0, samples.healthy_sdr_output, '')
        ).start()
        try:
            self.bmc.get_chassis_state()
            self.fail()
        except RuntimeError:
            pass

    def test_set_chassis_state(self):

        def fake_without_capture(cmd):
            self.assertEqual(cmd[-2:], ['power', 'on'])
            return True

        mock.patch('oob_rest_default_providers.execute_subprocess.without_capture',
                   return_value=True,
                   side_effect=fake_without_capture).start()
        self.bmc.set_chassis_state('on')

    def test_set_chassis_bad_process(self):
        mock.patch('oob_rest_default_providers.execute_subprocess.without_capture',
                   return_value=None).start()
        try:
            self.bmc.set_chassis_state('on')
            self.fail()
        except RuntimeError:
            pass

    def test_set_chassis_bad_state(self):
        try:
            self.bmc.set_chassis_state('goofball')
            self.fail()
        except RuntimeError:
            pass

    def test_set_led(self):

        interval = 15

        def fake_without_capture(cmd):
            self.assertEqual(cmd[-3:], ['chassis', 'identify', interval])
            return True

        mock.patch('oob_rest_default_providers.execute_subprocess.without_capture',
                   side_effect=fake_without_capture).start()

        self.bmc.set_led_interval(interval)

    def test_capture_raw_table(self):
        mock.patch('oob_rest_default_providers.execute_subprocess.with_capture',
                   return_value=execute_subprocess.Output('test_cmd', 0, 'test_out', 'test_err')).start()
        table = self.bmc.capture_raw_sensor_table()
        self.assertEqual(table, 'test_out')

    def test_led_exception(self):

        mock.patch('oob_rest_default_providers.execute_subprocess.without_capture',
                   side_effect=RuntimeError('test exception')).start()

        try:
            self.bmc.set_led_interval(1)
            self.fail()
        except RuntimeError:
            pass


    def test_get_sensor_by_name(self):
        mock.patch(
            "oob_rest_default_providers.IpmiBMC.capture_raw_sensor_table",
            return_value=samples.healthy_sdr_output
        ).start()
        result = self.bmc.get_sensor_by_name('Processor 1 Fan')
        self.assertEqual(result, '760')
        self.assertEqual(self.bmc.config['sensors']['Processor 1 Fan']['#units'], 'RPM')

    def test_get_unitless_sensor(self):
        mock.patch(
            "oob_rest_default_providers.IpmiBMC.capture_raw_sensor_table",
            return_value=samples.healthy_sdr_output
        ).start()
        result = self.bmc.get_sensor_by_name('IPMI Watchdog')
        self.assertEqual(result, '0x00')
        self.assertEqual(self.bmc.config['sensors']['IPMI Watchdog']['#units'], None)

    def test_capture_to_line(self):

        lines = [x.decode('ascii') for x in samples.theoretical_sol_activate_output.splitlines()]
        expectations = {
            'SIGIL0': lines[:1],
            'SIGIL1': lines[:4],
            'SIGIL2': lines[:5],
            'SIGIL3': lines[:6],
            'SIGIL4': lines[:6],
            'SIGIL5': lines[:7],
            'SIGIL6': lines[:9],
            'SIGIL7': lines
        }

        for sigil in expectations:
            popen_patch = mock.patch(
                "subprocess.Popen",
                return_value=FakeSubProcess(samples.theoretical_sol_activate_output, b'', 0)
            )
            popen_patch.start()
            result = self.bmc.capture_to_line(sigil)
            self.assertEqual(result, expectations[sigil])
            popen_patch.stop()

    def test_exception_capture_to_line(self):
        def thrower():
            raise RuntimeError('Exception for test!')
        mock.patch("subprocess.Popen", side_effect=thrower).start()
        try:
            self.bmc.capture_to_line('anything, really')
            self.fail()
        except RuntimeError as ex:
            pass

    def test_parse_exception(self):
        try:
            IpmiBMC.parse_raw_sensor_table(b"a | b | c\nd | e\nf | g | h\n")
            self.fail()
        except RuntimeError:
            pass

    def test_sels(self):
        mock.patch("subprocess.Popen", return_value=FakeSubProcess(samples.healthy_sel_elist_output, b'', 0)).start()
        self.assertEqual(self.bmc.get_sels(), samples.healthy_sel_elist_output.splitlines())
