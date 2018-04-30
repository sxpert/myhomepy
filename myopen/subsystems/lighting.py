# -*- coding: utf-8 -*-
import re

from .parser import OWNParser


class Lighting(OWNParser):
    SYSTEM_NAME = "LIGHTING"
    SYSTEM_WHO = 1

    OP_LIGHTING_OFF = 0
    OP_LIGHTING_ON = 1

    SYSTEM_CALLBACKS = {
        'OFF': OP_LIGHTING_OFF,
        'ON': OP_LIGHTING_ON
    }

    def parse_command(self, msg):
        # light command
        # '*0*#1##'
        m = re.match('^\*(?P<command>[01])\*(?P<light>\d{2,4})##$', msg)
        if m is not None:
            data = m.groupdict()
            self.log(str(data))
            device = {'light': data['light']}
            self.execute_callback(self.SYSTEM_WHO,
                                  data['command'],
                                  device, None)
            return
        m = re.match('^\*(?P<command>[01])\*#(?P<group>\d{1,3})##$', msg)
        if m is not None:
            data = m.groupdict()
            self.log(str(data))
            device = {'group': data['group']}
            self.execute_callback(self.SYSTEM_WHO,
                                  data['command'],
                                  device, None)
            return
        self.log('lighting command '+msg)

    def map_device(self, device):
        if (type(device) is dict) and ('group' in device.keys()):
            return 'G-'+str(device['group'])
        return None
