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

    KOS = (500, 400, 401, 404, 406)
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

    LIGHT_CTRL_TOGGLE = 0
    LIGHT_CTRL_TIMED_ON = 1
    LIGHT_CTRL_TOGGLE_DIMMER = 2
    LIGHT_CTRL_ON_OFF_DIMMING = 3
    LIGHT_CTRL_ON_OFF_P2P_DIMMING = 4
    LIGHT_CTRL_OFF = 5
    LIGHT_CTRL_ON = 6
    LIGHT_CTRL_PUL = 7

    LIGHT_CTRL = (0, 1, 2, 3, 9, 10, 11, 15)
    LIGHT_CTRL_IDS = ('TOGGLE',
                      'TIMED_ON',
                      'TOGGLE_DIMMER',
                      'ON_OFF_DIMMING',
                      'ON_OFF_P2P_DIMMING',
                      'OFF',
                      'ON',
                      'PUL')
    LIGHT_CTRL_NAMES = ('Toggle',
                        'Timed On',
                        'Toggle Dimmer',
                        'On/Off Dimming',
                        'On/Off and Point-to-Point Dimming',
                        'Off',
                        'On',
                        'Pushbutton')

    AUTOMATION_BISTABLE = 0
    AUTOMATION_MONOSTABLE = 1
    AUTOMATION_BISTABLE_BLADES = 2

    AUTOMATION = (12, 13, 14)
    AUTOMATION_IDS = ('BISTABLE',
                      'MONOSTABLE',
                      'BISTABLE_BLADES')
    AUTOMATION_NAMES = ('Bistable',
                        'Monostable',
                        'Bistable and Blades')

    ADDR_TYPE_P2P = 0
    ADDR_TYPE_AREA = 1
    ADDR_TYPE_GROUP = 2
    ADDR_TYPE_GENERAL = 3
    ADDR_TYPE = (0, 1, 2, 3)
    ADDR_TYPE_IDS = ('P2P',
                     'AREA',
                     'GROUP',
                     'GENERAL')
    ADDR_TYPE_NAMES = ('Point to Point',
                       'Area',
                       'Group',
                       'General')

    CEN_PLUS_DEFAULT = 1
    CEN_PLUS_BUTTON_UP_DEFAULT = 1
    CEN_PLUS_BUTTON_DOWN_DEFAULT = 2
    CEN_PLUS_BUTTON_MIN = 1
    CEN_PLUS_BUTTON_MAX = 32

    SLOT_VAR_KEYO = 'keyo'
    SLOT_VAR_MODE = 'mode'
    SLOT_VAR_STATE = 'state'
    SLOT_VAR_LIGHT_CONTROL = 'light_control'
    SLOT_VAR_AUTOMATION_CONTROL = 'automation_control'
    SLOT_VAR_AREA = 'area'
    SLOT_VAR_GROUP = 'group'
    SLOT_VAR_ADDRESS_TYPE = 'address_type'
    SLOT_VAR_ADDRESS = 'address'
    SLOT_VAR_A = 'a'
    SLOT_VAR_PL = 'pl'
    SLOT_VAR_REF_ADDRESS = 'ref_address'
    SLOT_VAR_REF_A = 'ref_a'
    SLOT_VAR_REF_PL = 'ref_pl'
    SLOT_VAR_CEN_PLUS = 'cen_plus'
    SLOT_VAR_CEN_PLUS_TEMP = '_cen_plus_temp'
    SLOT_VAR_BUTTON_UP = 'button_up'
    SLOT_VAR_BUTTON_DOWN = 'button_down'

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
        _keyo = slot_data.get(self.SLOT_VAR_KEYO, None)
        if _keyo is not None:
            _mode = self._get_mode_from_keyo(_keyo)
        if _mode is None:
            _m = slot_data.get(self.SLOT_VAR_MODE, None)
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
        slot[self.SLOT_VAR_MODE] = mode

        if mode == self.MODE_LIGHT_CTRL:
            light_control = self.get_check_param(
                0, (self.LIGHT_CTRL,),
                self.SLOT_VAR_LIGHT_CONTROL,
                (self.LIGHT_CTRL, self.LIGHT_CTRL_IDS),
                slot_data)
            if light_control is None:
                return
            slot[self.SLOT_VAR_LIGHT_CONTROL] = light_control

        if mode == self.MODE_AUTOMATION_CTRL:
            automation_control = self.get_check_param(
                0, (self.AUTOMATION,),
                self.SLOT_VAR_AUTOMATION_CONTROL,
                (self.AUTOMATION, self.AUTOMATION_IDS),
                slot_data)
            if automation_control is None:
                return
            slot[self.SLOT_VAR_AUTOMATION_CONTROL] = automation_control

        if mode in (self.MODE_LIGHT_CTRL, self.MODE_AUTOMATION_CTRL):
            address_type = self.get_check_param(
                1, (self.ADDR_TYPE,),
                self.SLOT_VAR_ADDRESS_TYPE,
                (self.ADDR_TYPE, self.ADDR_TYPE_IDS),
                slot_data)
            if address_type is None:
                return
            slot[self.SLOT_VAR_ADDRESS_TYPE] = address_type

            if address_type == self.ADDR_TYPE_P2P:
                address = self.get_check_param(
                    2, (self.check_byte_addr,),
                    self.SLOT_VAR_ADDRESS, (self.check_byte_addr,),
                    slot_data)
                if address is None:
                    return
                a, pl = self.split_byte_addr(address)
                slot[self.SLOT_VAR_A] = a
                slot[self.SLOT_VAR_PL] = pl

            if address_type == self.ADDR_TYPE_AREA:
                area = self.get_check_param(
                    2, (range(0, 11),),
                    self.SLOT_VAR_AREA, (range(0, 11),),
                    slot_data)
                if area is None:
                    return
                slot[self.SLOT_VAR_AREA] = area

            if address_type == self.ADDR_TYPE_GROUP:
                group = self.get_check_param(
                    2, (range(1, 255),),
                    self.SLOT_VAR_GROUP, (range(1, 255),),
                    slot_data)
                if group is None:
                    return
                slot[self.SLOT_VAR_GROUP] = group

            if address_type in (self.ADDR_TYPE_AREA, self.ADDR_TYPE_GROUP,):
                ref_address = self.get_check_param(
                    5, (self.check_byte_addr,),
                    self.SLOT_VAR_REF_ADDRESS, (self.check_byte_addr,),
                    slot_data)
                if ref_address is None:
                    return
                ref_a, ref_pl = self.split_byte_addr(ref_address)
                slot[self.SLOT_VAR_REF_A] = ref_a
                slot[self.SLOT_VAR_REF_PL] = ref_pl

        if mode == self.MODE_CEN_PLUS:
            slot[self.SLOT_VAR_CEN_PLUS] = \
                slot_data.get(self.SLOT_VAR_CEN_PLUS,
                              self.CEN_PLUS_DEFAULT)
            slot[self.SLOT_VAR_BUTTON_UP] = \
                slot_data.get(self.SLOT_VAR_BUTTON_UP,
                              self.CEN_PLUS_BUTTON_UP_DEFAULT)
            slot[self.SLOT_VAR_BUTTON_DOWN] = \
                slot_data.get(self.SLOT_VAR_BUTTON_DOWN,
                              self.CEN_PLUS_BUTTON_DOWN_DEFAULT)

        self.log('%d => %s' % (sid, str(slot)), LOG_ERROR)
        # TODO: set slot

    def dump_slot(self, sid):
        slot = self.slot_get_slot(sid)
        mode = slot.get('mode', None)
        if mode is not None:
            slot['mode'] = self.MODE_IDS[mode]
        return slot

    def res_ko_value(self, virt_id, slot, keyo, state):
        if not self._virt_id_check(virt_id, self._VIRT_ID_CHECK_STRICT):
            return False
        mode = self._get_mode_from_keyo(keyo)
        self.slot_set_value(slot, self.SLOT_VAR_MODE, mode)
        if mode != self.MODE_UNCONFIGURED and state == 1 or \
           mode == self.MODE_UNCONFIGURED and state == 0:
            # should not happen
            self.log('Device4652_Base.res_ko_value ERROR: '
                     'mode %d and state %d don\'t macth'
                     % (mode, state))
            self.slot_set_value(slot, self.SLOT_VAR_STATE, state)
        return True

    def res_param_ko(self, virt_id, slot, index, val_par):
        if not self._virt_id_check(virt_id, self._VIRT_ID_CHECK_STRICT):
            return False

        mode = self.slot_get_value(slot, self.SLOT_VAR_MODE, None)
        if mode is not None:
            if mode == self.MODE_CEN_PLUS:
                if index == 0:
                    self.slot_set_value(
                        slot, self.SLOT_VAR_CEN_PLUS_TEMP, val_par)
                    return True
                elif index == 1:
                    value = self.slot_get_value(
                        slot, self.SLOT_VAR_CEN_PLUS_TEMP, 0)
                    value += val_par * 256
                    self.slot_set_value(slot, self.SLOT_VAR_CEN_PLUS, value)
                    return True
                elif index == 2:
                    self.slot_set_value(slot, self.SLOT_VAR_BUTTON_UP,
                                        val_par)
                    return True
                elif index == 3:
                    self.slot_set_value(slot, self.SLOT_VAR_BUTTON_DOWN,
                                        val_par)
                    return True

        self.slot_set_param(slot, index, val_par)
        return True
