theoretical_sol_activate_output = \
b"""SIGIL0
>>> line one
>>> line two
SIGIL1_then_words
SIGIL2 then words
SIGIL3SIGIL4
SIGIL5

SIGIL6
SIGIL7"""

healthy_chassis_status_output = \
b"""System Power         : on
Power Overload       : false
Power Interlock      : inactive
Main Power Fault     : false
Power Control Fault  : false
Power Restore Policy : always-on
Last Power Event     :
Chassis Intrusion    : inactive
Front-Panel Lockout  : inactive
Drive Fault          : false
Cooling/Fan Fault    : false
Sleep Button Disable : not allowed
Diag Button Disable  : allowed
Reset Button Disable : allowed
Power Button Disable : allowed
Sleep Button Disabled: false
Diag Button Disabled : false
Reset Button Disabled: false
Power Button Disabled: false
"""

healthy_sdr_output = \
b"""Pwr Unit Status  | 0x00              | ok
IPMI Watchdog    | 0x00              | ok
Physical Scrty   | 0x00              | ok
FP NMI Diag Int  | 0x00              | ok
SMI Timeout      | 0x00              | ok
System Event Log | 0x00              | ok
System Event     | 0x00              | ok
Button           | 0x00              | ok
VR Watchdog      | 0x00              | ok
SSB Therm Trip   | 0x00              | ok
IO Mod Presence  | 0x00              | ok
SAS Mod Presence | 0x00              | ok
BMC FW Health    | 0x00              | ok
System Airflow   | 62 CFM            | ok
BB EDGE Temp     | 25 degrees C      | ok
Front Panel Temp | 26 degrees C      | ok
SSB Temp         | 43 degrees C      | ok
BB BMC Temp      | 35 degrees C      | ok
BB P2 VR Temp    | 30 degrees C      | ok
BB MEM VR Temp   | 31 degrees C      | ok
Exit Air Temp    | 28 degrees C      | ok
LAN NIC Temp     | 46 degrees C      | ok
System Fan 1     | 1330 RPM          | ok
System Fan 2     | 760 RPM           | ok
Processor 1 Fan  | 760 RPM           | ok
Processor 2 Fan  | 760 RPM           | ok
PS1 Status       | 0x00              | ok
PS1 Power In     | 120 Watts         | ok
PS1 Curr Out %   | 6 percent         | ok
PS1 Temperature  | 35 degrees C      | ok
P1 Status        | 0x00              | ok
P2 Status        | 0x00              | ok
P1 Therm Margin  | -65 degrees C     | ok
P2 Therm Margin  | -67 degrees C     | ok
P1 Therm Ctrl %  | 0 percent         | ok
P2 Therm Ctrl %  | 0 percent         | ok
P1 ERR2          | 0x00              | ok
P2 ERR2          | 0x00              | ok
CATERR           | 0x00              | ok
P1 MSID Mismatch | 0x00              | ok
CPU Missing      | 0x00              | ok
P1 DTS Therm Mgn | -65 degrees C     | ok
P2 DTS Therm Mgn | -67 degrees C     | ok
P2 MSID Mismatch | 0x00              | ok
P1 VRD Hot       | 0x00              | ok
P2 VRD Hot       | 0x00              | ok
P1 MEM01 VRD Hot | 0x00              | ok
P1 MEM23 VRD Hot | 0x00              | ok
P2 MEM01 VRD Hot | 0x00              | ok
P2 MEM23 VRD Hot | 0x00              | ok
PS1 1a Fan Fail  | 0x00              | ok
PS1 1b Fan Fail  | 0x00              | ok
MIC Status 1     | Not Readable      | ns
MIC Status 3     | Not Readable      | ns
MIC Status 5     | Not Readable      | ns
MIC Status 7     | Not Readable      | ns
DIMM Thrm Mrgn 1 | -65 degrees C     | ok
DIMM Thrm Mrgn 2 | -63 degrees C     | ok
DIMM Thrm Mrgn 3 | -64 degrees C     | ok
DIMM Thrm Mrgn 4 | -63 degrees C     | ok
Mem P1 Thrm Trip | 0x00              | ok
Mem P2 Thrm Trip | 0x00              | ok
MIC Margin 1     | disabled          | ns
MIC Margin 3     | disabled          | ns
MIC Margin 5     | disabled          | ns
MIC Margin 7     | disabled          | ns
Agg Thrm Mgn 1   | -24 degrees C     | ok
Agg Thrm Mgn 2   | -24 degrees C     | ok
BB +12.0V        | 11.88 Volts       | ok
BB +5.0V         | 5.00 Volts        | ok
BB +3.3V         | 3.32 Volts        | ok
BB +5.0V STBY    | 4.94 Volts        | ok
BB +3.3V AUX     | 3.24 Volts        | ok
BB +1.05V P1Vccp | 0.83 Volts        | ok
BB +1.05V P2Vccp | 0.82 Volts        | ok
BB +1.5 P1DDR AB | 1.50 Volts        | ok
BB +1.5 P1DDR CD | 1.50 Volts        | ok
BB +1.5 P2DDR AB | 1.50 Volts        | ok
BB +1.5 P2DDR CD | 1.51 Volts        | ok
BB +1.8V AUX     | 1.76 Volts        | ok
BB +1.1V STBY    | 1.08 Volts        | ok
BB VBAT          | 3.08 Volts        | ok
BB +1.35 P1LV AB | disabled          | ns
BB +1.35 P1LV CD | disabled          | ns
BB +1.35 P2LV AB | disabled          | ns
BB +1.35 P2LV CD | disabled          | ns
NM Capabilities  | Not Readable      | ns
P1 MTT           | no reading        | ns
P2 MTT           | no reading        | ns
"""

healthy_sel_elist_output = \
b"""   1 | 06/03/2014 | 17:38:05 | Event Logging Disabled System Event Log | Log area reset/cleared | Asserted
   2 | 06/03/2014 | 17:38:05 | Power Supply #0x51 | Presence detected | Deasserted
   3 | 06/03/2014 | 17:38:06 | Fan #0x0c | Fully Redundant | Deasserted
   4 | 06/03/2014 | 17:38:06 | Fan #0x0c | Redundancy Lost | Asserted
   5 | 06/03/2014 | 17:38:06 | Fan #0x0c | Non-Redundant: Insufficient Resources | Asserted
   6 | 06/03/2014 | 17:38:08 | Fan #0x0c | Redundancy Lost | Deasserted
   7 | 06/03/2014 | 17:38:08 | Fan #0x0c | Non-Redundant: Insufficient Resources | Deasserted
   8 | 06/03/2014 | 17:38:10 | Fan #0x0c | Fully Redundant | Deasserted
   9 | 06/03/2014 | 17:38:10 | Fan #0x0c | Redundancy Lost | Asserted
   a | 06/03/2014 | 17:38:10 | Fan #0x0c | Non-Redundant: Insufficient Resources | Asserted
   b | 06/03/2014 | 17:38:26 | Fan #0x38 | Lower Non-critical going low  | Asserted
   c | 06/03/2014 | 17:38:26 | Fan #0x38 | Lower Critical going low  | Asserted
   d | 06/03/2014 | 17:38:30 | Management Subsystem Health BMC FW Health | Sensor failure | Asserted
   e | 06/03/2014 | 17:38:30 | Management Subsystem Health BMC FW Health | Sensor failure | Asserted
   f | 06/03/2014 | 17:38:31 | Management Subsystem Health BMC FW Health | Sensor failure | Asserted
  10 | 06/03/2014 | 17:39:15 | Power Unit #0x02 | Redundancy Lost | Asserted
  11 | 06/03/2014 | 17:39:15 | Power Unit #0x02 | Non-Redundant: Sufficient from Redundant | Asserted
  12 | 06/03/2014 | 17:39:24 | Version Change FW Update Status |  | Asserted
  13 | 06/03/2014 | 17:39:32 | Unknown SPS FW Health |  | Asserted
  14 | 06/03/2014 | 17:39:32 | Unknown SPS FW Health |  | Asserted
  15 | 06/03/2014 | 17:39:33 | Unknown SPS FW Health |  | Asserted
  16 | 06/03/2014 | 17:39:53 | Version Change FW Update Status |  | Asserted
  17 | 06/03/2014 | 17:44:29 | Fan #0x0c | Redundancy Lost | Deasserted
  18 | 06/03/2014 | 17:44:29 | Fan #0x0c | Non-Redundant: Insufficient Resources | Deasserted
  19 | 06/03/2014 | 17:44:29 | Fan #0x38 | Lower Non-critical going low  | Deasserted
  1a | 06/03/2014 | 17:44:29 | Fan #0x38 | Lower Critical going low  | Deasserted
  1b | 06/03/2014 | 17:46:18 | Power Unit Pwr Unit Status | Power off/down | Asserted
  1c | 06/03/2014 | 17:46:23 | Power Unit Pwr Unit Status | Power off/down | Deasserted
  1d | 06/03/2014 | 17:46:34 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  1e | 06/03/2014 | 17:46:34 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  1f | 06/03/2014 | 17:47:03 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
  20 | 06/04/2014 | 10:13:00 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  21 | 06/04/2014 | 10:13:00 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  22 | 06/04/2014 | 10:13:23 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
  23 | 06/04/2014 | 11:26:46 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  24 | 06/04/2014 | 11:26:46 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  25 | 06/04/2014 | 09:41:52 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
  26 | 06/04/2014 | 09:47:45 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  27 | 06/04/2014 | 09:47:45 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  28 | 06/04/2014 | 09:47:45 | Power Unit Pwr Unit Status | Power off/down | Asserted
  29 | 06/04/2014 | 09:49:51 | Power Supply PS1 Status | Power Supply AC lost | Asserted
  2a | 06/10/2014 | 16:13:06 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  2b | 06/10/2014 | 16:13:06 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  2c | 06/10/2014 | 16:13:24 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
  2d | 06/10/2014 | 16:13:57 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  2e | 06/10/2014 | 16:13:57 | Button Button | Power Button pressed | Asserted
  2f | 06/10/2014 | 16:13:57 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  30 | 06/10/2014 | 16:13:57 | Power Unit Pwr Unit Status | Power off/down | Asserted
  31 | 06/10/2014 | 16:14:04 | Power Supply PS1 Status | Power Supply AC lost | Asserted
  32 | 06/10/2014 | 16:19:17 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  33 | 06/10/2014 | 16:19:17 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  34 | 06/10/2014 | 16:19:34 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
  35 | 06/10/2014 | 16:20:04 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  36 | 06/10/2014 | 16:20:04 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  37 | 06/10/2014 | 16:20:05 | Power Unit Pwr Unit Status | Power off/down | Asserted
  38 | 06/10/2014 | 16:20:05 | Button Button | Power Button pressed | Asserted
  39 | 06/10/2014 | 16:20:11 | Power Supply PS1 Status | Power Supply AC lost | Asserted
  3a | 06/11/2014 | 09:34:19 | Power Unit Pwr Unit Status | Power off/down | Asserted
  3b | 06/11/2014 | 09:36:20 | Power Unit Pwr Unit Status | Power off/down | Deasserted
  3c | 06/11/2014 | 09:36:20 | Button Button | Power Button pressed | Asserted
  3d | 06/11/2014 | 09:36:29 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  3e | 06/11/2014 | 09:36:29 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  3f | 06/11/2014 | 09:36:47 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
  40 | 06/11/2014 | 09:37:43 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  41 | 06/11/2014 | 09:37:43 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  42 | 06/11/2014 | 09:39:13 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
  43 | 06/11/2014 | 09:40:09 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  44 | 06/11/2014 | 09:40:09 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  45 | 06/11/2014 | 09:40:27 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
  46 | 06/11/2014 | 09:50:33 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  47 | 06/11/2014 | 09:50:33 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  48 | 06/11/2014 | 09:50:33 | Power Unit Pwr Unit Status | Power off/down | Asserted
  49 | 06/11/2014 | 09:50:49 | Power Unit Pwr Unit Status | Power off/down | Deasserted
  4a | 06/11/2014 | 09:50:49 | Button Button | Power Button pressed | Asserted
  4b | 06/11/2014 | 09:50:58 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  4c | 06/11/2014 | 09:50:58 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  4d | 06/11/2014 | 09:52:06 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  4e | 06/11/2014 | 09:52:06 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  4f | 06/11/2014 | 09:52:24 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
  50 | 06/11/2014 | 09:53:19 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  51 | 06/11/2014 | 09:53:19 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  52 | 06/11/2014 | 09:56:25 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  53 | 06/11/2014 | 09:56:26 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  54 | 06/11/2014 | 09:56:44 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
  55 | 06/11/2014 | 10:28:00 | Button Button | Reset Button pressed | Asserted
  56 | 06/11/2014 | 10:28:07 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  57 | 06/11/2014 | 10:28:07 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  58 | 06/11/2014 | 10:28:46 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  59 | 06/11/2014 | 10:28:46 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  5a | 06/11/2014 | 10:29:05 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
  5b | 06/11/2014 | 10:30:00 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  5c | 06/11/2014 | 10:30:00 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  5d | 06/11/2014 | 10:30:18 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
  5e | 06/11/2014 | 10:44:29 | Button Button | Power Button pressed | Asserted
  5f | 06/11/2014 | 10:44:33 | Button Button | Power Button pressed | Asserted
  60 | 06/11/2014 | 10:44:37 | Power Unit Pwr Unit Status | Power off/down | Asserted
  61 | 06/11/2014 | 10:54:13 | Power Supply PS1 Status | Power Supply AC lost | Asserted
  62 | 06/11/2014 | 11:22:16 | Power Unit Pwr Unit Status | Power off/down | Asserted
  63 | 06/11/2014 | 11:22:16 | Physical Security Physical Scrty | General Chassis intrusion | Asserted
  64 | 06/11/2014 | 11:22:58 | Button Button | Power Button pressed | Asserted
  65 | 06/11/2014 | 11:22:59 | Power Unit Pwr Unit Status | Power off/down | Deasserted
  66 | 06/11/2014 | 11:23:01 | Physical Security Physical Scrty | General Chassis intrusion | Deasserted
  67 | 06/11/2014 | 11:23:02 | Physical Security Physical Scrty | General Chassis intrusion | Asserted
  68 | 06/11/2014 | 11:23:08 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  69 | 06/11/2014 | 11:23:08 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  6a | 06/11/2014 | 11:24:18 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  6b | 06/11/2014 | 11:24:18 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  6c | 06/11/2014 | 11:24:18 | Power Unit Pwr Unit Status | Power off/down | Asserted
  6d | 06/11/2014 | 11:24:18 | Button Button | Power Button pressed | Asserted
  6e | 06/11/2014 | 11:27:15 | Physical Security Physical Scrty | General Chassis intrusion | Deasserted
  6f | 06/11/2014 | 11:27:39 | Power Unit Pwr Unit Status | Power off/down | Deasserted
  70 | 06/11/2014 | 11:27:39 | Button Button | Power Button pressed | Asserted
  71 | 06/11/2014 | 11:27:49 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  72 | 06/11/2014 | 11:27:49 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  73 | 06/11/2014 | 11:30:26 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  74 | 06/11/2014 | 11:30:26 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  75 | 06/11/2014 | 11:32:04 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  76 | 06/11/2014 | 11:32:05 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  77 | 06/11/2014 | 11:32:05 | Power Unit Pwr Unit Status | Power off/down | Asserted
  78 | 06/11/2014 | 11:32:05 | Button Button | Power Button pressed | Asserted
  79 | 06/11/2014 | 11:32:16 | Physical Security Physical Scrty | General Chassis intrusion | Asserted
  7a | 06/11/2014 | 11:33:14 | Physical Security Physical Scrty | General Chassis intrusion | Deasserted
  7b | 06/11/2014 | 11:33:15 | Physical Security Physical Scrty | General Chassis intrusion | Asserted
  7c | 06/11/2014 | 11:33:30 | Physical Security Physical Scrty | General Chassis intrusion | Deasserted
  7d | 06/11/2014 | 11:33:31 | Physical Security Physical Scrty | General Chassis intrusion | Asserted
  7e | 06/11/2014 | 11:33:39 | Physical Security Physical Scrty | General Chassis intrusion | Deasserted
  7f | 06/11/2014 | 11:33:41 | Physical Security Physical Scrty | General Chassis intrusion | Asserted
  80 | 06/11/2014 | 11:33:43 | Physical Security Physical Scrty | General Chassis intrusion | Deasserted
  81 | 06/11/2014 | 11:36:55 | Power Unit Pwr Unit Status | Power off/down | Deasserted
  82 | 06/11/2014 | 11:36:55 | Button Button | Power Button pressed | Asserted
  83 | 06/11/2014 | 11:37:05 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  84 | 06/11/2014 | 11:37:05 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  85 | 06/11/2014 | 11:38:08 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
  86 | 06/11/2014 | 11:38:35 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  87 | 06/11/2014 | 11:38:35 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  88 | 06/11/2014 | 11:40:24 | Power Unit Pwr Unit Status | Power off/down | Asserted
  89 | 06/11/2014 | 11:40:29 | Power Unit Pwr Unit Status | Power off/down | Deasserted
  8a | 06/11/2014 | 11:40:38 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  8b | 06/11/2014 | 11:40:39 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  8c | 06/11/2014 | 11:44:37 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
  8d | 06/11/2014 | 11:44:57 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  8e | 06/11/2014 | 11:44:57 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  8f | 06/11/2014 | 11:46:57 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  90 | 06/11/2014 | 11:46:58 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  91 | 06/11/2014 | 11:48:24 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
  92 | 06/11/2014 | 12:06:35 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  93 | 06/11/2014 | 12:06:35 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  94 | 06/11/2014 | 12:05:33 | Button Button | Power Button pressed | Asserted
  95 | 06/11/2014 | 12:05:34 | Power Unit Pwr Unit Status | Power off/down | Asserted
  96 | 06/11/2014 | 12:05:37 | Physical Security Physical Scrty | General Chassis intrusion | Asserted
  97 | 06/11/2014 | 12:06:57 | Physical Security Physical Scrty | General Chassis intrusion | Deasserted
  98 | 06/11/2014 | 12:07:15 | Physical Security Physical Scrty | General Chassis intrusion | Asserted
  99 | 06/11/2014 | 12:07:21 | Physical Security Physical Scrty | General Chassis intrusion | Deasserted
  9a | 06/11/2014 | 12:07:28 | Power Unit Pwr Unit Status | Power off/down | Deasserted
  9b | 06/11/2014 | 12:07:28 | Button Button | Power Button pressed | Asserted
  9c | 06/11/2014 | 12:07:37 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  9d | 06/11/2014 | 12:07:37 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  9e | 06/11/2014 | 12:10:06 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
  9f | 06/11/2014 | 12:10:29 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  a0 | 06/11/2014 | 12:10:29 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  a1 | 06/11/2014 | 12:10:57 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
  a2 | 06/11/2014 | 12:12:44 | Button Button | Reset Button pressed | Asserted
  a3 | 06/11/2014 | 12:12:52 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  a4 | 06/11/2014 | 12:12:52 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  a5 | 06/11/2014 | 12:13:11 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
  a6 | 06/11/2014 | 12:43:18 | Button Button | Power Button pressed | Asserted
  a7 | 06/11/2014 | 12:43:20 | Button Button | Power Button pressed | Asserted
  a8 | 06/11/2014 | 12:43:23 | Button Button | Power Button pressed | Asserted
  a9 | 06/11/2014 | 12:43:28 | Power Unit Pwr Unit Status | Power off/down | Asserted
  aa | 06/11/2014 | 12:43:37 | Physical Security Physical Scrty | General Chassis intrusion | Asserted
  ab | 06/11/2014 | 12:45:41 | Physical Security Physical Scrty | General Chassis intrusion | Deasserted
  ac | 06/11/2014 | 12:45:47 | Button Button | Power Button pressed | Asserted
  ad | 06/11/2014 | 12:45:48 | Power Unit Pwr Unit Status | Power off/down | Deasserted
  ae | 06/11/2014 | 12:45:57 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  af | 06/11/2014 | 12:45:57 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  b0 | 06/11/2014 | 12:46:27 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
  b1 | 06/11/2014 | 14:00:01 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  b2 | 06/11/2014 | 14:00:02 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  b3 | 06/11/2014 | 14:00:02 | Power Unit Pwr Unit Status | Power off/down | Asserted
  b4 | 06/11/2014 | 14:00:05 | Physical Security Physical Scrty | General Chassis intrusion | Asserted
  b5 | 06/11/2014 | 14:01:54 | Physical Security Physical Scrty | General Chassis intrusion | Deasserted
  b6 | 06/11/2014 | 14:02:03 | Physical Security Physical Scrty | General Chassis intrusion | Asserted
  b7 | 06/11/2014 | 14:02:05 | Physical Security Physical Scrty | General Chassis intrusion | Deasserted
  b8 | 06/11/2014 | 14:03:23 | Power Unit Pwr Unit Status | Power off/down | Deasserted
  b9 | 06/11/2014 | 14:03:23 | Button Button | Power Button pressed | Asserted
  ba | 06/11/2014 | 14:03:32 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  bb | 06/11/2014 | 14:03:32 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  bc | 06/11/2014 | 14:04:06 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
  bd | 06/11/2014 | 14:31:50 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  be | 06/11/2014 | 14:31:51 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  bf | 06/11/2014 | 14:33:17 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  c0 | 06/11/2014 | 14:33:17 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  c1 | 06/11/2014 | 14:33:55 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
  c2 | 06/11/2014 | 14:38:18 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  c3 | 06/11/2014 | 14:38:18 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  c4 | 06/11/2014 | 14:41:20 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  c5 | 06/11/2014 | 14:41:20 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  c6 | 06/11/2014 | 14:42:18 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
  c7 | 06/16/2014 | 07:45:32 | Button Button | Reset Button pressed | Asserted
  c8 | 06/16/2014 | 07:45:40 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  c9 | 06/16/2014 | 07:45:40 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  ca | 06/16/2014 | 07:46:05 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
  cb | 06/18/2014 | 14:12:41 | Power Supply PS1 Status | Predictive failure | Asserted
  cc | 06/18/2014 | 14:12:41 | Power Unit Pwr Unit Status | Failure detected | Asserted
  cd | 06/18/2014 | 14:12:42 | Power Unit Pwr Unit Status | Power off/down | Asserted
  ce | 06/18/2014 | 14:12:42 | Power Supply PS1 Status | Predictive failure | Deasserted
  cf | 06/18/2014 | 14:12:42 | Power Supply PS1 Status | Power Supply AC lost | Asserted
  d0 | 06/18/2014 | 14:24:17 | Power Unit Pwr Unit Status | Power off/down | Asserted
  d1 | 06/18/2014 | 14:24:17 | Power Unit Pwr Unit Status | AC lost | Asserted
  d2 | 06/18/2014 | 14:24:18 | Power Unit Pwr Unit Status | AC lost | Deasserted
  d3 | 06/18/2014 | 14:24:23 | Power Unit Pwr Unit Status | Power off/down | Deasserted
  d4 | 06/18/2014 | 14:24:23 | Button Button | Power Button pressed | Asserted
  d5 | 06/18/2014 | 14:24:32 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  d6 | 06/18/2014 | 14:24:32 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  d7 | 06/18/2014 | 14:24:53 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
  d8 | 06/19/2014 | 11:25:48 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  d9 | 06/19/2014 | 11:25:49 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  da | 06/19/2014 | 11:26:20 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
  db | 06/26/2014 | 13:58:12 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  dc | 06/26/2014 | 13:58:12 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  dd | 06/26/2014 | 13:58:11 | Power Unit Pwr Unit Status | Power off/down | Asserted
  de | 06/26/2014 | 14:43:52 | Power Unit Pwr Unit Status | Power off/down | Deasserted
  df | 06/26/2014 | 14:43:52 | Button Button | Power Button pressed | Asserted
  e0 | 06/26/2014 | 14:44:02 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  e1 | 06/26/2014 | 14:44:02 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  e2 | 06/26/2014 | 14:44:23 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
  e3 | 06/26/2014 | 15:03:55 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  e4 | 06/26/2014 | 15:03:56 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  e5 | 06/26/2014 | 15:03:56 | Power Unit Pwr Unit Status | Power off/down | Asserted
  e6 | 07/07/2014 | 07:44:50 | Power Unit Pwr Unit Status | Power off/down | Deasserted
  e7 | 07/07/2014 | 07:44:50 | Button Button | Power Button pressed | Asserted
  e8 | 07/07/2014 | 07:45:00 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  e9 | 07/07/2014 | 07:45:00 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  ea | 07/07/2014 | 07:45:18 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
  eb | 07/10/2014 | 07:45:44 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  ec | 07/10/2014 | 07:45:44 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  ed | 07/10/2014 | 07:46:15 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
  ee | 07/15/2014 | 10:51:52 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  ef | 07/15/2014 | 10:51:52 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  f0 | 07/15/2014 | 10:52:22 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
  f1 | 07/23/2014 | 12:01:10 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  f2 | 07/23/2014 | 12:01:10 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  f3 | 07/23/2014 | 12:01:40 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
  f4 | 07/23/2014 | 14:01:49 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  f5 | 07/23/2014 | 14:01:49 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  f6 | 07/23/2014 | 14:02:20 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
  f7 | 08/15/2014 | 07:42:54 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  f8 | 08/15/2014 | 07:41:15 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  f9 | 08/15/2014 | 07:41:46 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
  fa | 08/20/2014 | 13:04:41 | Physical Security Physical Scrty | System unplugged from LAN | Asserted
  fb | 08/20/2014 | 13:04:48 | Physical Security Physical Scrty | System unplugged from LAN | Deasserted
  fc | 08/26/2014 | 09:28:36 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  fd | 08/26/2014 | 09:28:35 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
  fe | 08/26/2014 | 09:29:06 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
  ff | 08/28/2014 | 07:55:38 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 100 | 08/28/2014 | 07:55:38 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 101 | 08/28/2014 | 07:56:09 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 102 | 09/04/2014 | 09:11:41 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 103 | 09/04/2014 | 09:11:40 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 104 | 09/04/2014 | 09:12:53 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 105 | 09/04/2014 | 11:50:40 | Button Button | Reset Button pressed | Asserted
 106 | 09/04/2014 | 11:50:47 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 107 | 09/04/2014 | 11:50:48 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 108 | 09/04/2014 | 11:51:08 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 109 | 09/05/2014 | 08:35:08 | Button Button | Power Button pressed | Asserted
 10a | 09/05/2014 | 08:35:09 | Button Button | Reset Button pressed | Asserted
 10b | 09/05/2014 | 08:35:16 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 10c | 09/05/2014 | 08:35:16 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 10d | 09/05/2014 | 08:35:36 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 10e | 09/08/2014 | 09:12:39 | Button Button | Reset Button pressed | Asserted
 10f | 09/08/2014 | 09:12:47 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 110 | 09/08/2014 | 09:12:47 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 111 | 09/08/2014 | 09:13:07 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 112 | 09/08/2014 | 09:27:53 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 113 | 09/08/2014 | 09:27:54 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 114 | 09/08/2014 | 09:28:25 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 115 | 09/10/2014 | 08:54:29 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 116 | 09/10/2014 | 08:54:29 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 117 | 09/10/2014 | 08:58:45 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 118 | 09/10/2014 | 08:58:45 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 119 | 09/10/2014 | 08:59:07 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 11a | 09/10/2014 | 15:34:44 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 11b | 09/10/2014 | 15:34:44 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 11c | 09/10/2014 | 15:35:06 | Button Button | Reset Button pressed | Asserted
 11d | 09/10/2014 | 15:35:14 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 11e | 09/10/2014 | 15:35:14 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 11f | 09/10/2014 | 15:35:42 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 120 | 09/10/2014 | 15:36:25 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 121 | 09/10/2014 | 15:38:33 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 122 | 09/10/2014 | 15:38:33 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 123 | 09/10/2014 | 15:38:54 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 124 | 09/15/2014 | 07:52:11 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 125 | 09/15/2014 | 07:52:11 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 126 | 09/15/2014 | 07:54:18 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 127 | 09/15/2014 | 09:35:15 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 128 | 09/15/2014 | 09:35:15 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 129 | 09/15/2014 | 09:35:35 | Button Button | Reset Button pressed | Asserted
 12a | 09/15/2014 | 09:35:42 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 12b | 09/15/2014 | 09:35:42 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 12c | 09/15/2014 | 09:36:09 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 12d | 09/15/2014 | 09:36:24 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 12e | 09/15/2014 | 09:45:22 | Button Button | Reset Button pressed | Asserted
 12f | 09/15/2014 | 09:45:29 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 130 | 09/15/2014 | 09:45:29 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 131 | 09/15/2014 | 09:45:57 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 132 | 09/15/2014 | 09:46:13 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 133 | 09/15/2014 | 09:53:44 | Button Button | Reset Button pressed | Asserted
 134 | 09/15/2014 | 09:53:52 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 135 | 09/15/2014 | 09:53:52 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 136 | 09/15/2014 | 09:54:18 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 137 | 09/15/2014 | 09:54:34 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 138 | 09/15/2014 | 09:56:25 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 139 | 09/15/2014 | 09:56:25 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 13a | 09/15/2014 | 09:56:51 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 13b | 09/15/2014 | 09:57:13 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 13c | 09/15/2014 | 09:57:14 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 13d | 09/15/2014 | 09:57:40 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 13e | 09/15/2014 | 09:58:40 | Button Button | Reset Button pressed | Asserted
 13f | 09/15/2014 | 09:58:47 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 140 | 09/15/2014 | 09:58:47 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 141 | 09/15/2014 | 09:59:09 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 142 | 09/17/2014 | 10:11:02 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 143 | 09/17/2014 | 10:11:01 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 144 | 09/17/2014 | 10:11:44 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 145 | 09/17/2014 | 10:12:09 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 146 | 09/17/2014 | 10:26:25 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 147 | 09/17/2014 | 10:26:26 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 148 | 09/17/2014 | 10:26:47 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 149 | 09/22/2014 | 10:08:42 | Button Button | Reset Button pressed | Asserted
 14a | 09/22/2014 | 10:08:49 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 14b | 09/22/2014 | 10:08:49 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 14c | 09/22/2014 | 10:09:09 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 14d | 09/23/2014 | 10:55:22 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 14e | 09/23/2014 | 10:55:22 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 14f | 09/23/2014 | 10:55:54 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 150 | 09/30/2014 | 12:00:44 | OS Stop/Shutdown | OS graceful shutdown | Asserted
 151 | 09/30/2014 | 12:00:44 | OEM record dd | 000157 | 000000000000
 152 | 09/30/2014 | 12:00:58 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 153 | 09/30/2014 | 12:00:58 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 154 | 09/30/2014 | 12:01:28 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 155 | 09/30/2014 | 12:36:14 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 156 | 09/30/2014 | 12:36:14 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 157 | 09/30/2014 | 12:36:45 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 158 | 09/30/2014 | 12:55:03 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 159 | 09/30/2014 | 12:55:04 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 15a | 09/30/2014 | 12:55:35 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 15b | 10/01/2014 | 08:50:11 | Button Button | Reset Button pressed | Asserted
 15c | 10/01/2014 | 08:50:19 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 15d | 10/01/2014 | 08:50:19 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 15e | 10/01/2014 | 08:50:39 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 15f | 10/01/2014 | 09:21:49 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 160 | 10/01/2014 | 09:21:50 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 161 | 10/01/2014 | 09:22:21 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 162 | 10/16/2014 | 16:07:08 | Button Button | Reset Button pressed | Asserted
 163 | 10/16/2014 | 16:07:15 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 164 | 10/16/2014 | 16:07:13 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 165 | 10/16/2014 | 16:07:34 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 166 | 10/17/2014 | 14:44:46 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 167 | 10/17/2014 | 14:44:46 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 168 | 10/17/2014 | 14:45:17 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 169 | 10/30/2014 | 07:39:12 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 16a | 10/30/2014 | 07:39:12 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 16b | 10/30/2014 | 07:39:41 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 16c | 11/11/2014 | 20:49:51 | Power Supply PS1 Status | Predictive failure | Asserted
 16d | 11/11/2014 | 20:49:52 | Power Supply PS1 Status | Predictive failure | Deasserted
 16e | 11/12/2014 | 09:02:16 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 16f | 11/12/2014 | 08:00:13 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 170 | 11/12/2014 | 08:00:44 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 171 | 11/18/2014 | 15:59:59 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 172 | 11/18/2014 | 15:59:59 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 173 | 11/18/2014 | 16:00:30 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 174 | 12/09/2014 | 14:33:30 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 175 | 12/09/2014 | 14:33:30 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 176 | 12/09/2014 | 14:34:11 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 177 | 12/09/2014 | 14:34:41 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 178 | 12/09/2014 | 14:34:42 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 179 | 12/09/2014 | 14:35:03 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 17a | 12/10/2014 | 12:15:50 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 17b | 12/10/2014 | 12:15:50 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 17c | 12/10/2014 | 12:16:21 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 17d | 12/16/2014 | 12:33:41 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 17e | 12/16/2014 | 12:32:57 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 17f | 12/16/2014 | 12:33:28 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 180 | 01/05/2015 | 08:33:33 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 181 | 01/05/2015 | 08:33:10 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 182 | 01/05/2015 | 08:33:41 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 183 | 01/07/2015 | 15:51:14 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 184 | 01/07/2015 | 15:51:13 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 185 | 01/07/2015 | 15:51:44 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 186 | 01/14/2015 | 11:56:40 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 187 | 01/14/2015 | 11:56:40 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 188 | 01/14/2015 | 11:57:10 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 189 | 01/19/2015 | 15:18:18 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 18a | 01/19/2015 | 15:18:18 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 18b | 01/19/2015 | 15:18:49 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 18c | 02/11/2015 | 10:23:18 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 18d | 02/11/2015 | 10:23:18 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 18e | 02/11/2015 | 10:23:46 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 18f | 02/12/2015 | 12:23:13 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 190 | 02/12/2015 | 12:23:14 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 191 | 02/12/2015 | 12:23:45 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 192 | 02/18/2015 | 16:00:07 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 193 | 02/18/2015 | 16:00:07 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 194 | 02/18/2015 | 16:00:07 | Power Unit Pwr Unit Status | Power off/down | Asserted
 195 | 02/18/2015 | 16:00:25 | Physical Security Physical Scrty | System unplugged from LAN | Asserted
 196 | 02/19/2015 | 07:29:57 | Power Supply PS1 Status | Power Supply AC lost | Asserted
 197 | 02/19/2015 | 08:19:00 | Power Unit Pwr Unit Status | Power off/down | Asserted
 198 | 02/19/2015 | 08:23:34 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 199 | 02/19/2015 | 08:23:43 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 19a | 02/19/2015 | 08:23:43 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 19b | 02/19/2015 | 08:24:05 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 19c | 02/20/2015 | 15:42:08 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 19d | 02/20/2015 | 15:42:08 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 19e | 02/20/2015 | 15:42:39 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 19f | 02/23/2015 | 08:12:50 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1a0 | 02/23/2015 | 08:12:51 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1a1 | 02/23/2015 | 08:13:22 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 1a2 | 03/03/2015 | 08:18:45 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1a3 | 03/03/2015 | 08:18:44 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1a4 | 03/03/2015 | 08:19:15 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 1a5 | 03/23/2015 | 08:26:59 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1a6 | 03/23/2015 | 09:26:49 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1a7 | 03/23/2015 | 09:27:20 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 1a8 | 03/24/2015 | 07:40:47 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1a9 | 03/24/2015 | 07:40:47 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1aa | 03/24/2015 | 07:41:18 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 1ab | 03/30/2015 | 12:28:49 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1ac | 03/30/2015 | 12:28:49 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1ad | 03/30/2015 | 12:29:19 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 1ae | 03/30/2015 | 12:49:14 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1af | 03/30/2015 | 12:49:15 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1b0 | 03/30/2015 | 12:49:46 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 1b1 | 04/13/2015 | 07:58:06 | Physical Security Physical Scrty | System unplugged from LAN | Asserted
 1b2 | 04/13/2015 | 08:00:33 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1b3 | 04/13/2015 | 08:00:31 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1b4 | 04/13/2015 | 08:00:31 | Power Unit Pwr Unit Status | Power off/down | Asserted
 1b5 | 04/13/2015 | 08:00:45 | Power Supply PS1 Status | Power Supply AC lost | Asserted
 1b6 | 04/13/2015 | 08:36:44 | Power Unit Pwr Unit Status | Power off/down | Asserted
 1b7 | 04/13/2015 | 08:41:18 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 1b8 | 04/13/2015 | 08:41:28 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1b9 | 04/13/2015 | 08:41:28 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1ba | 04/13/2015 | 08:41:49 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 1bb | 04/20/2015 | 07:56:14 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1bc | 04/20/2015 | 07:56:14 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1bd | 04/20/2015 | 07:56:45 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 1be | 04/20/2015 | 08:42:00 | Physical Security Physical Scrty | System unplugged from LAN | Asserted
 1bf | 04/20/2015 | 08:45:39 | Physical Security Physical Scrty | System unplugged from LAN | Deasserted
 1c0 | 04/20/2015 | 09:16:36 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1c1 | 04/20/2015 | 09:16:36 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1c2 | 04/20/2015 | 09:17:07 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 1c3 | 04/23/2015 | 07:58:43 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1c4 | 04/23/2015 | 07:58:43 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1c5 | 04/23/2015 | 07:59:14 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 1c6 | 05/04/2015 | 12:15:36 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1c7 | 05/04/2015 | 12:15:36 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1c8 | 05/04/2015 | 12:15:35 | Power Unit Pwr Unit Status | Power off/down | Asserted
 1c9 | 05/04/2015 | 12:16:34 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 1ca | 05/04/2015 | 12:16:34 | Button Button | Power Button pressed | Asserted
 1cb | 05/04/2015 | 12:16:44 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1cc | 05/04/2015 | 12:16:44 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1cd | 05/04/2015 | 12:17:05 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 1ce | 05/05/2015 | 12:49:36 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1cf | 05/05/2015 | 12:49:37 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1d0 | 05/05/2015 | 12:50:08 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 1d1 | 05/08/2015 | 08:24:44 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1d2 | 05/08/2015 | 08:24:44 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1d3 | 05/08/2015 | 08:25:15 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 1d4 | 05/11/2015 | 11:11:09 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1d5 | 05/11/2015 | 11:11:09 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1d6 | 05/11/2015 | 11:11:39 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 1d7 | 05/18/2015 | 08:58:21 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1d8 | 05/18/2015 | 08:58:20 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1d9 | 05/18/2015 | 08:58:51 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 1da | 05/21/2015 | 08:45:55 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1db | 05/21/2015 | 08:43:54 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1dc | 05/21/2015 | 08:44:25 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 1dd | 05/21/2015 | 09:15:51 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1de | 05/21/2015 | 09:15:52 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1df | 05/21/2015 | 09:17:22 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 1e0 | 05/21/2015 | 09:18:25 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1e1 | 05/21/2015 | 09:18:25 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1e2 | 05/21/2015 | 09:18:47 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 1e3 | 05/21/2015 | 10:11:23 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1e4 | 05/21/2015 | 10:11:23 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1e5 | 05/21/2015 | 10:13:02 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1e6 | 05/21/2015 | 10:13:02 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1e7 | 05/21/2015 | 10:13:28 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 1e8 | 05/21/2015 | 10:14:01 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 1e9 | 05/21/2015 | 10:33:35 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1ea | 05/21/2015 | 10:33:35 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1eb | 05/21/2015 | 10:33:56 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 1ec | 05/21/2015 | 10:34:14 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 1ed | 05/21/2015 | 10:41:45 | Button Button | Power Button pressed | Asserted
 1ee | 05/21/2015 | 10:41:55 | Button Button | Power Button pressed | Asserted
 1ef | 05/21/2015 | 10:41:59 | Power Unit Pwr Unit Status | Power off/down | Asserted
 1f0 | 05/21/2015 | 10:42:02 | Button Button | Power Button pressed | Asserted
 1f1 | 05/21/2015 | 10:42:06 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 1f2 | 05/21/2015 | 10:42:06 | Button Button | Power Button pressed | Asserted
 1f3 | 05/21/2015 | 10:42:15 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1f4 | 05/21/2015 | 10:42:15 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1f5 | 05/21/2015 | 10:43:02 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1f6 | 05/21/2015 | 10:43:02 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1f7 | 05/21/2015 | 10:43:23 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 1f8 | 06/01/2015 | 15:14:28 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1f9 | 06/01/2015 | 15:14:27 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1fa | 06/01/2015 | 15:15:07 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 1fb | 06/01/2015 | 15:15:21 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 1fc | 06/01/2015 | 15:24:11 | Button Button | Reset Button pressed | Asserted
 1fd | 06/01/2015 | 15:24:18 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1fe | 06/01/2015 | 15:24:18 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 1ff | 06/01/2015 | 15:25:14 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 200 | 06/01/2015 | 15:25:14 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 201 | 06/01/2015 | 15:25:34 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 202 | 06/01/2015 | 15:25:58 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 203 | 06/01/2015 | 15:25:58 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 204 | 06/01/2015 | 15:26:50 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 205 | 06/01/2015 | 15:26:50 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 206 | 06/01/2015 | 15:29:11 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 207 | 06/01/2015 | 15:29:12 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 208 | 06/01/2015 | 15:29:40 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 209 | 06/01/2015 | 15:30:14 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 20a | 06/01/2015 | 15:39:41 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 20b | 06/01/2015 | 15:39:41 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 20c | 06/01/2015 | 15:40:25 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 20d | 06/01/2015 | 15:40:25 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 20e | 06/01/2015 | 15:40:46 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 20f | 06/02/2015 | 07:42:59 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 210 | 06/02/2015 | 07:42:59 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 211 | 06/02/2015 | 07:43:53 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 212 | 06/02/2015 | 07:43:54 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 213 | 06/02/2015 | 07:44:15 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 214 | 06/02/2015 | 07:45:03 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 215 | 06/02/2015 | 07:49:14 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 216 | 06/02/2015 | 07:49:14 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 217 | 06/02/2015 | 07:49:40 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 218 | 06/02/2015 | 07:50:51 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 219 | 06/02/2015 | 07:50:51 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 21a | 06/02/2015 | 07:51:38 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 21b | 06/02/2015 | 07:51:39 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 21c | 06/02/2015 | 07:52:00 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 21d | 06/02/2015 | 08:31:40 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 21e | 06/02/2015 | 08:31:41 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 21f | 06/02/2015 | 08:32:35 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 220 | 06/02/2015 | 08:32:35 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 221 | 06/02/2015 | 08:33:01 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 222 | 06/02/2015 | 08:34:25 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 223 | 06/02/2015 | 08:43:53 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 224 | 06/02/2015 | 08:43:53 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 225 | 06/02/2015 | 08:44:21 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 226 | 06/02/2015 | 08:56:37 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 227 | 06/02/2015 | 08:56:37 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 228 | 06/02/2015 | 08:57:16 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 229 | 06/02/2015 | 08:57:52 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 22a | 06/02/2015 | 09:15:15 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 22b | 06/02/2015 | 09:15:15 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 22c | 06/02/2015 | 09:15:37 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 22d | 06/02/2015 | 09:15:52 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 22e | 06/02/2015 | 09:24:15 | Button Button | Reset Button pressed | Asserted
 22f | 06/02/2015 | 09:24:22 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 230 | 06/02/2015 | 09:24:22 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 231 | 06/02/2015 | 09:25:04 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 232 | 06/02/2015 | 09:25:04 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 233 | 06/02/2015 | 09:25:26 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 234 | 06/02/2015 | 10:05:46 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 235 | 06/02/2015 | 10:05:46 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 236 | 06/02/2015 | 10:05:46 | Power Unit Pwr Unit Status | Power off/down | Asserted
 237 | 06/02/2015 | 10:07:38 | Physical Security Physical Scrty | General Chassis intrusion | Asserted
 238 | 06/02/2015 | 10:25:09 | Physical Security Physical Scrty | General Chassis intrusion | Deasserted
 239 | 06/02/2015 | 10:25:42 | Button Button | Power Button pressed | Asserted
 23a | 06/02/2015 | 10:25:43 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 23b | 06/02/2015 | 10:25:52 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 23c | 06/02/2015 | 10:25:52 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 23d | 06/02/2015 | 10:26:37 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 23e | 06/02/2015 | 10:33:35 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 23f | 06/02/2015 | 10:33:35 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 240 | 06/02/2015 | 10:34:23 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 241 | 06/02/2015 | 10:34:23 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 242 | 06/02/2015 | 10:34:42 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 243 | 06/02/2015 | 10:35:09 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 244 | 06/02/2015 | 10:47:10 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 245 | 06/02/2015 | 10:47:10 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 246 | 06/02/2015 | 10:47:28 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 247 | 06/02/2015 | 10:47:45 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 248 | 06/02/2015 | 12:35:27 | Button Button | Power Button pressed | Asserted
 249 | 06/02/2015 | 12:36:25 | Button Button | Reset Button pressed | Asserted
 24a | 06/02/2015 | 12:36:32 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 24b | 06/02/2015 | 12:36:33 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 24c | 06/02/2015 | 12:36:51 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 24d | 06/02/2015 | 12:37:08 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 24e | 06/02/2015 | 15:13:16 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 24f | 06/02/2015 | 15:13:16 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 250 | 06/02/2015 | 15:15:30 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 251 | 06/02/2015 | 15:15:31 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 252 | 06/02/2015 | 15:15:50 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 253 | 06/02/2015 | 15:16:04 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 254 | 06/03/2015 | 07:37:22 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 255 | 06/03/2015 | 07:37:22 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 256 | 06/03/2015 | 07:37:40 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 257 | 06/03/2015 | 07:38:00 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 258 | 06/03/2015 | 09:32:16 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 259 | 06/03/2015 | 09:32:16 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 25a | 06/03/2015 | 09:32:40 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 25b | 06/03/2015 | 09:34:09 | OS Boot | C: boot completed | Asserted
 25c | 06/03/2015 | 09:34:09 | OEM record dc | 000137 | 00c4c96e5500
 25d | 06/03/2015 | 09:55:00 | OS Stop/Shutdown | OS graceful shutdown | Asserted
 25e | 06/03/2015 | 09:55:00 | OEM record dd | 000137 | 000000000000
 25f | 06/03/2015 | 09:55:12 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 260 | 06/03/2015 | 09:55:12 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 261 | 06/03/2015 | 09:55:30 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 262 | 06/03/2015 | 09:55:45 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 263 | 06/03/2015 | 10:00:21 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 264 | 06/03/2015 | 10:00:21 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 265 | 06/03/2015 | 10:00:40 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 266 | 06/03/2015 | 10:00:56 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 267 | 06/03/2015 | 13:04:43 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 268 | 06/03/2015 | 13:04:44 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 269 | 06/03/2015 | 13:05:02 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 26a | 06/03/2015 | 13:05:19 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 26b | 06/03/2015 | 13:10:19 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 26c | 06/03/2015 | 13:10:20 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 26d | 06/03/2015 | 13:10:38 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 26e | 06/03/2015 | 13:10:52 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 26f | 06/04/2015 | 08:55:26 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 270 | 06/04/2015 | 08:55:26 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 271 | 06/04/2015 | 08:55:48 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 272 | 06/04/2015 | 08:56:14 | OS Boot | C: boot completed | Asserted
 273 | 06/04/2015 | 08:56:14 | OEM record dc | 000137 | 00a012705500
 274 | 06/04/2015 | 09:54:33 | OS Stop/Shutdown | OS graceful shutdown | Asserted
 275 | 06/04/2015 | 09:54:33 | OEM record dd | 000137 | 000000000000
 276 | 06/04/2015 | 09:54:45 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 277 | 06/04/2015 | 09:54:45 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 278 | 06/04/2015 | 09:55:08 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 279 | 06/04/2015 | 09:55:23 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 27a | 06/04/2015 | 12:10:19 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 27b | 06/04/2015 | 12:10:19 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 27c | 06/04/2015 | 12:10:38 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 27d | 06/04/2015 | 12:10:52 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 27e | 06/04/2015 | 12:20:32 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 27f | 06/04/2015 | 12:20:33 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 280 | 06/04/2015 | 12:20:51 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 281 | 06/04/2015 | 12:21:08 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 282 | 06/04/2015 | 12:31:24 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 283 | 06/04/2015 | 12:31:24 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 284 | 06/04/2015 | 12:31:42 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 285 | 06/04/2015 | 12:31:56 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 286 | 06/04/2015 | 12:36:12 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 287 | 06/04/2015 | 12:36:12 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 288 | 06/04/2015 | 12:36:30 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 289 | 06/04/2015 | 12:36:44 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 28a | 06/05/2015 | 13:24:57 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 28b | 06/05/2015 | 13:24:57 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 28c | 06/05/2015 | 13:25:16 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 28d | 06/05/2015 | 13:25:30 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 28e | 06/05/2015 | 13:30:51 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 28f | 06/05/2015 | 13:30:51 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 290 | 06/05/2015 | 13:31:09 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 291 | 06/05/2015 | 13:31:25 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 292 | 06/05/2015 | 13:35:13 | Button Button | Reset Button pressed | Asserted
 293 | 06/05/2015 | 13:35:20 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 294 | 06/05/2015 | 13:35:20 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 295 | 06/05/2015 | 13:35:38 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 296 | 06/05/2015 | 13:35:52 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 297 | 06/05/2015 | 13:41:17 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 298 | 06/05/2015 | 13:41:18 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 299 | 06/05/2015 | 13:41:36 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 29a | 06/05/2015 | 13:41:51 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 29b | 06/08/2015 | 10:01:12 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 29c | 06/08/2015 | 10:01:12 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 29d | 06/08/2015 | 10:03:00 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 29e | 06/08/2015 | 10:03:01 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 29f | 06/08/2015 | 10:03:20 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 2a0 | 06/08/2015 | 10:03:33 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 2a1 | 06/16/2015 | 12:54:38 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 2a2 | 06/16/2015 | 12:54:38 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 2a3 | 06/16/2015 | 12:54:56 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 2a4 | 06/16/2015 | 12:55:12 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 2a5 | 06/18/2015 | 08:09:12 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 2a6 | 06/18/2015 | 08:09:12 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 2a7 | 06/18/2015 | 08:09:30 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 2a8 | 06/18/2015 | 08:09:47 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 2a9 | 06/19/2015 | 08:06:38 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 2aa | 06/19/2015 | 08:06:38 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 2ab | 06/19/2015 | 08:06:56 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 2ac | 06/19/2015 | 08:07:13 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 2ad | 06/25/2015 | 09:36:56 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 2ae | 06/25/2015 | 09:36:55 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 2af | 06/25/2015 | 09:38:56 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 2b0 | 06/25/2015 | 09:38:56 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 2b1 | 06/25/2015 | 09:39:15 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 2b2 | 06/25/2015 | 09:39:29 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 2b3 | 07/07/2015 | 08:32:52 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 2b4 | 07/07/2015 | 08:32:52 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 2b5 | 07/07/2015 | 08:33:09 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 2b6 | 07/07/2015 | 08:33:23 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 2b7 | 07/07/2015 | 09:44:39 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 2b8 | 07/07/2015 | 09:44:39 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 2b9 | 07/07/2015 | 09:46:22 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 2ba | 07/07/2015 | 09:46:23 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 2bb | 07/07/2015 | 09:46:41 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 2bc | 07/07/2015 | 09:46:56 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 2bd | 07/07/2015 | 14:39:23 | Temperature SSB Temp | Lower Non-critical going low  | Asserted | Reading 0 < Threshold 5 degrees C
 2be | 07/07/2015 | 14:39:23 | Temperature SSB Temp | Lower Critical going low  | Asserted | Reading 0 < Threshold 0 degrees C
 2bf | 07/07/2015 | 14:39:24 | Temperature SSB Temp | Lower Critical going low  | Deasserted | Reading 43 < Threshold 0 degrees C
 2c0 | 07/07/2015 | 14:39:24 | Temperature SSB Temp | Lower Non-critical going low  | Deasserted | Reading 43 < Threshold 5 degrees C
 2c1 | 07/08/2015 | 19:01:56 | Temperature SSB Temp | Lower Non-critical going low  | Asserted | Reading 0 < Threshold 5 degrees C
 2c2 | 07/08/2015 | 19:01:56 | Temperature SSB Temp | Lower Critical going low  | Asserted | Reading 0 < Threshold 0 degrees C
 2c3 | 07/08/2015 | 19:01:57 | Temperature SSB Temp | Lower Critical going low  | Deasserted | Reading 43 < Threshold 0 degrees C
 2c4 | 07/08/2015 | 19:01:57 | Temperature SSB Temp | Lower Non-critical going low  | Deasserted | Reading 43 < Threshold 5 degrees C
 2c5 | 07/08/2015 | 22:11:02 | Temperature SSB Temp | Lower Non-critical going low  | Asserted | Reading 0 < Threshold 5 degrees C
 2c6 | 07/08/2015 | 22:11:02 | Temperature SSB Temp | Lower Critical going low  | Asserted | Reading 0 < Threshold 0 degrees C
 2c7 | 07/08/2015 | 22:11:03 | Temperature SSB Temp | Lower Critical going low  | Deasserted | Reading 43 < Threshold 0 degrees C
 2c8 | 07/08/2015 | 22:11:03 | Temperature SSB Temp | Lower Non-critical going low  | Deasserted | Reading 43 < Threshold 5 degrees C
 2c9 | 07/09/2015 | 06:33:02 | Temperature SSB Temp | Lower Non-critical going low  | Asserted | Reading 0 < Threshold 5 degrees C
 2ca | 07/09/2015 | 06:33:02 | Temperature SSB Temp | Lower Critical going low  | Asserted | Reading 0 < Threshold 0 degrees C
 2cb | 07/09/2015 | 06:33:04 | Temperature SSB Temp | Lower Critical going low  | Deasserted | Reading 43 < Threshold 0 degrees C
 2cc | 07/09/2015 | 06:33:04 | Temperature SSB Temp | Lower Non-critical going low  | Deasserted | Reading 43 < Threshold 5 degrees C
 2cd | 07/13/2015 | 12:00:27 | Memory Mmry ECC Sensor | Uncorrectable ECC | Asserted
 2ce | 07/13/2015 | 12:00:28 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 2cf | 07/13/2015 | 12:01:33 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 2d0 | 07/13/2015 | 12:01:34 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 2d1 | 07/13/2015 | 12:01:52 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 2d2 | 07/13/2015 | 12:02:07 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 2d3 | 07/13/2015 | 12:05:54 | Button Button | Reset Button pressed | Asserted
 2d4 | 07/13/2015 | 12:06:01 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 2d5 | 07/13/2015 | 12:06:01 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 2d6 | 07/13/2015 | 12:06:19 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 2d7 | 07/13/2015 | 12:06:41 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 2d8 | 08/11/2015 | 10:33:01 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 2d9 | 08/11/2015 | 10:32:57 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 2da | 08/11/2015 | 10:33:15 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 2db | 08/11/2015 | 10:33:29 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 2dc | 10/19/2015 | 08:38:32 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 2dd | 10/19/2015 | 08:38:23 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 2de | 10/19/2015 | 08:38:41 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 2df | 10/19/2015 | 08:38:56 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 2e0 | 10/29/2015 | 11:03:47 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 2e1 | 10/29/2015 | 11:03:46 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 2e2 | 10/29/2015 | 11:04:04 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 2e3 | 10/29/2015 | 11:04:21 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 2e4 | 12/31/2015 | 16:11:36 | Power Unit Pwr Unit Status | Failure detected | Asserted
 2e5 | 12/31/2015 | 16:11:36 | Power Unit Pwr Unit Status | Power off/down | Asserted
 2e6 | 12/31/2015 | 16:11:36 | Power Supply PS1 Status | Power Supply AC lost | Asserted
 2e7 | 12/31/2015 | 16:11:41 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 2e8 | 12/31/2015 | 16:11:43 | Power Supply PS1 Status | Power Supply AC lost | Deasserted
 2e9 | 12/31/2015 | 16:11:43 | Power Unit Pwr Unit Status | Failure detected | Deasserted
 2ea | 12/31/2015 | 16:11:48 | Physical Security Physical Scrty | System unplugged from LAN | Asserted
 2eb | 12/31/2015 | 16:11:49 | Physical Security Physical Scrty | System unplugged from LAN | Deasserted
 2ec | 12/31/2015 | 16:11:52 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 2ed | 12/31/2015 | 16:11:52 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 2ee | 12/31/2015 | 15:07:58 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 2ef | 12/31/2015 | 15:08:14 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 2f0 | 01/05/2016 | 08:03:11 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 2f1 | 01/05/2016 | 08:03:11 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 2f2 | 01/05/2016 | 08:03:29 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 2f3 | 01/05/2016 | 08:03:46 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 2f4 | 01/05/2016 | 08:48:30 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 2f5 | 01/05/2016 | 08:48:30 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 2f6 | 01/05/2016 | 08:48:48 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 2f7 | 01/05/2016 | 08:49:05 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 2f8 | 01/05/2016 | 08:51:04 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 2f9 | 01/05/2016 | 08:51:04 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 2fa | 01/05/2016 | 08:51:23 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 2fb | 01/05/2016 | 08:51:39 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 2fc | 01/07/2016 | 12:54:48 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 2fd | 01/07/2016 | 12:54:49 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 2fe | 01/07/2016 | 12:55:07 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 2ff | 01/07/2016 | 12:55:22 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 300 | 01/15/2016 | 08:46:23 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 301 | 01/15/2016 | 08:46:23 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 302 | 01/15/2016 | 08:46:41 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 303 | 01/15/2016 | 08:46:56 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 304 | 01/15/2016 | 08:49:01 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 305 | 01/15/2016 | 08:49:01 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 306 | 01/15/2016 | 08:49:19 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 307 | 01/15/2016 | 08:49:36 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 308 | 01/15/2016 | 10:14:36 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 309 | 01/15/2016 | 10:14:36 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 30a | 01/15/2016 | 10:14:37 | Power Unit Pwr Unit Status | Power off/down | Asserted
 30b | 01/15/2016 | 10:19:03 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 30c | 01/15/2016 | 10:19:03 | Button Button | Power Button pressed | Asserted
 30d | 01/15/2016 | 10:19:11 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 30e | 01/15/2016 | 10:19:11 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 30f | 01/15/2016 | 10:19:31 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 310 | 01/15/2016 | 10:19:45 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 311 | 01/15/2016 | 10:39:01 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 312 | 01/15/2016 | 10:39:01 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 313 | 01/15/2016 | 10:40:47 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 314 | 01/15/2016 | 10:40:47 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 315 | 01/15/2016 | 10:41:06 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 316 | 01/15/2016 | 10:41:20 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 317 | 01/20/2016 | 11:44:18 | Temperature SSB Temp | Lower Non-critical going low  | Asserted | Reading 0 < Threshold 5 degrees C
 318 | 01/20/2016 | 11:44:18 | Temperature SSB Temp | Lower Critical going low  | Asserted | Reading 0 < Threshold 0 degrees C
 319 | 01/20/2016 | 11:44:19 | Temperature SSB Temp | Lower Critical going low  | Deasserted | Reading 43 < Threshold 0 degrees C
 31a | 01/20/2016 | 11:44:19 | Temperature SSB Temp | Lower Non-critical going low  | Deasserted | Reading 43 < Threshold 5 degrees C
 31b | 01/20/2016 | 14:24:33 | Temperature SSB Temp | Lower Non-critical going low  | Asserted | Reading 0 < Threshold 5 degrees C
 31c | 01/20/2016 | 14:24:33 | Temperature SSB Temp | Lower Critical going low  | Asserted | Reading 0 < Threshold 0 degrees C
 31d | 01/20/2016 | 14:24:34 | Temperature SSB Temp | Lower Critical going low  | Deasserted | Reading 43 < Threshold 0 degrees C
 31e | 01/20/2016 | 14:24:34 | Temperature SSB Temp | Lower Non-critical going low  | Deasserted | Reading 43 < Threshold 5 degrees C
 31f | 01/20/2016 | 17:19:00 | Temperature SSB Temp | Lower Non-critical going low  | Asserted | Reading 0 < Threshold 5 degrees C
 320 | 01/20/2016 | 17:19:00 | Temperature SSB Temp | Lower Critical going low  | Asserted | Reading 0 < Threshold 0 degrees C
 321 | 01/20/2016 | 17:19:01 | Temperature SSB Temp | Lower Critical going low  | Deasserted | Reading 43 < Threshold 0 degrees C
 322 | 01/20/2016 | 17:19:01 | Temperature SSB Temp | Lower Non-critical going low  | Deasserted | Reading 43 < Threshold 5 degrees C
 323 | 01/21/2016 | 08:04:57 | Temperature SSB Temp | Lower Non-critical going low  | Asserted | Reading 0 < Threshold 5 degrees C
 324 | 01/21/2016 | 08:04:57 | Temperature SSB Temp | Lower Critical going low  | Asserted | Reading 0 < Threshold 0 degrees C
 325 | 01/21/2016 | 08:04:58 | Temperature SSB Temp | Lower Critical going low  | Deasserted | Reading 43 < Threshold 0 degrees C
 326 | 01/21/2016 | 08:04:58 | Temperature SSB Temp | Lower Non-critical going low  | Deasserted | Reading 43 < Threshold 5 degrees C
 327 | 01/21/2016 | 09:37:44 | Temperature SSB Temp | Lower Non-critical going low  | Asserted | Reading 0 < Threshold 5 degrees C
 328 | 01/21/2016 | 09:37:44 | Temperature SSB Temp | Lower Critical going low  | Asserted | Reading 0 < Threshold 0 degrees C
 329 | 01/21/2016 | 09:37:45 | Temperature SSB Temp | Lower Critical going low  | Deasserted | Reading 43 < Threshold 0 degrees C
 32a | 01/21/2016 | 09:37:45 | Temperature SSB Temp | Lower Non-critical going low  | Deasserted | Reading 43 < Threshold 5 degrees C
 32b | 01/21/2016 | 11:04:07 | Temperature SSB Temp | Lower Non-critical going low  | Asserted | Reading 0 < Threshold 5 degrees C
 32c | 01/21/2016 | 11:04:07 | Temperature SSB Temp | Lower Critical going low  | Asserted | Reading 0 < Threshold 0 degrees C
 32d | 01/21/2016 | 11:04:08 | Temperature SSB Temp | Lower Critical going low  | Deasserted | Reading 43 < Threshold 0 degrees C
 32e | 01/21/2016 | 11:04:08 | Temperature SSB Temp | Lower Non-critical going low  | Deasserted | Reading 43 < Threshold 5 degrees C
 32f | 02/16/2016 | 09:53:34 | Temperature SSB Temp | Lower Non-critical going low  | Asserted | Reading 0 < Threshold 5 degrees C
 330 | 02/16/2016 | 09:53:34 | Temperature SSB Temp | Lower Critical going low  | Asserted | Reading 0 < Threshold 0 degrees C
 331 | 02/16/2016 | 09:53:35 | Temperature SSB Temp | Lower Critical going low  | Deasserted | Reading 43 < Threshold 0 degrees C
 332 | 02/16/2016 | 09:53:35 | Temperature SSB Temp | Lower Non-critical going low  | Deasserted | Reading 43 < Threshold 5 degrees C
 333 | 04/22/2016 | 12:07:47 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 334 | 04/22/2016 | 12:07:47 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 335 | 04/22/2016 | 12:07:53 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 336 | 04/22/2016 | 12:08:10 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 337 | 04/22/2016 | 13:47:10 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 338 | 04/22/2016 | 13:47:11 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 339 | 04/22/2016 | 13:47:29 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 33a | 04/22/2016 | 13:47:46 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 33b | 06/20/2016 | 12:17:27 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 33c | 06/20/2016 | 12:17:27 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 33d | 06/20/2016 | 12:18:40 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 33e | 06/20/2016 | 12:18:40 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 33f | 06/20/2016 | 12:18:59 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 340 | 06/20/2016 | 12:19:29 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 341 | 06/20/2016 | 12:26:46 | Button Button | Power Button pressed | Asserted
 342 | 06/20/2016 | 12:26:51 | Power Unit Pwr Unit Status | Power off/down | Asserted
 343 | 06/20/2016 | 12:26:53 | Button Button | Power Button pressed | Asserted
 344 | 06/20/2016 | 12:26:57 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 345 | 06/20/2016 | 12:27:06 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 346 | 06/20/2016 | 12:27:06 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 347 | 06/20/2016 | 12:27:48 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 348 | 06/20/2016 | 12:27:48 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 349 | 06/20/2016 | 12:28:08 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 34a | 06/20/2016 | 12:28:25 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 34b | 06/20/2016 | 12:33:26 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 34c | 06/20/2016 | 12:33:27 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 34d | 06/20/2016 | 12:33:45 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 34e | 06/20/2016 | 12:34:01 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 34f | 06/20/2016 | 12:36:33 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 350 | 06/20/2016 | 12:36:33 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 351 | 06/20/2016 | 12:36:57 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 352 | 06/20/2016 | 12:37:23 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 353 | 06/20/2016 | 12:40:49 | Button Button | Reset Button pressed | Asserted
 354 | 06/20/2016 | 12:40:56 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 355 | 06/20/2016 | 12:40:56 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 356 | 06/20/2016 | 12:41:15 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 357 | 06/20/2016 | 12:41:33 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 358 | 06/27/2016 | 06:55:23 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 359 | 06/27/2016 | 06:55:23 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 35a | 06/27/2016 | 06:57:28 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 35b | 06/27/2016 | 06:57:29 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 35c | 06/27/2016 | 06:57:48 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 35d | 06/27/2016 | 06:58:16 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 35e | 06/27/2016 | 07:14:00 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 35f | 06/27/2016 | 07:14:00 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 360 | 06/27/2016 | 07:14:18 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 361 | 06/27/2016 | 07:14:38 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 362 | 06/27/2016 | 07:17:50 | Button Button | Reset Button pressed | Asserted
 363 | 06/27/2016 | 07:17:57 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 364 | 06/27/2016 | 07:17:57 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 365 | 06/27/2016 | 07:18:15 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 366 | 06/27/2016 | 07:18:36 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 367 | 06/27/2016 | 07:51:44 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 368 | 06/27/2016 | 07:51:45 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 369 | 06/27/2016 | 07:52:03 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 36a | 06/27/2016 | 07:52:18 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 36b | 06/27/2016 | 08:02:22 | Button Button | Reset Button pressed | Asserted
 36c | 06/27/2016 | 08:02:29 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 36d | 06/27/2016 | 08:02:30 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 36e | 06/27/2016 | 08:02:48 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 36f | 06/27/2016 | 08:03:10 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 370 | 06/27/2016 | 08:06:42 | Button Button | Reset Button pressed | Asserted
 371 | 06/27/2016 | 08:06:49 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 372 | 06/27/2016 | 08:06:49 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 373 | 06/27/2016 | 08:07:08 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 374 | 06/27/2016 | 08:07:30 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 375 | 06/27/2016 | 08:15:48 | Button Button | Reset Button pressed | Asserted
 376 | 06/27/2016 | 08:15:55 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 377 | 06/27/2016 | 08:15:55 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 378 | 06/27/2016 | 08:16:37 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 379 | 06/27/2016 | 08:16:37 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 37a | 06/27/2016 | 08:16:55 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 37b | 06/27/2016 | 08:17:12 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 37c | 06/27/2016 | 08:20:58 | Button Button | Reset Button pressed | Asserted
 37d | 06/27/2016 | 08:21:05 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 37e | 06/27/2016 | 08:21:05 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 37f | 06/27/2016 | 08:21:24 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 380 | 06/27/2016 | 08:21:38 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 381 | 08/08/2016 | 07:17:12 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 382 | 08/08/2016 | 07:17:07 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 383 | 08/08/2016 | 07:17:25 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 384 | 08/08/2016 | 07:17:42 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 385 | 09/12/2016 | 07:52:42 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 386 | 09/12/2016 | 07:52:42 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 387 | 09/12/2016 | 07:52:39 | Power Unit Pwr Unit Status | Power off/down | Asserted
 388 | 09/12/2016 | 07:53:18 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 389 | 09/12/2016 | 07:53:18 | Button Button | Power Button pressed | Asserted
 38a | 09/12/2016 | 07:53:27 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 38b | 09/12/2016 | 07:53:27 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 38c | 09/12/2016 | 07:53:47 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 38d | 09/12/2016 | 07:54:01 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 38e | 09/12/2016 | 14:04:42 | Power Unit Pwr Unit Status | Power off/down | Asserted
 38f | 09/12/2016 | 14:05:21 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 390 | 09/12/2016 | 14:05:21 | Button Button | Power Button pressed | Asserted
 391 | 09/12/2016 | 14:05:31 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 392 | 09/12/2016 | 14:05:31 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 393 | 09/12/2016 | 14:05:50 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 394 | 09/12/2016 | 14:06:04 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 395 | 09/12/2016 | 14:12:44 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 396 | 09/12/2016 | 14:12:44 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 397 | 09/12/2016 | 14:13:02 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 398 | 09/12/2016 | 14:13:19 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 399 | 09/13/2016 | 11:28:36 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 39a | 09/13/2016 | 11:28:36 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 39b | 09/13/2016 | 11:31:01 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 39c | 09/13/2016 | 11:31:01 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 39d | 09/13/2016 | 11:31:20 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 39e | 09/13/2016 | 11:31:34 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 39f | 09/13/2016 | 11:49:24 | Critical Interrupt FP NMI Diag Int | NMI/Diag Interrupt | Asserted
 3a0 | 09/13/2016 | 11:55:03 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3a1 | 09/13/2016 | 11:55:04 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3a2 | 09/13/2016 | 11:55:22 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 3a3 | 09/13/2016 | 11:55:39 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 3a4 | 09/13/2016 | 12:20:55 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3a5 | 09/13/2016 | 12:20:55 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3a6 | 09/13/2016 | 12:21:13 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 3a7 | 09/13/2016 | 12:21:30 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 3a8 | 09/13/2016 | 12:31:44 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3a9 | 09/13/2016 | 12:31:44 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3aa | 09/13/2016 | 12:31:45 | Power Unit Pwr Unit Status | Power off/down | Asserted
 3ab | 09/13/2016 | 12:32:32 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 3ac | 09/13/2016 | 12:32:32 | Button Button | Power Button pressed | Asserted
 3ad | 09/13/2016 | 12:32:41 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3ae | 09/13/2016 | 12:32:41 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3af | 09/13/2016 | 12:33:01 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 3b0 | 09/13/2016 | 12:33:15 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 3b1 | 09/13/2016 | 12:39:45 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3b2 | 09/13/2016 | 12:39:45 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3b3 | 09/13/2016 | 12:39:45 | Power Unit Pwr Unit Status | Power off/down | Asserted
 3b4 | 09/13/2016 | 12:40:47 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 3b5 | 09/13/2016 | 12:40:47 | Button Button | Power Button pressed | Asserted
 3b6 | 09/13/2016 | 12:40:56 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3b7 | 09/13/2016 | 12:40:56 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3b8 | 09/13/2016 | 12:41:16 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 3b9 | 09/13/2016 | 12:41:30 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 3ba | 09/13/2016 | 12:49:19 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3bb | 09/13/2016 | 12:49:19 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3bc | 09/13/2016 | 12:49:20 | Power Unit Pwr Unit Status | Power off/down | Asserted
 3bd | 09/13/2016 | 12:50:03 | Button Button | Power Button pressed | Asserted
 3be | 09/13/2016 | 12:50:04 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 3bf | 09/13/2016 | 12:50:13 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3c0 | 09/13/2016 | 12:50:13 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3c1 | 09/13/2016 | 12:50:32 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 3c2 | 09/13/2016 | 12:50:48 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 3c3 | 09/13/2016 | 13:22:49 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3c4 | 09/13/2016 | 13:22:49 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3c5 | 09/13/2016 | 13:22:50 | Power Unit Pwr Unit Status | Power off/down | Asserted
 3c6 | 09/13/2016 | 13:22:57 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 3c7 | 09/13/2016 | 13:22:57 | Button Button | Power Button pressed | Asserted
 3c8 | 09/13/2016 | 13:23:07 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3c9 | 09/13/2016 | 13:23:07 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3ca | 09/13/2016 | 13:23:26 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 3cb | 09/13/2016 | 13:23:39 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 3cc | 09/13/2016 | 13:26:13 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3cd | 09/13/2016 | 13:26:13 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3ce | 09/13/2016 | 13:26:32 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 3cf | 09/13/2016 | 13:26:49 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 3d0 | 09/13/2016 | 14:49:56 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3d1 | 09/13/2016 | 14:49:56 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3d2 | 09/13/2016 | 14:49:56 | Power Unit Pwr Unit Status | Power off/down | Asserted
 3d3 | 09/13/2016 | 14:50:28 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 3d4 | 09/13/2016 | 14:50:38 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3d5 | 09/13/2016 | 14:50:38 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3d6 | 09/13/2016 | 14:50:58 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 3d7 | 09/13/2016 | 14:51:12 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 3d8 | 09/20/2016 | 12:07:51 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3d9 | 09/20/2016 | 12:07:51 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3da | 09/20/2016 | 12:07:50 | Power Unit Pwr Unit Status | Power off/down | Asserted
 3db | 09/20/2016 | 12:28:56 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 3dc | 09/20/2016 | 12:29:06 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3dd | 09/20/2016 | 12:29:06 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3de | 09/20/2016 | 12:29:24 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 3df | 09/20/2016 | 12:29:39 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 3e0 | 09/22/2016 | 09:05:54 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3e1 | 09/22/2016 | 09:05:55 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3e2 | 09/22/2016 | 09:05:55 | Power Unit Pwr Unit Status | Power off/down | Asserted
 3e3 | 09/22/2016 | 09:06:33 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 3e4 | 09/22/2016 | 09:06:33 | Button Button | Power Button pressed | Asserted
 3e5 | 09/22/2016 | 09:06:42 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3e6 | 09/22/2016 | 09:06:42 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3e7 | 09/22/2016 | 09:08:24 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3e8 | 09/22/2016 | 09:08:25 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3e9 | 09/22/2016 | 09:08:43 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 3ea | 09/22/2016 | 09:08:58 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 3eb | 09/22/2016 | 09:12:47 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3ec | 09/22/2016 | 09:12:47 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3ed | 09/22/2016 | 09:12:48 | Power Unit Pwr Unit Status | Power off/down | Asserted
 3ee | 09/22/2016 | 09:14:20 | Button Button | Power Button pressed | Asserted
 3ef | 09/22/2016 | 09:14:21 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 3f0 | 09/22/2016 | 09:14:30 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3f1 | 09/22/2016 | 09:14:30 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3f2 | 09/22/2016 | 09:14:48 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 3f3 | 09/22/2016 | 09:15:14 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3f4 | 09/22/2016 | 09:15:14 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3f5 | 09/22/2016 | 09:16:13 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3f6 | 09/22/2016 | 09:16:14 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3f7 | 09/22/2016 | 09:16:32 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 3f8 | 09/22/2016 | 09:17:27 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3f9 | 09/22/2016 | 09:17:27 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3fa | 09/22/2016 | 09:17:46 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 3fb | 09/22/2016 | 09:18:52 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3fc | 09/22/2016 | 09:18:53 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3fd | 09/22/2016 | 09:19:11 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 3fe | 09/22/2016 | 09:19:51 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 3ff | 09/22/2016 | 09:19:51 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 400 | 09/22/2016 | 09:20:10 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 401 | 09/22/2016 | 09:21:17 | Power Unit Pwr Unit Status | Power off/down | Asserted
 402 | 09/22/2016 | 09:22:00 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 403 | 09/22/2016 | 09:22:09 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 404 | 09/22/2016 | 09:22:10 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 405 | 09/22/2016 | 09:23:06 | Power Unit Pwr Unit Status | Power off/down | Asserted
 406 | 09/22/2016 | 09:23:30 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 407 | 09/22/2016 | 09:23:40 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 408 | 09/22/2016 | 09:23:40 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 409 | 09/22/2016 | 09:24:33 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 40a | 09/22/2016 | 09:24:48 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 40b | 09/22/2016 | 10:20:29 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 40c | 09/22/2016 | 10:20:29 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 40d | 09/22/2016 | 10:20:48 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 40e | 09/22/2016 | 10:21:05 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 40f | 09/22/2016 | 10:23:44 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 410 | 09/22/2016 | 10:23:45 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 411 | 09/22/2016 | 10:25:18 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 412 | 09/22/2016 | 10:25:35 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 413 | 09/22/2016 | 10:39:10 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 414 | 09/22/2016 | 10:39:10 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 415 | 09/22/2016 | 10:39:58 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 416 | 09/22/2016 | 10:40:15 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 417 | 09/22/2016 | 11:05:10 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 418 | 09/22/2016 | 11:05:10 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 419 | 09/22/2016 | 11:05:29 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 41a | 09/22/2016 | 11:05:44 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 41b | 09/22/2016 | 11:37:20 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 41c | 09/22/2016 | 11:37:20 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 41d | 09/22/2016 | 11:37:38 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 41e | 09/22/2016 | 11:37:52 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 41f | 09/22/2016 | 11:41:39 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 420 | 09/22/2016 | 11:41:39 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 421 | 09/22/2016 | 11:41:57 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 422 | 09/22/2016 | 11:42:13 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 423 | 09/22/2016 | 12:54:45 | Power Unit Pwr Unit Status | Power off/down | Asserted
 424 | 09/22/2016 | 12:55:52 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 425 | 09/22/2016 | 12:56:02 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 426 | 09/22/2016 | 12:56:02 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 427 | 09/22/2016 | 12:56:21 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 428 | 09/22/2016 | 12:56:36 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 429 | 09/23/2016 | 13:49:15 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 42a | 09/23/2016 | 13:49:15 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 42b | 09/23/2016 | 13:50:57 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 42c | 09/23/2016 | 21:46:54 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 42d | 09/23/2016 | 21:47:12 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 42e | 09/23/2016 | 21:47:26 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 42f | 09/23/2016 | 21:55:40 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 430 | 09/23/2016 | 21:55:41 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 431 | 09/23/2016 | 21:55:59 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 432 | 09/23/2016 | 21:56:13 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 433 | 09/26/2016 | 21:31:35 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 434 | 09/26/2016 | 21:31:35 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 435 | 09/26/2016 | 21:31:53 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 436 | 09/26/2016 | 21:32:11 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 437 | 09/26/2016 | 21:33:18 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 438 | 09/26/2016 | 21:33:19 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 439 | 09/26/2016 | 21:33:37 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 43a | 09/26/2016 | 21:33:51 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 43b | 10/03/2016 | 17:36:01 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 43c | 10/03/2016 | 17:36:01 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 43d | 10/03/2016 | 17:36:17 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 43e | 10/03/2016 | 17:36:34 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 43f | 10/17/2016 | 14:56:42 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 440 | 10/17/2016 | 14:56:42 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 441 | 10/17/2016 | 14:57:00 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 442 | 10/17/2016 | 14:57:17 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 443 | 10/17/2016 | 18:47:50 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 444 | 10/17/2016 | 18:47:50 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 445 | 10/17/2016 | 18:47:51 | Power Unit Pwr Unit Status | Power off/down | Asserted
 446 | 10/17/2016 | 18:52:07 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 447 | 10/17/2016 | 18:52:16 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 448 | 10/17/2016 | 18:52:16 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 449 | 10/17/2016 | 18:52:33 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 44a | 10/17/2016 | 18:52:50 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 44b | 10/17/2016 | 18:53:57 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 44c | 10/17/2016 | 18:53:57 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 44d | 10/17/2016 | 18:53:58 | Power Unit Pwr Unit Status | Power off/down | Asserted
 44e | 10/17/2016 | 19:00:48 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 44f | 10/17/2016 | 19:00:58 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 450 | 10/17/2016 | 19:00:58 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 451 | 10/17/2016 | 19:01:15 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 452 | 10/17/2016 | 19:01:32 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 453 | 10/17/2016 | 19:13:02 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 454 | 10/17/2016 | 19:13:02 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 455 | 10/17/2016 | 19:14:04 | Power Unit Pwr Unit Status | Power off/down | Asserted
 456 | 10/17/2016 | 19:17:27 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 457 | 10/17/2016 | 19:17:36 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 458 | 10/17/2016 | 19:17:37 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 459 | 10/17/2016 | 19:17:54 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 45a | 10/17/2016 | 19:18:11 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 45b | 10/17/2016 | 19:23:32 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 45c | 10/17/2016 | 19:23:33 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 45d | 10/17/2016 | 19:24:16 | Power Unit Pwr Unit Status | Power off/down | Asserted
 45e | 10/17/2016 | 19:24:41 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 45f | 10/17/2016 | 19:24:50 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 460 | 10/17/2016 | 19:24:51 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 461 | 10/17/2016 | 19:25:08 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 462 | 10/17/2016 | 19:25:25 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 463 | 10/17/2016 | 19:32:20 | Power Unit Pwr Unit Status | Power off/down | Asserted
 464 | 10/17/2016 | 19:33:51 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 465 | 10/17/2016 | 19:34:00 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 466 | 10/17/2016 | 19:34:00 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 467 | 10/17/2016 | 19:34:07 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 468 | 10/17/2016 | 19:34:08 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 469 | 10/17/2016 | 19:35:44 | Power Unit Pwr Unit Status | Power off/down | Asserted
 46a | 10/17/2016 | 19:35:52 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 46b | 10/17/2016 | 19:36:01 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 46c | 10/17/2016 | 19:36:02 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 46d | 10/17/2016 | 19:36:19 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 46e | 10/17/2016 | 19:36:36 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 46f | 10/17/2016 | 19:48:08 | Power Unit Pwr Unit Status | Power off/down | Asserted
 470 | 10/17/2016 | 19:48:14 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 471 | 10/17/2016 | 19:48:24 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 472 | 10/17/2016 | 19:48:24 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 473 | 10/17/2016 | 19:48:41 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 474 | 10/17/2016 | 19:48:58 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 475 | 10/17/2016 | 19:52:45 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 476 | 10/17/2016 | 19:52:45 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 477 | 10/17/2016 | 19:53:49 | Power Unit Pwr Unit Status | Power off/down | Asserted
 478 | 10/17/2016 | 19:57:25 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 479 | 10/17/2016 | 19:57:34 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 47a | 10/17/2016 | 19:57:34 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 47b | 10/17/2016 | 19:57:51 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 47c | 10/17/2016 | 19:58:08 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 47d | 10/17/2016 | 20:06:59 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 47e | 10/17/2016 | 20:07:00 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 47f | 10/17/2016 | 20:10:45 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 480 | 10/17/2016 | 20:10:46 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 481 | 10/17/2016 | 20:11:40 | Power Unit Pwr Unit Status | Power off/down | Asserted
 482 | 10/17/2016 | 20:11:56 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 483 | 10/17/2016 | 20:12:05 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 484 | 10/17/2016 | 20:12:06 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 485 | 10/17/2016 | 20:12:23 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 486 | 10/17/2016 | 20:12:40 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 487 | 10/17/2016 | 20:19:16 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 488 | 10/17/2016 | 20:19:16 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 489 | 10/17/2016 | 20:19:54 | Power Unit Pwr Unit Status | Power off/down | Asserted
 48a | 10/17/2016 | 20:24:25 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 48b | 10/17/2016 | 20:24:34 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 48c | 10/17/2016 | 20:24:35 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 48d | 10/17/2016 | 20:24:52 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 48e | 10/17/2016 | 20:25:09 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 48f | 10/17/2016 | 20:27:08 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 490 | 10/17/2016 | 20:27:08 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 491 | 10/17/2016 | 20:27:51 | Power Unit Pwr Unit Status | Power off/down | Asserted
 492 | 10/17/2016 | 20:30:20 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 493 | 10/17/2016 | 20:30:30 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 494 | 10/17/2016 | 20:30:30 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 495 | 10/17/2016 | 20:30:47 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 496 | 10/17/2016 | 20:31:04 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 497 | 10/17/2016 | 21:56:58 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 498 | 10/17/2016 | 21:56:58 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 499 | 10/17/2016 | 21:57:51 | Power Unit Pwr Unit Status | Power off/down | Asserted
 49a | 10/17/2016 | 21:58:12 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 49b | 10/17/2016 | 21:58:21 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 49c | 10/17/2016 | 21:58:22 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 49d | 10/17/2016 | 21:58:39 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 49e | 10/17/2016 | 21:58:56 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 49f | 10/17/2016 | 22:11:14 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4a0 | 10/17/2016 | 22:11:15 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4a1 | 10/17/2016 | 22:12:07 | Power Unit Pwr Unit Status | Power off/down | Asserted
 4a2 | 10/17/2016 | 22:12:28 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 4a3 | 10/17/2016 | 22:12:37 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4a4 | 10/17/2016 | 22:12:37 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4a5 | 10/17/2016 | 22:12:54 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 4a6 | 10/17/2016 | 22:13:11 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 4a7 | 10/20/2016 | 14:52:27 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4a8 | 10/20/2016 | 14:52:28 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4a9 | 10/20/2016 | 14:53:20 | Power Unit Pwr Unit Status | Power off/down | Asserted
 4aa | 10/20/2016 | 14:53:49 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 4ab | 10/20/2016 | 14:53:58 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4ac | 10/20/2016 | 14:53:59 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4ad | 10/20/2016 | 14:54:16 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 4ae | 10/20/2016 | 14:54:33 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 4af | 11/04/2016 | 18:03:42 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4b0 | 11/04/2016 | 18:03:42 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4b1 | 11/04/2016 | 18:03:58 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 4b2 | 11/04/2016 | 18:04:15 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 4b3 | 11/04/2016 | 19:02:41 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4b4 | 11/04/2016 | 19:02:42 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4b5 | 11/04/2016 | 19:02:59 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 4b6 | 11/04/2016 | 19:03:16 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 4b7 | 11/07/2016 | 20:33:19 | Power Unit Pwr Unit Status | Power off/down | Asserted
 4b8 | 11/07/2016 | 20:41:11 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 4b9 | 11/07/2016 | 20:41:20 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4ba | 11/07/2016 | 20:41:20 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4bb | 11/07/2016 | 20:41:37 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 4bc | 11/07/2016 | 20:41:54 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 4bd | 11/07/2016 | 20:57:24 | Power Unit Pwr Unit Status | Power off/down | Asserted
 4be | 11/07/2016 | 20:57:30 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 4bf | 11/07/2016 | 20:57:40 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4c0 | 11/07/2016 | 20:57:41 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4c1 | 11/07/2016 | 20:57:58 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 4c2 | 11/07/2016 | 20:58:15 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 4c3 | 11/07/2016 | 21:01:34 | Power Unit Pwr Unit Status | Power off/down | Asserted
 4c4 | 11/07/2016 | 21:01:40 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 4c5 | 11/07/2016 | 21:01:50 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4c6 | 11/07/2016 | 21:01:50 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4c7 | 11/07/2016 | 21:02:07 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 4c8 | 11/07/2016 | 21:02:24 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 4c9 | 11/07/2016 | 21:12:25 | Power Unit Pwr Unit Status | Power off/down | Asserted
 4ca | 11/07/2016 | 21:12:32 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 4cb | 11/07/2016 | 21:12:41 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4cc | 11/07/2016 | 21:12:41 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4cd | 11/07/2016 | 21:12:59 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 4ce | 11/07/2016 | 21:13:16 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 4cf | 11/07/2016 | 21:14:59 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4d0 | 11/07/2016 | 21:15:00 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4d1 | 11/07/2016 | 21:15:17 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 4d2 | 11/07/2016 | 21:15:34 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 4d3 | 11/07/2016 | 21:17:49 | Power Unit Pwr Unit Status | Power off/down | Asserted
 4d4 | 11/07/2016 | 21:17:55 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 4d5 | 11/07/2016 | 21:18:05 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4d6 | 11/07/2016 | 21:18:05 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4d7 | 11/07/2016 | 21:18:22 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 4d8 | 11/07/2016 | 21:18:39 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 4d9 | 11/07/2016 | 23:28:18 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4da | 11/07/2016 | 23:28:19 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4db | 11/07/2016 | 23:29:16 | Power Unit Pwr Unit Status | Power off/down | Asserted
 4dc | 11/07/2016 | 23:29:22 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 4dd | 11/07/2016 | 23:29:32 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4de | 11/07/2016 | 23:29:32 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4df | 11/07/2016 | 23:29:49 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 4e0 | 11/07/2016 | 23:30:06 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 4e1 | 11/07/2016 | 23:37:21 | Power Unit Pwr Unit Status | Power off/down | Asserted
 4e2 | 11/07/2016 | 23:37:27 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 4e3 | 11/07/2016 | 23:37:37 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4e4 | 11/07/2016 | 23:37:38 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4e5 | 11/07/2016 | 23:37:55 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 4e6 | 11/07/2016 | 23:38:12 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 4e7 | 11/08/2016 | 15:24:49 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4e8 | 11/08/2016 | 15:24:49 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4e9 | 11/08/2016 | 15:26:05 | Power Unit Pwr Unit Status | Power off/down | Asserted
 4ea | 11/08/2016 | 15:26:12 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 4eb | 11/08/2016 | 15:26:21 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4ec | 11/08/2016 | 15:26:21 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4ed | 11/08/2016 | 15:26:39 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 4ee | 11/08/2016 | 15:26:56 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 4ef | 11/08/2016 | 18:07:15 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4f0 | 11/08/2016 | 18:07:15 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4f1 | 11/08/2016 | 18:07:15 | Power Unit Pwr Unit Status | Power off/down | Asserted
 4f2 | 11/08/2016 | 18:08:42 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 4f3 | 11/08/2016 | 18:08:51 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4f4 | 11/08/2016 | 18:08:51 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4f5 | 11/08/2016 | 18:09:09 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 4f6 | 11/08/2016 | 18:09:26 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 4f7 | 11/08/2016 | 20:34:56 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4f8 | 11/08/2016 | 20:34:56 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4f9 | 11/08/2016 | 20:36:01 | Power Unit Pwr Unit Status | Power off/down | Asserted
 4fa | 11/08/2016 | 20:36:07 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 4fb | 11/08/2016 | 20:36:16 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4fc | 11/08/2016 | 20:36:16 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 4fd | 11/08/2016 | 20:36:34 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 4fe | 11/08/2016 | 20:36:51 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 4ff | 11/10/2016 | 19:16:29 | Power Unit Pwr Unit Status | Power off/down | Asserted
 500 | 11/10/2016 | 19:16:35 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 501 | 11/10/2016 | 19:16:44 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 502 | 11/10/2016 | 19:16:44 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 503 | 11/10/2016 | 19:17:01 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 504 | 11/10/2016 | 19:17:18 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 505 | 11/10/2016 | 19:19:39 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 506 | 11/10/2016 | 19:19:39 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 507 | 11/10/2016 | 19:20:42 | Power Unit Pwr Unit Status | Power off/down | Asserted
 508 | 11/10/2016 | 19:20:48 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 509 | 11/10/2016 | 19:20:57 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 50a | 11/10/2016 | 19:20:57 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 50b | 11/10/2016 | 19:21:14 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 50c | 11/10/2016 | 19:21:31 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 50d | 11/11/2016 | 17:37:00 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 50e | 11/11/2016 | 17:37:00 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 50f | 11/11/2016 | 17:37:43 | Power Unit Pwr Unit Status | Power off/down | Asserted
 510 | 11/11/2016 | 17:37:49 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 511 | 11/11/2016 | 17:37:58 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 512 | 11/11/2016 | 17:37:59 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 513 | 11/11/2016 | 17:38:16 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 514 | 11/11/2016 | 17:38:33 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 515 | 11/11/2016 | 18:26:10 | Power Unit Pwr Unit Status | Power off/down | Asserted
 516 | 11/11/2016 | 18:26:16 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 517 | 11/11/2016 | 18:26:26 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 518 | 11/11/2016 | 18:26:26 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 519 | 11/11/2016 | 18:26:43 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 51a | 11/11/2016 | 18:27:00 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 51b | 12/01/2016 | 16:54:54 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 51c | 12/01/2016 | 16:54:53 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 51d | 12/01/2016 | 16:55:10 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 51e | 12/01/2016 | 16:55:27 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 51f | 12/08/2016 | 15:23:04 | Management Subsystem Health BMC Watchdog | State Asserted | Asserted
 520 | 12/09/2016 | 15:23:00 | Physical Security Physical Scrty | System unplugged from LAN | Asserted
 521 | 12/09/2016 | 15:34:30 | Physical Security Physical Scrty | System unplugged from LAN | Deasserted
 522 | 12/09/2016 | 16:48:28 | Management Subsystem Health BMC Watchdog | State Asserted | Asserted
 523 | 01/12/2017 | 16:38:21 | Management Subsystem Health BMC Watchdog | State Asserted | Asserted
 524 | 01/12/2017 | 16:39:34 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 525 | 01/12/2017 | 16:39:35 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 526 | 01/12/2017 | 16:39:35 | Power Unit Pwr Unit Status | Power off/down | Asserted
 527 | 01/12/2017 | 16:42:35 | Management Subsystem Health BMC Watchdog | State Asserted | Asserted
 528 | 01/12/2017 | 16:42:35 | Power Unit Pwr Unit Status | Power off/down | Asserted
 529 | 01/12/2017 | 16:44:59 | Management Subsystem Health BMC Watchdog | State Asserted | Asserted
 52a | 01/12/2017 | 16:45:00 | Power Unit Pwr Unit Status | Power off/down | Asserted
 52b | 01/12/2017 | 16:51:47 | Power Supply PS1 Status | Power Supply AC lost | Asserted
 52c | 03/23/2017 | 15:50:15 | Power Unit Pwr Unit Status | Power off/down | Asserted
 52d | 03/23/2017 | 15:53:33 | Power Unit Pwr Unit Status | Power off/down | Deasserted
 52e | 03/23/2017 | 15:53:33 | Button Button | Power Button pressed | Asserted
 52f | 03/23/2017 | 15:53:34 | Button Button | Reset Button pressed | Asserted
 530 | 03/23/2017 | 15:53:43 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 531 | 03/23/2017 | 15:53:43 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 532 | 03/23/2017 | 15:54:12 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 533 | 03/23/2017 | 15:54:33 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 534 | 03/23/2017 | 15:54:33 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 535 | 03/23/2017 | 15:56:01 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 536 | 03/23/2017 | 15:56:01 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 537 | 03/23/2017 | 15:56:37 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 538 | 03/23/2017 | 15:57:05 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 539 | 03/23/2017 | 16:25:10 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 53a | 03/23/2017 | 16:25:11 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 53b | 03/23/2017 | 16:25:29 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 53c | 03/23/2017 | 16:25:47 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 53d | 03/23/2017 | 16:25:47 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 53e | 03/23/2017 | 16:28:23 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 53f | 03/23/2017 | 16:28:39 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 540 | 03/23/2017 | 16:51:21 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 541 | 03/23/2017 | 16:51:21 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 542 | 03/23/2017 | 16:51:38 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 543 | 03/23/2017 | 16:51:55 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 544 | 03/23/2017 | 16:52:06 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 545 | 03/23/2017 | 16:52:06 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 546 | 03/23/2017 | 16:53:03 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 547 | 03/23/2017 | 16:53:03 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 548 | 03/23/2017 | 16:53:20 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 549 | 03/23/2017 | 16:53:36 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 54a | 03/23/2017 | 16:57:19 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 54b | 03/23/2017 | 16:57:20 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 54c | 03/23/2017 | 16:58:05 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 54d | 03/23/2017 | 16:58:05 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 54e | 03/23/2017 | 16:58:23 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 54f | 03/23/2017 | 16:58:36 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 550 | 03/23/2017 | 18:03:55 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 551 | 03/23/2017 | 18:03:56 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 552 | 03/23/2017 | 18:04:14 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 553 | 03/23/2017 | 18:04:39 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 554 | 03/30/2017 | 19:47:20 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 555 | 03/30/2017 | 19:47:20 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 556 | 03/30/2017 | 19:47:37 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 557 | 03/30/2017 | 19:47:54 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 558 | 03/30/2017 | 21:39:40 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 559 | 03/30/2017 | 21:39:41 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 55a | 03/30/2017 | 21:39:58 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 55b | 03/30/2017 | 21:40:15 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 55c | 04/04/2017 | 14:44:04 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 55d | 04/04/2017 | 14:44:04 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 55e | 04/04/2017 | 14:44:21 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 55f | 04/04/2017 | 14:44:38 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 560 | 04/13/2017 | 18:52:09 | Management Subsystem Health BMC Watchdog | State Asserted | Asserted
 561 | 04/21/2017 | 18:03:28 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 562 | 04/21/2017 | 18:03:28 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 563 | 04/21/2017 | 18:03:46 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 564 | 04/21/2017 | 18:04:02 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 565 | 04/21/2017 | 18:07:27 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 566 | 04/21/2017 | 18:07:27 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 567 | 04/21/2017 | 18:07:45 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 568 | 04/21/2017 | 18:08:02 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 569 | 04/21/2017 | 18:16:07 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 56a | 04/21/2017 | 18:16:07 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 56b | 04/21/2017 | 18:16:25 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 56c | 04/21/2017 | 18:16:41 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 56d | 04/21/2017 | 18:21:09 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 56e | 04/21/2017 | 18:21:10 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 56f | 04/21/2017 | 18:21:27 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 570 | 04/21/2017 | 18:21:43 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 571 | 04/21/2017 | 18:23:14 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 572 | 04/21/2017 | 18:23:15 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 573 | 04/21/2017 | 18:23:33 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 574 | 04/21/2017 | 18:23:49 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 575 | 04/27/2017 | 20:18:32 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 576 | 04/27/2017 | 20:18:32 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 577 | 04/27/2017 | 20:18:50 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 578 | 04/27/2017 | 20:19:06 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 579 | 05/26/2017 | 03:38:01 | Management Subsystem Health BMC Watchdog | State Asserted | Asserted
 57a | 06/15/2017 | 20:26:25 | Management Subsystem Health BMC Watchdog | State Asserted | Asserted
 57b | 06/15/2017 | 20:30:41 | Management Subsystem Health BMC Watchdog | State Asserted | Asserted
 57c | 06/29/2017 | 22:26:05 | Management Subsystem Health BMC Watchdog | State Asserted | Asserted
 57d | 07/06/2017 | 20:57:29 | Management Subsystem Health BMC Watchdog | State Asserted | Asserted
 57e | 07/13/2017 | 21:18:22 | Management Subsystem Health BMC Watchdog | State Asserted | Asserted
 57f | 07/13/2017 | 21:20:46 | Management Subsystem Health BMC Watchdog | State Asserted | Asserted
 580 | 08/25/2017 | 17:21:06 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 581 | 08/25/2017 | 17:21:06 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 582 | 08/25/2017 | 17:21:35 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 583 | 08/25/2017 | 17:21:54 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 584 | 08/25/2017 | 17:21:54 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 585 | 08/25/2017 | 17:23:01 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 586 | 08/25/2017 | 17:23:02 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 587 | 08/25/2017 | 17:23:33 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 588 | 08/25/2017 | 17:34:30 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 589 | 08/25/2017 | 17:34:30 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 58a | 08/25/2017 | 17:34:57 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 58b | 08/25/2017 | 17:35:32 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 58c | 08/25/2017 | 17:56:15 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 58d | 08/25/2017 | 17:56:15 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 58e | 08/25/2017 | 17:56:42 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 58f | 08/25/2017 | 17:57:13 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 590 | 08/25/2017 | 17:57:37 | OS Boot | Installation started | Asserted
 591 | 08/25/2017 | 20:02:40 | OS Boot | Installation completed | Asserted
 592 | 08/25/2017 | 20:03:43 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 593 | 08/25/2017 | 20:03:43 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 594 | 08/25/2017 | 19:57:01 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 595 | 08/25/2017 | 19:57:30 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 596 | 08/25/2017 | 19:57:30 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 597 | 08/25/2017 | 19:58:19 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 598 | 08/25/2017 | 19:58:19 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 599 | 08/25/2017 | 19:58:38 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 59a | 08/25/2017 | 19:59:06 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 59b | 08/25/2017 | 20:17:16 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 59c | 08/25/2017 | 20:17:16 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 59d | 08/25/2017 | 20:17:34 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 59e | 08/25/2017 | 20:17:49 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 59f | 08/25/2017 | 20:31:36 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 5a0 | 08/25/2017 | 20:31:37 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 5a1 | 08/25/2017 | 20:31:54 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 5a2 | 08/25/2017 | 20:32:10 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 5a3 | 08/25/2017 | 20:35:19 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 5a4 | 08/25/2017 | 20:35:19 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 5a5 | 08/25/2017 | 20:35:37 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 5a6 | 08/25/2017 | 20:35:53 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 5a7 | 08/25/2017 | 21:14:17 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 5a8 | 08/25/2017 | 21:14:17 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 5a9 | 08/25/2017 | 21:14:34 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 5aa | 08/25/2017 | 21:14:50 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 5ab | 09/08/2017 | 21:09:15 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 5ac | 09/08/2017 | 21:09:15 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 5ad | 09/08/2017 | 21:14:39 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 5ae | 09/08/2017 | 21:14:40 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 5af | 09/08/2017 | 21:14:57 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 5b0 | 09/08/2017 | 21:15:13 | Critical Interrupt PCIe Cor Sensor |  | Asserted
 5b1 | 09/11/2017 | 15:00:08 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 5b2 | 09/11/2017 | 15:00:08 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 5b3 | 09/11/2017 | 15:01:52 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 5b4 | 09/11/2017 | 15:01:53 | System Event BIOS Evt Sensor | Timestamp Clock Sync | Asserted
 5b5 | 09/11/2017 | 15:02:10 | System Event BIOS Evt Sensor | OEM System boot event | Asserted
 5b6 | 09/11/2017 | 15:02:26 | Critical Interrupt PCIe Cor Sensor |  | Asserted
"""
