# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Intel Corp.
#

"""
OOBREST Plugin for atomic OOB Management through IPMI.
"""

import functools
import threading
import time
import subprocess

from oob_rest_default_providers import execute_subprocess


class IpmiBMC(object):

    def __init__(self, hostname=None, port=None, username=None, password=None, interface='lanplus',
                 ssh_timeout=10, ssh_retries=10, ssh_address=None, ssh_port=22, ssh_username=None, ssh_password=None, ssh_id=None, ssh_interval=10,
                 ping_address=None, ping_retries=10, ping_interval=10):

        self.sol_lock = threading.Lock()
        self.sol_process = None
        self.power_state_lock = threading.Lock()
        self.sdr_lock = threading.Lock()
        self.last_sdr_update_time = 0
        self.sdr_cache = {}

        self.ssh_timeout = ssh_timeout
        self.ssh_interval = ssh_interval
        self.ssh_retries = ssh_retries
        self.ssh_check_cmd = sum([
            ['ssh', '-q'],
            [] if ssh_id is None else ['-i', ssh_id],
            ['-p', "%d" % ssh_port],
            ['%s@%s' % (ssh_username, ssh_address)],
            ['-o', 'ConnectTimeout={}'.format(ssh_timeout)],
            ['echo', '-n', '""']],
        [])

        self.ping_interval = ping_interval
        self.ping_retries = ping_retries
        self.ping_check_cmd = ['ping', '-c', '1', '-W', '1', '-q', ping_address]

        self.ipmitool_opts = ['ipmitool', '-I', interface, '-H', hostname or '127.0.0.1', '-p', port or '623']
        if username:
            self.ipmitool_opts += ['-U', username]
        if password:
            self.ipmitool_opts += ['-P', password]

        self.config = {
            'chassis_state': {
                '#getter': self.get_chassis_state,
                '#setter': self.set_chassis_state,
                '#units': 'ChassisState'
            },
            'sol_stream': {
                '#setter': self.set_sol_stream,
                '#cleanup': self.end_sol
            },
            'sel': {
                '#getter': self.get_sels
            },
            'sensors': {
            },
            'refresh_sensors': {
                '#getter': self.populate_sensors
            },
            'chassis_led_interval': {
                '#setter': self.set_led_interval
            }
        }
        self.populate_sensors()

    def get_chassis_state(self):
        command = self.ipmitool_opts+ ['chassis', 'status']
        with self.power_state_lock:
            subprocess_result = execute_subprocess.with_capture(command)
        if subprocess_result.return_code != 0 or subprocess_result.stdout is None:
            raise RuntimeError('Failed to execute ipmitool! Command: {} stdout: {} stderr: {}'
                               .format(command, subprocess_result.stdout, subprocess_result.stderr))
        for line in subprocess_result.stdout.splitlines():
            if line.decode().strip().startswith('System Power'):
                return line.decode().split(':')[1].strip()
        raise RuntimeError('Failed to retrieve chassis power state!')

    def set_chassis_state(self, new_state):
        with self.power_state_lock:
            states = ["on", "off", "soft", "cycle"]
            if new_state in states:
                self.__blind_ipmitool_invoke(['power', new_state])
            elif new_state == "block_on":
                self.__blind_ipmitool_invoke(['power', 'on'])
                self.block_to_ssh()
            elif new_state == "block_cycle":
                self.__blind_ipmitool_invoke(['power', 'cycle'])
                self.block_to_ssh()
            elif new_state == "block_soft_reboot":
                self.__blind_ipmitool_invoke(['power', 'soft'])
                self.block_to_off()
                self.__blind_ipmitool_invoke(['power', 'on'])
                self.block_to_ssh()
            else:
                valid_states = states + ["block_on", "block_cycle", "block_soft_reboot"]
                raise RuntimeError("Invalid power state: {}. Choose from {}".format(new_state, valid_states))

    def __blind_ipmitool_invoke(self, cmd):
        if not execute_subprocess.without_capture(self.ipmitool_opts+cmd):
            raise RuntimeError('Failed to execute ipmitool!')

    def block_to_ssh(self):
        retry_counter = 0
        while execute_subprocess.without_capture(self.ssh_check_cmd).return_code and retry_counter < self.ssh_retries:
            retry_counter += 1
            time.sleep(self.ssh_retries)
        if retry_counter == self.ssh_retries:
            raise RuntimeError('Timeout waiting for node to come up for SSH!')

    def block_to_off(self):
        retry_counter = 0
        while not execute_subprocess.without_capture(self.ping_check_cmd).return_code and retry_counter < self.ping_retries:
            retry_counter += 1
            time.sleep(self.ping_interval)
        if retry_counter == self.ssh_retries:
            raise RuntimeError('Timeout waiting for node to shut down (stop pinging)!')

    def set_led_interval(self, interval):
        try:
            command = self.ipmitool_opts + ['chassis', 'identify', interval]
            execute_subprocess.without_capture(command)
        except Exception as ex:
            raise RuntimeError("Error using ipmitool: " + str(ex))

    def populate_sensors(self):
        with self.sdr_lock:
            self.__update_sdr_cache()
            for sensor_name in self.sdr_cache:
                self.config['sensors'][sensor_name] = {
                    '#getter': functools.partial(self.get_sensor_by_name, sensor_name),
                    '#units': self.sdr_cache[sensor_name][1]
                }

    def get_sensor_by_name(self, sensor_name):
        with self.sdr_lock:
            self.__update_sdr_cache()
            value, units = self.sdr_cache.get(sensor_name, (None, None))
            return value

    def __update_sdr_cache(self):
        if self.last_sdr_update_time <= time.time() - 1.0:
            raw_table = self.capture_raw_sensor_table()
            self.sdr_cache = IpmiBMC.parse_raw_sensor_table(raw_table)
            self.last_sdr_update_time = time.time()

    def capture_raw_sensor_table(self):
        command = self.ipmitool_opts + ['sdr']
        return execute_subprocess.with_capture(command).stdout

    @staticmethod
    def parse_raw_sensor_table(raw_table):
        sensor_table = {}
        for line in raw_table.splitlines():
            sensor_name, value, units = IpmiBMC.parse_sensor_table_line(line.decode('ascii'))
            sensor_table[sensor_name] = (value, units)
        return sensor_table

    @staticmethod
    def parse_sensor_table_line(line):
        words = [word.strip() for word in line.split('|')]
        if len(words) < 3:
            raise RuntimeError("Unexpected stdout from ipmitool: " + line)
        measure_words = words[1].split(' ')
        name = words[0]
        sample = measure_words[0]
        units = None
        if len(measure_words) > 1:
            units = ' '.join(measure_words[1:])
        return (name, sample, units)

    def get_sels(self):
        cmd = self.ipmitool_opts + ['sel', 'list']
        proc = execute_subprocess.with_capture(cmd)
        output_bytes = proc.stdout
        output_string = output_bytes.decode('ascii')
        output_lines = output_string.splitlines()
        return output_lines

    def set_sol_stream(self, file_name):
        if file_name is None:
            self.end_sol()
        else:
            self.start_sol(file_name)

    def start_sol(self, cap_file_name):
        with self.sol_lock, open(cap_file_name) as cap_file:
            try:
                cmd = self.ipmitool_opts + ['sol', 'activate']
                self.sol_process = subprocess.Popen(cmd, stdout=cap_file, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
            except Exception as ex:
                raise RuntimeError("Could not activate  IPMI SOL capture: {}".format(str(ex)))

    def end_sol(self):
        with self.sol_lock:
            if self.sol_process is not None:
                self.sol_process.terminate()
                try:
                    self.sol_process.wait(1.0)
                except subprocess.TimeoutExpired:
                    if not self.sol_process.poll():
                        self.sol_process.kill()
                self.sol_process = None
            try:
                cmd = self.ipmitool_opts + ['sol', 'deactivate']
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL)
                return proc.communicate(timeout=1.0)[0]
            except Exception as ex:
                raise RuntimeError("Could not deactivate IPMI SOL capture: {}".format(str(ex)))


