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

    def parse_status(self, msg):
        super().parse_status(msg)
        # temperature report
        # '101*0*0270##'
        m = re.match('^\*(?P<probe>\d{3})\*0\*(?P<temperature>\d{4})##$', msg)
        if m is not None:
            data = m.groupdict()
            js_data = json.dumps(data)
            # generate the device key
            zone = int(data['probe'][0])
            sensor = int(data['probe'][1:])
            device = {'zone': zone, 'sensor': sensor}
            temp = float(data['temperature'])/10.0
            data = {'temp': temp, 'unit': '°C'}
            self.execute_callback(self.SYSTEM_WHO, self.OP_REPORT_TEMP,
                                  device, data)
            return True
        else:
            self.log("Temp control no match")
        self.log('temp control status ' + msg)

    def map_device(self, device):
        if (type(device) is dict) and \
           ('zone' in device.keys()) and \
           ('sensor' in device.keys()):
            return '['+str(device['zone'])+'-'+str(device['sensor'])+']'
        return None
