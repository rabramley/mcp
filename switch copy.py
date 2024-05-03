#!/usr/bin/env python3

import sys
import logging
import subprocess
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
a = 0x10
b_keyboard = 0x01
b_mouse = 0x01
c_keyboard = 0x09
c_mouse = 0x0a
d_keyboard = 0x1e
d_mouse = 0x1b
e_channel: str = ''
f: str = 0x00
g: str = 0x00

devices = [
    Device(b='0x01', c='0x09', d='0x1e'),
    Device(b='0x02', c='0x0a', d='0x1b'),
]


if sys.platform.startswith('linux'):
    hidapitester = 'hidapitester'

    for d in devices:
        d.channel = '0x01'

elif sys.platform.startswith('win32'):
    hidapitester = 'hidapitester.exe'

    for d in devices:
        d.channel = '0x00'

else:
    logging.error(f"Yes, I don't know what to do for {sys.platform}")
    exit()

for d in devices:
    result = subprocess.run([
        hidapitester,
        '--vidpid',
        vidpid,
        '--usage',
        0x0001,
        '--usagePage',
        0xFF00,
        '--open',
        '--length',
        '7',
        '--send-output',
        d.a,
        d.b,
        d.c,
        d.d,
        d.channel,
        d.f,
        d.g,
        ], shell=True, capture_output=True, text=True)

    print(result.stdout)
