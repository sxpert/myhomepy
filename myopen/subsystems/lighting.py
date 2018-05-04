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

    def parse_command(self, msg):
        # light command
        # '*0*#1##'
        m = re.match('^\*(?P<command>[01])\*(?P<light>\d{2,4})##$', msg)
        if m is not None:
            data = m.groupdict()
            self.log(str(data))
            device = {'light': data['light']}

            self.execute_callback(self.SYSTEM_WHO,
                                  int(data['command']),
                                  device, None)
            return
        m = re.match('^\*(?P<command>[01])\*#(?P<group>\d{1,3})##$', msg)
        if m is not None:
            data = m.groupdict()
            self.log(str(data))
            device = {'group': data['group']}
            self.execute_callback(self.SYSTEM_WHO,
                                  int(data['command']),
                                  device, None)
            return
        self.log('lighting command '+msg)

    def map_device(self, device):
        if (type(device) is dict) and ('group' in device.keys()):
            return 'G-'+str(device['group'])
        return None

    # command generators

    def gen_command(self, operation, target):
        self.log("%s %s" % (str(operation), str(target)))
        if operation in [self.OP_LIGHTING_OFF, self.OP_LIGHTING_ON]:
            if 'light' in target.keys():
                destination = target['light']
                return '*1*%s*%s##' % (str(operation), destination)
        return None
