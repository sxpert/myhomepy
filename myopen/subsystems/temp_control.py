# -*- coding: utf-8 -*-
import json
import re

from .subsystem import OWNSubSystem


class TempControl(OWNSubSystem):
    SYSTEM_NAME = 'TEMP_CONTROL'
    SYSTEM_WHO = 4

    OP_RES_TEMP_REPORT = 0

    SYSTEM_CALLBACKS = {
        'RES_TEMP_REPORT': OP_RES_TEMP_REPORT,
    }

    SYSTEM_REGEXPS = {
        'STATUS': [
            {
                'name': 'RES_TEMP_REPORT',
                're': r'^\*(?P<probe>\d{3})\*0\*(?P<temperature>\d{4})##$',
                'func': 'res_temp_report'
            }
        ]
    }

    def res_temp_report(self, matches):
        _zone = int(matches['probe'][1:])
        _sensor = int(matches['probe'][0])
        _temp = float(matches['temperature'])/10.0

        _order = self.OP_RES_TEMP_REPORT 
        _device = {'zone': _zone, 'sensor': _sensor}
        _data = {'temp': _temp, 'unit': '°C'}
        return self.gen_callback_dict(_order, _device, _data)

    def map_device(self, device):
        if (type(device) is dict) and \
           ('zone' in device.keys()) and \
           ('sensor' in device.keys()):
            return '['+str(device['zone'])+'-'+str(device['sensor'])+']'
        return None
