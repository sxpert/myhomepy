# -*- coding: utf-8 -*-
from ..constants import *
from .dev_utils import *
from .baseslot import BaseSlot


class Device4652_Slot(BaseSlot):
    MODE_UNCONFIGURED = 0
    MODE_LIGHT_CTRL = 1
    MODE_AUTOMATION_CTRL = 2
    MODE_CEN = 3
    MODE_CEN_PLUS = 4

    KOS = (500, 400, 401, 404, 406)
    MODE_IDS = ('UNCONFIGURED', 'LIGHT_CONTROL', 'AUTOMATION_CONTROL',
                'CEN', 'CEN_PLUS')
    MODE_NAMES = ('Unconfigured', 'Light control', 'Automation control',
                  'CEN', 'CEN+')
    LIGHT_CTRL_TOGGLE = 0
    LIGHT_CTRL_TIMED_ON = 1
    LIGHT_CTRL_TOGGLE_DIMMER = 2
    LIGHT_CTRL_ON_OFF_DIMMING = 3
    LIGHT_CTRL_ON_OFF_P2P_DIMMING = 4
    LIGHT_CTRL_OFF = 5
    LIGHT_CTRL_ON = 6
    LIGHT_CTRL_PUL = 7

    LIGHT_CTRL = (0, 1, 2, 3, 9, 10, 11, 15)
    LIGHT_CTRL_IDS = ('TOGGLE', 'TIMED_ON', 'TOGGLE_DIMMER', 'ON_OFF_DIMMING',
                      'ON_OFF_P2P_DIMMING', 'OFF', 'ON', 'PUL')
    LIGHT_CTRL_NAMES = ('Toggle', 'Timed On', 'Toggle Dimmer',
                        'On/Off Dimming', 'On/Off and Point-to-Point Dimming',
                        'Off', 'On', 'Pushbutton')

    DELAY_1_M = 1
    DELAY_2_M = 2
    DELAY_3_M = 3
    DELAY_4_M = 4
    DELAY_5_M = 5
    DELAY_15_M = 6
    DELAY_30_S = 7
    DELAY_0_5_S = 8
    DELAY_2_S = 9
    DELAY_10_M = 10
    DELAYS_IDS = ('1_M', '2_M', '3_M', '4_M', '5_M',
                  '15_M', '30_S', '0_5_S', '2_S', '10_M')
    DELAYS_NAMES = ('1 mn', '2 mn', '3 mn', '4 mn', '5 mn',
                    '15 mn', '30 s', '0.5 s', '2 s', '10 mn')

    AUTOMATION_BISTABLE = 0
    AUTOMATION_MONOSTABLE = 1
    AUTOMATION_BISTABLE_BLADES = 2

    AUTOMATION = (12, 13, 14)
    AUTOMATION_IDS = ('BISTABLE', 'MONOSTABLE', 'BISTABLE_BLADES')
    AUTOMATION_NAMES = ('Bistable', 'Monostable', 'Bistable and Blades')

    ADDR_TYPE_P2P = 0
    ADDR_TYPE_AREA = 1
    ADDR_TYPE_GROUP = 2
    ADDR_TYPE_GENERAL = 3
    ADDR_TYPE = (0, 1, 2, 3)
    ADDR_TYPE_IDS = ('P2P', 'AREA', 'GROUP', 'GENERAL')
    ADDR_TYPE_NAMES = ('Point to Point', 'Area', 'Group', 'General')

    CEN_PLUS_MIN = 1
    CEN_PLUS_MAX = 2047
    CEN_PLUS_BUTTON_MIN = 1
    CEN_PLUS_BUTTON_MAX = 32

    # ========================================================================
    #
    # json loading function
    #
    # ========================================================================

    def get_mode_from_keyo(self, keyo):
        mode = None
        if keyo is not None:
            if keyo in self.KOS:
                mode = self.KOS.index(keyo)
            else:
                self.log('Device4652_Base ERROR: '
                         'keyo %d unknown %s'
                         % (keyo, str(self.KOS)),
                         LOG_ERROR)
        return mode

    def get_mode(self, data):
        mode = None
        keyo = data.get(SLOT_VAR_KEYO, None)
        if keyo is not None:
            mode = self.get_mode_from_keyo(keyo)
        if mode is None:
            m = data.get(SLOT_VAR_MODE, None)
            if isinstance(m, str):
                if m.isdecimal():
                    m = int(m)
                else:
                    try:
                        m = self.MODE_IDS.index(m)
                    except ValueError:
                        pass
            if isinstance(m, int):
                if m >= 0 and m < len(self.MODE_IDS):
                    mode = m
        if mode is None:
            self.log('Device4652_Slot ERROR: '
                     'unable to read mode value',
                     LOG_ERROR)
        return mode

    def loads(self, data):
        print('%s.loads : %s'
              % (self.__class__.__name__, str(data)))
        mode = self.get_mode(data)
        if mode is None:
            return False

        self.set_value(SLOT_VAR_MODE, mode)

        if mode == self.MODE_LIGHT_CTRL:
            light_control = get_check(
                data, 0, (self.LIGHT_CTRL,), SLOT_VAR_LIGHT_CONTROL,
                (self.LIGHT_CTRL, self.LIGHT_CTRL_IDS))
            if light_control is None:
                return False
            self.set_value(SLOT_VAR_LIGHT_CONTROL, light_control)

            if light_control == self.LIGHT_CTRL_TIMED_ON:
                delay = self.get_check_param(
                    data, 17, (self.DELAYS,), self.SLOT_VAR_DELAY,
                    (self.DELAYS, self.DELAYS_IDS))
                if delay is None:
                    return False
                self.set_value(SLOT_VAR_DELAY, delay)

        if mode == self.MODE_AUTOMATION_CTRL:
            automation_control = get_check(
                data, 0, (self.AUTOMATION,), SLOT_VAR_AUTOMATION_CONTROL,
                (self.AUTOMATION, self.AUTOMATION_IDS))
            if automation_control is None:
                return False
            self.set_value(SLOT_VAR_AUTOMATION_CONTROL, automation_control)

        if mode in (self.MODE_LIGHT_CTRL, self.MODE_AUTOMATION_CTRL):
            address_type = get_check(
                data, 1, (self.ADDR_TYPE,), SLOT_VAR_ADDRESS_TYPE,
                (self.ADDR_TYPE, self.ADDR_TYPE_IDS))
            if address_type is None:
                return False
            self.set_value(SLOT_VAR_ADDRESS_TYPE, address_type)

            if address_type == self.ADDR_TYPE_P2P:
                # this is not fatal as we have other options
                address = get_check(
                    data, 2, (check_byte_addr,),
                    SLOT_VAR_ADDRESS, (check_byte_addr,), warn=False)
                if address is None:
                    # look for a and pl
                    a = get_check_value(data, SLOT_VAR_A, (range(0, 11),))
                    pl = get_check_value(data, SLOT_VAR_PL, (range(0, 16),))
                    if a is None or pl is None:
                        return False
                else:
                    a, pl = split_byte_addr(address)
                self.set_value(SLOT_VAR_A, a)
                self.set_value(SLOT_VAR_PL, pl)

            if address_type == self.ADDR_TYPE_AREA:
                area = get_check(
                    data, 2, (range(0, 11),),
                    SLOT_VAR_AREA, (range(0, 11),))
                if area is None:
                    return False
                self.set_value(SLOT_VAR_AREA, area)

            if address_type == self.ADDR_TYPE_GROUP:
                group = get_check(
                    data, 2, (range(1, 255),),
                    SLOT_VAR_GROUP, (range(1, 255),))
                if group is None:
                    return False
                self.set_value(SLOT_VAR_GROUP, group)

            if address_type in (self.ADDR_TYPE_AREA, self.ADDR_TYPE_GROUP,):
                ref_address = get_check(
                    data, 5, (check_byte_addr,),
                    SLOT_VAR_REF_ADDRESS, (check_byte_addr,), warn=False)
                if ref_address is None:
                    # look for a and pl
                    ref_a = get_check_value(data, SLOT_VAR_REF_A,
                                            (range(0, 11),))
                    ref_pl = get_check_value(data, SLOT_VAR_REF_PL,
                                             (range(0, 16),))
                    if ref_a is None or ref_pl is None:
                        return False
                else:
                    ref_a, ref_pl = split_byte_addr(ref_address)
                self.set_value(SLOT_VAR_REF_A, ref_a)
                self.set_value(SLOT_VAR_REF_PL, ref_pl)

        # missing MODE_CEN

        if mode == self.MODE_CEN_PLUS:

            range_cen_plus = range(
                self.CEN_PLUS_MIN,
                self.CEN_PLUS_MAX + 1)

            cen_plus = get_check_value(
                data, SLOT_VAR_CEN_PLUS, (range_cen_plus,))
            if cen_plus is None:
                # TODO: look for params 0 and 1
                return False
            self.set_value(SLOT_VAR_CEN_PLUS, cen_plus)

            range_cen_plus_button = range(
                self.CEN_PLUS_BUTTON_MIN,
                self.CEN_PLUS_BUTTON_MAX + 1)

            button_up = get_check(
                data, 2, (range_cen_plus_button,),
                SLOT_VAR_BUTTON_UP, (range_cen_plus_button,))
            if button_up is None:
                return False
            self.set_value(SLOT_VAR_BUTTON_UP, button_up)

            button_down = get_check(
                data, 3, (range_cen_plus_button,),
                SLOT_VAR_BUTTON_DOWN, (range_cen_plus_button,))
            if button_down is None:
                return False
            self.set_value(SLOT_VAR_BUTTON_DOWN, button_down)

        return True

    # ========================================================================
    #
    # json generating
    #
    # ========================================================================

    def json_mode(self, data):
        mode = self.get_value(SLOT_VAR_MODE, None)
        if mode is not None:
            data[SLOT_VAR_MODE] = self.MODE_IDS[mode]
        return mode

    def json_light_control(self, data):
        light_control = self.get_value(SLOT_VAR_LIGHT_CONTROL, None)
        if light_control is not None:
            data[SLOT_VAR_LIGHT_CONTROL] = self.LIGHT_CTRL_IDS[light_control]
        if light_control is self.LIGHT_CTRL_TIMED_ON:
            delay = self.json_set_var(SLOT_VAR_DELAY, None)
            if delay is None:
                return None
        return light_control

    def json_automation_control(self, data):
        automation_control = self.get_value(SLOT_VAR_AUTOMATION_CONTROL, None)
        if automation_control is not None:
            data[SLOT_VAR_AUTOMATION_CONTROL] = \
                self.AUTOMATION_IDS[automation_control]
        return automation_control

    def json_address_type(self, data):
        address_type = self.get_value(SLOT_VAR_ADDRESS_TYPE, None)
        if address_type is not None:
            data[SLOT_VAR_ADDRESS_TYPE] = self.ADDR_TYPE_IDS[address_type]
            if address_type == self.ADDR_TYPE_P2P:
                a = self.json_set_var(SLOT_VAR_A, data)
                pl = self.json_set_var(SLOT_VAR_PL, data)
                if a is None or pl is None:
                    return None
            if address_type == self.ADDR_TYPE_AREA:
                area = self.json_set_var(SLOT_VAR_AREA, data)
                if area is None:
                    return None
            if address_type == self.ADDR_TYPE_GROUP:
                group = self.json_set_var(SLOT_VAR_GROUP, data)
                if group is None:
                    return None
            if address_type in (self.ADDR_TYPE_AREA, self.ADDR_TYPE_GROUP,):
                ref_a = self.json_set_var(SLOT_VAR_REF_PL, data)
                ref_pl = self.json_set_Var(SLOT_VAR_REF_PL, data)
                if ref_a is None or ref_pl is None:
                    return None
        return address_type

    def json_cen_plus(self, data):
        cen_plus = self.json_set_var(SLOT_VAR_CEN_PLUS, data)
        if cen_plus is None:
            return None
        button_up = self.json_set_var(SLOT_VAR_BUTTON_UP, data)
        if button_up is None:
            return None
        button_down = self.json_set_var(SLOT_VAR_BUTTON_DOWN, data)
        if button_down is None:
            return None
        return cen_plus

    def __to_json__(self):
        data = super().__to_json__()
        data['_source'] = super().__class__.__name__
        _data = {}
        mode = self.json_mode(_data)
        if mode is None:
            return data
        if mode is self.MODE_LIGHT_CTRL:
            light_control = self.json_light_control(_data)
            if light_control is None:
                return data
        if mode == self.MODE_AUTOMATION_CTRL:
            automation_control = self.json_automation_control(_data)
            if automation_control is None:
                return data
        if mode in (self.MODE_LIGHT_CTRL, self.MODE_AUTOMATION_CTRL,):
            address_type = self.json_address_type(_data)
            if address_type is None:
                return data
        if mode == self.MODE_CEN_PLUS:
            cen_plus = self.json_cen_plus(_data)
            if cen_plus is None:
                return data
        return _data

    # ========================================================================
    #
    # config-reactor functions
    #
    # ========================================================================

    def res_ko_value(self, keyo, state):
        mode = self.get_mode_from_keyo(keyo)
        self.set_value(SLOT_VAR_MODE, mode)
        if mode != self.MODE_UNCONFIGURED and state == 1 or \
           mode == self.MODE_UNCONFIGURED and state == 0:
            # should not happen
            self.log('Device4652_Slot.res_ko_value ERROR: '
                     'mode %d and state %d don\'t match'
                     % (mode, state))
            self.set_value(SLOT_VAR_STATE, state)
        return True

    def res_param_ko(self, index, val_par):
        mode = self.get_value(SLOT_VAR_MODE, None)
        if mode is not None:
            if mode == self.MODE_LIGHT_CTRL:
                if index == 0:
                    self.set_value(SLOT_VAR_LIGHT_CONTROL, val_par)
                    return True
                if index == 17:
                    light_control = self.get_value(
                        SLOT_VAR_LIGHT_CONTROL, None)
                    if light_control == self.LIGHT_CTRL_TIMED_ON:
                        self.set_value(SLOT_VAR_DELAY, val_par)
                        return True
            if mode == self.MODE_AUTOMATION_CTRL:
                if index == 0:
                    self.set_value(SLOT_VAR_AUTOMATION_CONTROL, val_par)
                    return True
            if mode in (self.MODE_LIGHT_CTRL, self.MODE_AUTOMATION_CTRL,):
                if index == 1:
                    self.set_value(SLOT_VAR_ADDRESS_TYPE, val_par)
                    return True
                if index == 2:
                    addr_type = self.get_value(SLOT_VAR_ADDRESS_TYPE, None)
                    if addr_type == self.ADDR_TYPE_P2P:
                        a, pl = split_byte_addr(val_par)
                        self.set_value(SLOT_VAR_A, a)
                        self.set_value(SLOT_VAR_PL, pl)
                        return True
                    if addr_type == self.ADDR_TYPE_AREA:
                        self.set_value(SLOT_VAR_AREA, val_par)
                        return True
                    if addr_type == self.ADDR_TYPE_GROUP:
                        self.set_value(SLOT_VAR_GROUP, val_par)
                        return True
                if index == 5:
                    addr_type = self.get_value(SLOT_VAR_ADDRESS_TYPE, None)
                    if addr_type in (self.ADDR_TYPE_AREA,
                                     self.ADDR_TYPE_GROUP,):
                        a, pl = split_byte_addr(val_par)
                        self.set_value(SLOT_VAR_REF_A, a)
                        self.set_value(SLOT_VAR_REF_PL, pl)
                        return True
            # missin CEN
            if mode == self.MODE_CEN_PLUS:
                if index == 0:
                    self._cen_plus_temp = val_par
                    return True
                elif index == 1:
                    value = val_par * 256 + self._cen_plus_temp
                    self.set_value(SLOT_VAR_CEN_PLUS, value)
                    return True
                elif index == 2:
                    self.set_value(SLOT_VAR_BUTTON_UP, val_par)
                    return True
                elif index == 3:
                    self.set_value(SLOT_VAR_BUTTON_DOWN, val_par)
                    return True
        self.set_param(index, val_par)
        return True
