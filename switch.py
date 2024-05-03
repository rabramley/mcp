#!/usr/bin/env python3

import sys
import logging
import subprocess
import monitorcontrol
from dataclasses import dataclass

@dataclass
class Device:
    b: str
    c: str
    d: str
    vidpid: str = '046D:C548'
    a: str = '0x10'
    channel: str = '0x00'
    f: str = '0x00'
    g: str = '0x00'


hidapitester: str = ''
vidpid : str = '046D:C548'
hdmi_port : str = ''

devices = [
    Device(b='0x01', c='0x09', d='0x1e'),
    Device(b='0x02', c='0x0a', d='0x1b'),
]

if sys.platform.startswith('linux'):
    hidapitester = 'hidapitester'
    hdmi_port = 'HDMI1'

    for d in devices:
        d.channel = '0x01'

elif sys.platform.startswith('win32'):
    hidapitester = 'hidapitester.exe'
    hdmi_port = 'HDMI2'

    for d in devices:
        d.channel = '0x00'

else:
    logging.error(f"Yes, I don't know what to do for {sys.platform}")
    exit()

for d in devices:
    params = f'{d.a},{d.b},{d.c},{d.d},{d.channel},{d.f},{d.g}'
    mess = f'{hidapitester} --vidpid {vidpid} --usage 0x0001 --usagePage 0xFF00 --open --length 7 --send-output {params}'
    result = subprocess.run(mess, shell=True, capture_output=True, text=True)

for monitor in monitorcontrol.monitorcontrol.get_monitors():
    with monitor:
        monitor.set_input_source(hdmi_port)
