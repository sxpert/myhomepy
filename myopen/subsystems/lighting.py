# -*- coding: utf-8 -*-
import re

from myopen.device_db import device_db
from .subsystem import OWNSubSystem


class Lighting(OWNSubSystem):
    SYSTEM_NAME = 'LIGHTING'
    SYSTEM_WHO = 1

    OP_CMD_LIGHT_OFF = 0
    OP_CMD_LIGHT_ON = 1
    OP_CMD_GROUP_OFF = 2
    OP_CMD_GROUP_ON = 3

    SYSTEM_CALLBACKS = {
        'CMD_LIGHT_OFF': OP_CMD_LIGHT_OFF,
        'CMD_LIGHT_ON': OP_CMD_LIGHT_ON,
        'CMD_GROUP_OFF': OP_CMD_GROUP_OFF,
        'CMD_GROUP_ON': OP_CMD_GROUP_ON
    }

    TARGET_GENERAL = {'light': '0'}

    SYSTEM_REGEXPS = {
        'COMMAND': [
            {
                'name': 'CMD_LIGHT_OFF',
                're': r'^\*0\*(?P<light>\d{2,4})##$',
                'func': 'cmd_light_off'
            },
            {
                'name': 'CMD_LIGHT_ON',
                're': r'^\*1\*(?P<light>\d{2,4})##$',
                'func': 'cmd_light_on'
            },
            {
                'name': 'CMD_GROUP_OFF',
                're': r'^\*0\*#(?P<group>\d{1,3})##$',
                'func': 'cmd_group_off'
            },
            {
                'name': 'CMD_GROUP_On',
                're': r'^\*1\*#(?P<group>\d{1,3})##$',
                'func': 'cmd_group_on'
            },
        ]
    }

    def _cmd_light(self, order, matches):
        info = {
            'data': matches,
            'order': order,
            'device': matches,
            'func': None
        }
        return info

    def cmd_light_off(self, matches):
        return self._cmd_light(self.OP_CMD_LIGHT_OFF, matches)

    def cmd_light_on(self, matches):
        return self._cmd_light(self.OP_CMD_LIGHT_ON, matches)

    def cmd_group_off(self, matches):
        return self._cmd_light(self.OP_CMD_GROUP_OFF, matches)

    def cmd_group_on(self, matches):
        return self._cmd_light(self.OP_CMD_GROUP_ON, matches)

    def map_device(self, device):
        if isinstance(device, dict):
            light = device.get('light', None)
            group = device.get('group', None)
            if light is not None:
                ok, addr = device_db.parse_ADDRESS_long(light)
                if ok:
                    self.log('found %s' % (str(addr)))
                    a = addr.get('a', None)
                    pl = addr.get('pl', None)
                    if a is not None and pl is not None:
                        return '%d-%d' % (a, pl)
                    else:
                        self.log('Error in address, we need \'a\' and \'pl\' values, parsed \'%s\' => %s' % (light, str(addr))) 
                else:
                    self.log('Error while parsing light \'%s\'' % (light))
            elif group is not None:
                return 'G-' + group
        return None

    def gen_command(self, operation, target):
        self.log("%s %s" % (str(operation), str(target)))
        if operation in [self.OP_CMD_LIGHT_OFF, self.OP_CMD_LIGHT_ON]:
            if 'light' in target.keys():
                destination = target['light']
                return '*1*%s*%s##' % (str(operation), destination)
        return None
