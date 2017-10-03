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

    def __init__(self, hostname, port, username, password, interface='lanplus'):
        self.sol_lock = threading.Lock()
        self.power_state_lock = threading.Lock()
        self.sdr_lock = threading.Lock()

        self.config = {
            'chassis_state': {
                '#getter': self.get_chassis_state,
                '#setter': self.set_chassis_state,
                '#units': 'ChassisState'
            },
            'console': {
                '#setter': self.capture_to_line
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
        self.last_sdr_update_time = 0
        self.sdr_cache = {}

        hostname = hostname or '127.0.0.1'
        port = port or '623'
        self.ipmitool_opts = ['ipmitool', '-I', interface, '-H', hostname, '-p', port]
        if username:
            self.ipmitool_opts += ['-U', username]
        if password:
            self.ipmitool_opts += ['-P', password]

        self.populate_sensors()

    def get_chassis_state(self):
        command = self.ipmitool_opts+ ['chassis', 'status']
        with self.power_state_lock:
            subprocess_result = execute_subprocess.with_capture(command)
        if subprocess_result.return_code != 0 or subprocess_result.stdout is None:
            raise RuntimeError('Failed to execute ipmitool! Command: {} stdout: {} stderr: {}'
                               .format(command, subprocess_result.stdout, subprocess_result.stderr))
        for line in subprocess_result.stdout.splitlines():
            if line.strip().startswith('System Power'):
                return line.split(':')[1].strip()
        raise RuntimeError('Failed to retrieve chassis power state!')

    def set_chassis_state(self, new_state):
        with self.power_state_lock:
            valid_states = ["on", "off", "soft", "cycle"]
            if not new_state in valid_states:
                raise RuntimeError("Invalid power state: {}. Choose from {}".format(new_state, valid_states))
            cmd = self.ipmitool_opts + ['power', new_state]
            if not execute_subprocess.without_capture(cmd):
                raise RuntimeError('Failed to execute ipmitool!')

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
            sensor_name, value, units = IpmiBMC.parse_sensor_table_line(str(line))
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
        return execute_subprocess.with_capture(cmd).stdout.splitlines()

    def capture_to_line(self, stop_line):
        """Start capturing console"""
        with self.sol_lock:
            console_lines = []
            try:
                command = self.ipmitool_opts + ['sol', 'activate']
                consolelog = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
            except Exception as ex:  # Catching all Exceptions as Popen or IPMI could fail with some unknow exceptions
                raise RuntimeError("Could not activate IPMI sol on BMC. Console logs will not be collected\n Received Error:"
                                  + str(ex))
            while not consolelog.poll():
                buffer_v = consolelog.stdout.readline()
                length_buff = len(buffer_v)
                if length_buff > 0:
                    line = buffer_v.strip('\n')
                    console_lines.append(line)
                    if stop_line in line:
                        consolelog.terminate()
                # consoleLog.wait()
            consolelog.terminate()
            return console_lines
