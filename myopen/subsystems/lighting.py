# -*- coding: utf-8 -*-
import re

from .subsystem import OWNSubSystem


class Lighting(OWNSubSystem):
    SYSTEM_NAME = "LIGHTING"
    SYSTEM_WHO = 1

    OP_LIGHTING_OFF = 0
    OP_LIGHTING_ON = 1

    SYSTEM_CALLBACKS = {
        'OFF': OP_LIGHTING_OFF,
        'ON': OP_LIGHTING_ON
    }

    TARGET_GENERAL = {'light': '0'}

    SYSTEM_REGEXPS = {
        'Command': [
            (r'^\*(?P<command>[01])\*(?P<light>\d{2,4})##$', '_light_device', ),
            (r'^\*(?P<command>[01])\*#(?P<group>\\d{1,3})##$', '_group_device', ),
        ]
    }

    def _light_device(self, matches):
        # light command
        # '*0*#1##'
        # TODO: something smarter here
        _order = int(matches['command'])
        _device = {'light': matches['light']}
        return self.gen_callback_dict(_order, _device, None)
        
    def _group_device(self, matches):
        _order = int(matches['command'])
        _device = {'group': matches['group']}
        return self.gen_callback_dict(_order, _device, None)

    def map_device(self, device):
        if (type(device) is dict) and ('group' in device.keys()):
            return 'G-'+str(device['group'])
        return None

    def gen_command(self, operation, target):
        self.log("%s %s" % (str(operation), str(target)))
        if operation in [self.OP_LIGHTING_OFF, self.OP_LIGHTING_ON]:
            if 'light' in target.keys():
                destination = target['light']
                return '*1*%s*%s##' % (str(operation), destination)
        return None
