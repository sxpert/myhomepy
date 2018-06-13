# -*- coding: utf-8 -*-
import re

from .subsystem import OWNSubSystem

class CenPlusDryContacts(OWNSubSystem):
    SYSTEM_NAME = 'CEN_PLUS_DRY_CONTACTS'
    SYSTEM_WHO = 25

    OP_CEN_PLUS_SHORT_PRESSURE = 21
    OP_CEN_PLUS_START_PRESSURE = 22
    OP_CEN_PLUS_PRESSURE =       23
    OP_CEN_PLUS_END_PRESSURE =   24

    SYSTEM_CALLBACKS = {
        'CEN_PLUS_SHORT_PRESSURE': OP_CEN_PLUS_SHORT_PRESSURE,
        'CEN_PLUS_START_PRESSURE': OP_CEN_PLUS_SHORT_PRESSURE,
        'CEN_PLUS_PRESSURE':       OP_CEN_PLUS_SHORT_PRESSURE,
        'CEN_PLUS_END_PRESSURE':   OP_CEN_PLUS_SHORT_PRESSURE,
    }

    SYSTEM_REGEXPS = {
        'COMMAND': [
            {
                'name': 'CEN_PLUS_SHORT_PRESSURE',
                're': r'^\*21#(?P<button>\d{1,2})\*2(?P<cen_command>\d{1,4})##$',
                'func': 'cen_plus_short_pressure'
            },
            {
                'name': 'CEN_PLUS_START_PRESSURE',
                're': r'^\*22#(?P<button>\d{1,2})\*2(?P<cen_command>\d{1,4})##$',
                'func': 'cen_plus_start_pressure'
            },
            {
                'name': 'CEN_PLUS_PRESSURE',
                're': r'^\*23#(?P<button>\d{1,2})\*2(?P<cen_command>\d{1,4})##$',
                'func': 'cen_plus_pressure'
            },
            {
                'name': 'CEN_PLUS_END_PRESSURE',
                're': r'^\*24#(?P<button>\d{1,2})\*2(?P<cen_command>\d{1,4})##$',
                'func': 'cen_plus_end_pressure'
            },
        ],
        'STATUS': [

        ]
    }

    def map_device(self, device):
        command = device.get('command', None)
        button = device.get('button', None)
        if command is not None and button is not None:
            return '%d-%d' % (command, button)

    def cen_plus_short_pressure(self, matches):
        command = int(matches.get('cen_command', 1))
        button = int(matches.get('button', 0))
        info = {
            'data': matches,
            'device': {'command': command, 'button': button},
            'order': self.OP_CEN_PLUS_SHORT_PRESSURE,
            'func': None
        }
        return info

    def cen_plus_start_pressure(self, matches):
        command = int(matches.get('cen_command', 1))
        button = int(matches.get('button', 0))
        info = {
            'data': matches,
            'device': {'command': command, 'button': button},
            'order': self.OP_CEN_PLUS_START_PRESSURE,
            'func': None
        }
        return info

    def cen_plus_pressure(self, matches):
        command = int(matches.get('cen_command', 1))
        button = int(matches.get('button', 0))
        info = {
            'data': matches,
            'device': {'command': command, 'button': button},
            'order': self.OP_CEN_PLUS_PRESSURE,
            'func': None
        }
        return info

    def cen_plus_end_pressure(self, matches):
        command = int(matches.get('cen_command', 1))
        button = int(matches.get('button', 0))
        info = {
            'data': matches,
            'device': {'command': command, 'button': button},
            'order': self.OP_CEN_PLUS_END_PRESSURE,
            'func': None
        }
        return info

