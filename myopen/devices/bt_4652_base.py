# -*- coding: utf-8 -*-

from core.logger import *

from ..subsystems.lighting import Lighting
from .basedevice import BaseDevice


class Device4652_Base(BaseDevice):
    DEVICE_SYSTEM = Lighting

    MODE_UNCONFIGURED = 0
    MODE_LIGHT_CTRL = 1
    MODE_AUTOMATION_CTRL = 2
    MODE_CEN = 3
    MODE_CEN_PLUS = 4

    MODE_IDS = ('UNCONFIGURED',
                'LIGHT_CONTROL',
                'AUTOMATION_CONTROL',
                'CEN',
                'CEN_PLUS')
    MODE_NAMES = ('Unconfigured',
                  'Light control',
                  'Automation control',
                  'CEN',
                  'CEN+')

    KOS = (500, 400, 401, 404, 406)

    def _get_mode_from_keyo(self, _keyo):
        _mode = None
        if _keyo is not None:
            if _keyo in self.KOS:
                _mode = self.KOS.index(_keyo)
            else:
                self.log('Device4652_Base ERROR: '
                         'keyo %d unknown %s'
                         % (_keyo, str(self.KOS)),
                         LOG_ERROR)
        return _mode

    def _get_mode(self, slot_data):
        _mode = None
        _keyo = slot_data.get('keyo', None)
        if _keyo is not None:
            _mode = self._get_mode_from_keyo(_keyo)
        if _mode is None:
            _m = slot_data.get('mode', None)
            if isinstance(_m, str):
                if _m.isnumeric():
                    _m = int(_m)
                else:
                    try:
                        _m = self.MODE_IDS.index(_m)
                    except ValueError:
                        pass
            if isinstance(_m, int):
                if _m >= 0 and _m < len(self.MODE_IDS):
                    _mode = _m
        if _mode is None:
            self.log('Device4652_Base ERROR: '
                     'unable to read mode value',
                     LOG_ERROR)
        return _mode

    def load_slot(self, sid, slot_data):
        self.log('%d %s' % (sid, str(slot_data)), LOG_ERROR)
        slot = {}

        mode = self._get_mode(slot_data)
        if mode is None:
            return
        slot['mode'] = mode

        self.log('%d => %s' % (sid, str(slot)), LOG_ERROR)

    def res_ko_value(self, virt_id, slot, keyo, state):
        if not self._virt_id_check(virt_id, self._VIRT_ID_CHECK_STRICT):
            return False
        mode = self._get_mode_from_keyo(keyo)
        self.slot_set_value(slot, 'mode', mode)
        if mode != self.MODE_UNCONFIGURED and state == 1 or \
           mode == self.MODE_UNCONFIGURED and state == 0:
            # should not happen
            self.slot_set_value(slot, 'state', state)
        return True

    def res_param_ko(self, virt_id, slot, index, val_par):
        if not self._virt_id_check(virt_id, self._VIRT_ID_CHECK_STRICT):
            return False

        mode = self.slot_get_value(slot, 'mode', None)
        if mode is not None:
            if mode == self.MODE_CEN_PLUS:
                if index == 0:
                    self.log('saving value %d' % (val_par), LOG_ERROR)
                    self.slot_set_value(slot, '_cenplus_temp', val_par)
                    return True
                elif index == 1:
                    value = self.slot_del_value(slot, '_cenplus_temp', 0)
                    self.log('saved value %d' % (value), LOG_ERROR)
                    value += val_par * 256
                    self.log('new value %d' % (value), LOG_ERROR)
                    self.slot_set_value(slot, 'cenplus', value)
                    return True

        self.slot_set_param(slot, index, val_par)
        return True
