# -*- coding: utf-8 -*-

from core.logger import *

from ..subsystems.lighting import Lighting
from .basedevice import BaseDevice


class Device4652_Base(BaseDevice):
    DEVICE_SYSTEM = Lighting

    MODE_LIGHT_CTRL = 0
    MODE_AUTOMATION_CTRL = 1
    MODE_CEN = 2
    MODE_CEN_PLUS = 3
    MODE_UNCONFIGURED = 4

    MODE_IDS = ('LIGHT_CONTROL',
                'AUTOMATION_CONTROL',
                'CEN',
                'CEN_PLUS',
                'UNCONFIGURED')
    MODE_NAMES = ('Light control',
                  'Automation control',
                  'CEN',
                  'CEN+',
                  'Unconfigured')

    KOS = (400, 401, 404, 406, 500)

    def load_slot(self, sid, slot_data):
        slot = {}
        mode = None
        _keyo = slot_data.get('keyo', None)
        if _keyo is not None:
            if _keyo in self.KOS:
                mode = self.KOS.index(_keyo)
            else:
                self.log('Device4652_Base ERROR: '
                         'keyo %d unknown %s'
                         % (_keyo, str(self.KOS)))
            self.log('Device4652_Base mode slot[%d] = (%s %s)'
                     % (sid,
                        self.MODE_IDS[mode],
                        self.MODE_NAMES[mode]),
                     LOG_ERROR)
        _mode = slot_data.get('mode', None)
        if _mode is not None:
            # mode can be either
            # an int (0 - 4)
            # a MODE_IDS
            pass

        if mode is None:
            self.log('Device4652_Base ERROR: '
                     'unable to read mode value',
                     LOG_ERROR)
            return

        slot['mode'] = mode

        self.log('%d => %s' % (sid, str(slot)), LOG_ERROR)
