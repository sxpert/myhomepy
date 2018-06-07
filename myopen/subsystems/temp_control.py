# -*- coding: utf-8 -*-
import json
import re

from .subsystem import OWNSubSystem


class TempControl(OWNSubSystem):
    SYSTEM_NAME = 'TEMP_CONTROL'
    SYSTEM_WHO = 4

    OP_REPORT_TEMP = 0

    SYSTEM_CALLBACKS = {
        'REPORT_TEMP': OP_REPORT_TEMP,
    }

    SYSTEM_REGEXPS = {
        'STATUS': [
            (r'^\*(?P<probe>\d{3})\*0\*(?P<temperature>\d{4})##$',
             '_report_temperature')
        ]
    }

    def parse_address_slave(self, address):
        self.log('address: \'%s\' %d' % (address, len(address)))
        if len(address) != 3:
            self.log("ERROR, slave address for temperature probes are 3 chars long")
            zone = int(address[1])
            slave = int(address[2:3])
            addr = {
                "zone": zone,
                "slave": slave
            }
            return addr

    def _report_temperature(self, matches):
        _zone = int(matches['probe'][0])
        _sensor = int(matches['probe'][1:])
        _temp = float(matches['temperature'])/10.0

        _order = self.OP_REPORT_TEMP
        _device = {'zone': _zone, 'sensor': _sensor}
        _data = {'temp': _temp, 'unit': '°C'}
        return self.gen_callback_dict(_order, _device, _data)

    def map_device(self, device):
        if (type(device) is dict) and \
           ('zone' in device.keys()) and \
           ('sensor' in device.keys()):
            return '['+str(device['zone'])+'-'+str(device['sensor'])+']'
        return None
