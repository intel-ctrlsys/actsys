# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""Holds all the test files"""
import os


class TestJsonFiles(object):
    """Class that create and remove json files for tests"""

    @classmethod
    def write_file(cls, file_name):
        """Create a file if the name is known and an empty file if not"""
        with open(file_name, 'w') as working_file:
            file_content = cls.file_contents.get(file_name, '')
            working_file.write(file_content)
            working_file.close()

    @staticmethod
    def remove_file(file_name):
        """Remove a file"""
        if os.path.exists(file_name):
            os.remove(file_name)

    file_contents = {'version1.json': '''{
  "version": "1",
  "profile": [
    {
      "profile_name": "compute_node",
      "role": [
        "compute"
      ],
      "password": "pass@123",
      "port": 20,
      "image": "/etc/images/UBUNTU",
      "user": "username",
      "service_list": [
        "gmond",
        "orcmd"
      ],
      "os_shutdown_timeout_seconds": 150,
      "os_boot_timeout_seconds": 300,
      "os_network_to_halt_time": 5,
      "bmc_boot_timeout_seconds": 10,
      "bmc_chassis_off_wait": 3
    },
    {
      "user": "username",
      "channel": 11,
      "priv_level": "USER",
      "auth_method": "PASSWORD",
      "password": "pass@123",
      "port": 20,
      "profile_name": "bmc_prof"
    },
    {
      "profile_name": "power_units",
      "outlets_count": 12,
      "port": 20,
      "user": "username",
      "password": "pass@123"
    }
  ],
  "node": [
    {
      "profile": "compute_node",
      "ip_address": "192.168.1.33",
      "hostname": "master5",
      "role": [
        "aggregator"
      ],
      "service_list": [
        "gmond",
        "gmetad",
        "orcmd",
        "orcmsched"
      ],
      "bmc": "bmc2"
    },
    {
      "profile": "compute_node",
      "ip_address": "192.168.1.32",
      "hostname": "master4",
      "bmc": "192.168.2.32"
    }
   ],
  "bmc": [
    {
      "profile": "bmc_prof",
      "ip_address": "192.168.2.33",
      "device_id": "bmc2"
    },
    {
      "profile": "bmc_prof",
      "ip_address": "192.168.2.32"
    }
  ],
  "pdu": [
    {
      "profile": "power_units",
      "ip_address": "192.168.3.32",
      "connected_device": [
        {
          "outlet": "3",
          "device": ["master4"]
        },
        {
          "outlet": "0",
          "device": ["192.168.4.32"]
        }
      ]
    },
    {
      "profile": "power_units",
      "ip_address": "192.168.3.33",
      "hostname": "pdu2",
      "connected_device": [
        {
          "outlet": "3",
          "device": ["master5"]
        },
        {
          "outlet": "0",
          "device": ["bmc2"]
        }
      ]
    }
  ],

  "psu": [
    {
      "profile": "power_units",
      "outlets_count": 2,
      "ip_address": "192.168.4.32",
      "connected_device": [
        {
          "outlet": "1",
          "device": ["master4"]
        },
        {
          "outlet": "0",
          "device": ["master5"]
        }
      ]
    }
  ],

  "configuration_variables": {
    "provisioning_agent_software": "Warewulf",
    "log_file": {
      "path": "/var/log/ctrl.log",
      "max_bytes": 10485760,
      "retention_period": 30,
      "level": "DEBUG"
    },
    "console_output": {
      "file": [
        "/opt/ctrl/console'"
      ],
      "error_level_regex": [
        "regex"
      ],
      "warning_level_regex": [
        "regex"
      ]
    }
  }
}
''',
                     'bad_version.json': '''{
  "version": "2",
  "profile": [
    {
      "profile_name": "compute_node",
      "role": [
        "compute"
      ],
      "password": "pass@123",
      "port": 20,
      "image": "/etc/images/UBUNTU",
      "user": "username",
      "service_list": [
        "gmond",
        "orcmd"
      ]
    }
  ]
}
''',
                     'file.json': '''{
  "profile": [
    {
      "profile_name": "compute_node",
      "role": [
        "compute"
      ],
      "password": "pass@123",
      "port": 20,
      "image": "/etc/images/UBUNTU",
      "user": "username",
      "service_list": [
        "gmond",
        "orcmd"
      ],
      "os_shutdown_timeout_seconds": 150,
      "os_boot_timeout_seconds": 300,
      "os_network_to_halt_time": 5,
      "bmc_boot_timeout_seconds": 10,
      "bmc_chassis_off_wait": 3
    },
    {
      "user": "username",
      "channel": 11,
      "priv_level": "USER",
      "auth_method": "PASSWORD",
      "password": "pass@123",
      "port": 20,
      "profile_name": "bmc_prof"
    },
    {
      "profile_name": "power_units",
      "outlets_count": 12,
      "port": 20,
      "user": "username",
      "password": "pass@123"
    }
  ],
  "node": [
    {
      "profile": "compute_node",
      "ip_address": "192.168.1.33",
      "hostname": "master5",
      "role": [
        "aggregator"
      ],
      "service_list": [
        "gmond",
        "gmetad",
        "orcmd",
        "orcmsched"
      ],
      "bmc": "bmc2"
    },
    {
      "profile": "compute_node",
      "ip_address": "192.168.1.32",
      "hostname": "master4",
      "bmc": "192.168.2.32"
    }
   ],
  "bmc": [
    {
      "profile": "bmc_prof",
      "ip_address": "192.168.2.33",
      "device_id": "bmc2"
    },
    {
      "profile": "bmc_prof",
      "ip_address": "192.168.2.32"
    }
  ],
  "pdu": [
    {
      "profile": "power_units",
      "ip_address": "192.168.3.32",
      "connected_device": [
        {
          "outlet": "3",
          "device": ["master4"]
        },
        {
          "outlet": "0",
          "device": ["192.168.4.32"]
        }
      ]
    },
    {
      "profile": "power_units",
      "ip_address": "192.168.3.33",
      "hostname": "pdu2",
      "connected_device": [
        {
          "outlet": "3",
          "device": ["master5"]
        },
        {
          "outlet": "0",
          "device": ["bmc2"]
        }
      ]
    }
  ],

  "psu": [
    {
      "profile": "power_units",
      "outlets_count": 2,
      "ip_address": "192.168.4.32",
      "connected_device": [
        {
          "outlet": "1",
          "device": ["master4"]
        },
        {
          "outlet": "0",
          "device": ["master5"]
        }
      ]
    }
  ],

  "configuration_variables": {
    "provisioning_agent_software": "Warewulf",
    "log_file": {
      "path": "/var/log/ctrl.log",
      "max_bytes": 10485760,
      "retention_period": 30,
      "level": "DEBUG"
    },
    "console_output": {
      "file": [
        "/opt/ctrl/console'"
      ],
      "error_level_regex": [
        "regex"
      ],
      "warning_level_regex": [
        "regex"
      ]
    }
  }
}

''',
                     'config-example.json': '''{
  "profile": [
    {
      "profile_name": "compute_node",
      "user": "user",
      "password": "password",
      "port": 22,
      "access_type": "ssh",
      "image": "centos7.2",
      "service_list": [
        "orcmd",
        "gmond"
      ],
      "role": [
        "compute"
      ],
      "os_shutdown_timeout_seconds": 150,
      "os_boot_timeout_seconds": 300,
      "os_network_to_halt_time": 5,
      "bmc_boot_timeout_seconds": 10,
      "bmc_chassis_off_wait": 3
    },
    {
      "profile_name": "service_node",
      "user": "user",
      "password": "password",
      "port": 22,
      "access_type": "ssh",
      "image": "centos7.2",
      "service_list": [
        "orcmsched",
        "orcmd",
        "gmond",
        "gmetad"
      ],
      "role": [
        "service"
      ],
      "os_shutdown_timeout_seconds": 150,
      "os_boot_timeout_seconds": 300,
      "os_network_to_halt_time": 5,
      "bmc_boot_timeout_seconds": 10,
      "bmc_chassis_off_wait": 3
    },
    {
      "profile_name": "bmc_default",
      "user": "user",
      "password": "password",
      "channel": 2,
      "priv_level": "ADMINISTRATOR",
      "auth_method": "PASSWORD",
      "port": 22,
      "access_type": "ipmi_util"
    },
    {
      "profile_name": "pdu_default",
      "device_type": "pdu",
      "outlets_count": 8,
      "port": 22,
      "user": "user",
      "password": "password",
      "access_type": "ipmi_util"
    }
  ],
  "node": [
    {
      "profile": "compute_node",
      "hostname": "compute-29",
      "ip_address": "192.168.1.29",
      "mac_address": "00:00:00:00:00:00",
      "bmc": "compute-29-bmc"
    },
    {
      "profile": "compute_node",
      "hostname": "compute-30",
      "ip_address": "192.168.1.30",
      "mac_address": "00:00:00:00:00:00",
      "bmc": "compute-30-bmc"
    },
    {
      "profile": "compute_node",
      "hostname": "compute-31",
      "ip_address": "192.168.1.31",
      "mac_address": "00:00:00:00:00:00",
      "bmc": "compute-31-bmc"
    },
    {
      "profile": "compute_node",
      "hostname": "compute-32",
      "ip_address": "192.168.1.32",
      "mac_address": "00:00:00:00:00:00",
      "bmc": "compute-32-bmc"
    }
  ],
  "bmc": [
    {
      "profile": "bmc_default",
      "hostname": "compute-29-bmc",
      "ip_address": "192.168.2.29",
      "mac_address": "00:00:00:00:00:00"
    },
    {
      "profile": "bmc_default",
      "hostname": "compute-30-bmc",
      "ip_address": "192.168.2.30",
      "mac_address": "00:00:00:00:00:00"
    },
    {
      "profile": "bmc_default",
      "hostname": "compute-31-bmc",
      "ip_address": "192.168.2.31",
      "mac_address": "00:00:00:00:00:00"
    },
    {
      "profile": "bmc_default",
      "hostname": "compute-32-bmc",
      "ip_address": "192.168.2.32",
      "mac_address": "00:00:00:00:00:00"
    }
  ],
  "pdu": [
    {
      "profile": "pdu_default",
      "hostname": "pdu-1",
      "ip_address": "192.168.3.1",
      "mac_address": "00:00:00:00:00:00",
      "connected_device": [
        {
          "outlet": "5",
          "device": [
            "compute-29",
            "compute-30"
          ]
        }
      ]
    },
    {
      "profile": "pdu_default",
      "hostname": "pdu-2",
      "ip_address": "192.168.3.2",
      "mac_address": "00:00:00:00:00:00",
      "connected_device": [
        {
          "outlet": "1",
          "device": [
            "compute-31"
          ]
        },
        {
          "outlet": "2",
          "device": [
            "compute-32"
          ]
        }
      ]
    }
  ],
  "configuration_variables": {
    "provisioning_agent_software": "Warewulf",
    "log_file": {
      "path": "/var/log/ctrl.log",
      "max_bytes": 10485760,
      "retention_period": 30,
      "level": "DEBUG"
    },
    "console_output": {
      "file": [
        "/var/log/ctrl.console.log'"
      ],
      "error_level_regex": [
        "regex"
      ],
      "warning_level_regex": [
        "regex"
      ]
    }
  }
}

''',
                     'non_parsable.json': '''This is not a json file'''}
