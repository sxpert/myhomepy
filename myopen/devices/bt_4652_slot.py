# -*- coding: utf-8 -*-
from core.logger import LOG_DEBUG

from ..constants import (SLOT_VAR_A, SLOT_VAR_ADDRESS, SLOT_VAR_ADDRESS_TYPE,
                         SLOT_VAR_AREA, SLOT_VAR_AUTOMATION_CONTROL,
                         SLOT_VAR_BUTTON_DOWN, SLOT_VAR_BUTTON_UP,
                         SLOT_VAR_CEN_PLUS, SLOT_VAR_DELAY, SLOT_VAR_GROUP,
                         SLOT_VAR_LIGHT_CONTROL, SLOT_VAR_MODE, SLOT_VAR_PL,
                         SLOT_VAR_REF_A, SLOT_VAR_REF_ADDRESS, SLOT_VAR_REF_PL,
                         SLOT_VAR_STATE)
from .baseslot import BaseSlot
from .dev_utils import (check_byte_addr, get_check, get_check_value,
                        json_find_value, map_value, split_byte_addr)

KO_UNCONFIGURED = 500
KO_LIGHT_CONTROL = 400
KO_AUTOMATION_CONTROL = 401
KO_CEN = 404
KO_CEN_PLUS = 406

KOS = {
    'values': (KO_UNCONFIGURED, KO_LIGHT_CONTROL, KO_AUTOMATION_CONTROL, KO_CEN, KO_CEN_PLUS),
    'ids': ('UNCONFIGURED', 'LIGHT_CONTROL', 'AUTOMATION_CONTROL', 'CEN', 'CEN_PLUS'),
    'names': ('Unconfigured', 'Light control', 'Automation control', 'CEN', 'CEN+')
}

LC_TOGGLE = 0
LC_TIMED_ON = 1
LC_TOGGLE_DIM = 2
LC_ON_OFF_DIM = 3
LC_ON_OFF_P2P_DIM = 9
LC_OFF = 10
LC_ON = 11
LC_PUL = 15

LIGHT_CONTROL = {
    'values': (LC_TOGGLE, LC_TIMED_ON, LC_TOGGLE_DIM, LC_ON_OFF_DIM, LC_ON_OFF_P2P_DIM, LC_OFF, LC_ON, LC_PUL),
    'ids': ('TOGGLE', 'TIMED_ON', 'TOGGLE_DIMMER', 'ON_OFF_DIMMING', 'ON_OFF_P2P_DIMMING', 'OFF', 'ON', 'PUL'),
    'names': ('Toggle', 'Timed On', 'Toggle Dimmer', 'On/Off Dimming', 'On/Off and Point-to-Point Dimming', 'Off', 'On', 'Pushbutton')
}

AC_BISTABLE = 12
AC_MONOSTABLE = 13
AC_BISTABLE_BLADES = 14

AUTOMATION_CONTROL = {
    'values': (AC_BISTABLE, AC_MONOSTABLE, AC_BISTABLE_BLADES),
    'ids': ('BISTABLE', 'MONOSTABLE', 'BISTABLE_BLADES'),
    'names': ('Bistable', 'Monostable', 'Bistable and Blades')
}

AT_P2P = 0
AT_AREA = 1
AT_GROUP = 2
AT_GENERAL = 3
ADDRESS_TYPE = {
    'values': (AT_P2P, AT_AREA, AT_GROUP, AT_GENERAL),
    'ids': ('P2P', 'AREA', 'GROUP', 'GENERAL'),
    'names': ('Point to Point', 'Area', 'Group', 'General')
}

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
DELAYS = {
    'values': (DELAY_1_M, DELAY_2_M, DELAY_3_M, DELAY_4_M, DELAY_5_M, DELAY_15_M, DELAY_30_S, DELAY_0_5_S, DELAY_2_S, DELAY_10_M),
    'ids': ('1_M', '2_M', '3_M', '4_M', '5_M', '15_M', '30_S', '0_5_S', '2_S', '10_M'),
    'names': ('1 mn', '2 mn', '3 mn', '4 mn', '5 mn', '15 mn', '30 s', '0.5 s', '2 s', '10 mn')
}

CEN = None

CEN_PLUS_MIN = 1
CEN_PLUS_MAX = 2047

CEN_PLUS_BUTTON_MIN = 1
CEN_PLUS_BUTTON_MAX = 32

F_KO = 'KO'
F_MODE = 'mode'
F_LIGHT_CONTROL = 'light_control'
F_AUTOMATION_CONTROL = 'automation_control'
F_CEN = 'cen'
F_CEN_PLUS = 'cen_plus'
F_ADDRESS_TYPE = 'address_type'
F_BUTTON_UP = 'button_up'
F_ADDRESS = 'address'
F_AREA = 'area'
F_GROUP = 'group'
F_BUTTON_DOWN = 'button_down'
F_REF_ADDRESS = 'ref_address'
F_DELAY = 'delay'

FIELDS = {
    F_KO: {
        'param': F_KO,
        'values': ('list', KOS),
        'disp': {'label': 'Operating mode', 'order': 0}
    },
    F_LIGHT_CONTROL: {
        'param': 0,
        'values': ('list', LIGHT_CONTROL),
        'cond': ('==', F_KO, KO_LIGHT_CONTROL),
        'disp': {'label': 'Light op. mode', 'order': 1}
    },
    F_AUTOMATION_CONTROL: {
        'param': 0,
        'values': ('list', AUTOMATION_CONTROL),
        'cond': ('==', F_KO, KO_AUTOMATION_CONTROL),
        'disp': {'label': 'Automation op. mode', 'order': 1}
    },
    F_CEN: {
        'param': 0,
        'values': ('list', CEN),
        'cond': ('==', F_KO, KO_CEN),
        'disp': {'label': 'CEN command', 'order': 1}
    },
    F_CEN_PLUS: {
        'param': {'low_8': 0, 'high_8': 1},
        'values': ('int', CEN_PLUS_MIN, CEN_PLUS_MAX),
        'cond': ('==', F_KO, KO_CEN_PLUS),
        'disp': {'label': 'CEN+ command', 'order': 1}
    },
    F_ADDRESS_TYPE: {
        'param': 1,
        'values': ('list', ADDRESS_TYPE),
        'cond': ('in', F_KO, (KO_LIGHT_CONTROL, KO_AUTOMATION_CONTROL)),
        'disp': {'label': 'Addressing mode', 'order': 2}
    },
    F_BUTTON_UP: {
        'param': 2,
        'values': ('int', CEN_PLUS_BUTTON_MIN, CEN_PLUS_BUTTON_MAX),
        'cond': ('==', F_KO, KO_CEN_PLUS),
        'disp': {'label': 'Top button', 'order': 2}
    },
    F_ADDRESS: {
        'param': 2,
        'values': ('address', '8_bit'),
        'cond': ('and', ('in', F_KO, (KO_LIGHT_CONTROL, KO_AUTOMATION_CONTROL)), ('==', F_ADDRESS_TYPE, AT_P2P)),
        'disp': {'label': 'Address', 'order': 3}
    },
    F_AREA: {
        'param': 2,
        'values': ('area'),
        'cond': ('and', ('in', F_KO, (KO_LIGHT_CONTROL, KO_AUTOMATION_CONTROL)), ('==', F_ADDRESS_TYPE, AT_AREA)),
        'disp': {'label': 'Area', 'order': 3}
    },
    F_GROUP: {
        'param': 2,
        'values': ('group'),
        'cond': ('and', ('in', F_KO, (KO_LIGHT_CONTROL, KO_AUTOMATION_CONTROL)), ('==', F_ADDRESS_TYPE, AT_GROUP)),
        'disp': {'label': 'Group', 'order': 3}
    },
    F_REF_ADDRESS: {
        'param': 5,
        'values': ('address', '8_bit'),
        'cond': ('and', ('in', F_KO, (KO_LIGHT_CONTROL, KO_AUTOMATION_CONTROL)), ('in', F_ADDRESS_TYPE, (AT_AREA, AT_GROUP)))
    },
    F_BUTTON_DOWN: {
        'param': 3,
        'values': ('int', CEN_PLUS_BUTTON_MIN, CEN_PLUS_BUTTON_MAX),
        'cond': ('==', F_KO, KO_CEN_PLUS),
        'disp': {'label': 'Bottom button', 'order': 3}
    },
    F_DELAY: {
        'param': 17,
        'values': ('list', DELAYS),
        'cond': ('and', (('==', F_KO, KO_LIGHT_CONTROL), ('==', LIGHT_CONTROL, LC_TIMED_ON))),
        'disp': {'label': 'Duration', 'order': 4}
    }
}

class Device4652_Slot(BaseSlot):
    MODE_UNCONFIGURED = 0
    MODE_LIGHT_CTRL = 1
    MODE_AUTOMATION_CTRL = 2
    MODE_CEN = 3
    MODE_CEN_PLUS = 4

    # KOS = (500, 400, 401, 404, 406)
    KOS = KOS['values']
    MODE_IDS = ('UNCONFIGURED', 'LIGHT_CONTROL', 'AUTOMATION_CONTROL', 'CEN', 'CEN_PLUS')
    MODE_NAMES = ('Unconfigured', 'Light control', 'Automation control', 'CEN', 'CEN+')
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
    # front-end functions
    #
    # ========================================================================
    
    @property
    def slot_options(self):
        options = {
            'slot_type': '4652',
            'fields': [
                {'name': SLOT_VAR_MODE, 'order': 1, 'type': 'select', 'options': self.MODE_NAMES},
                {'name': SLOT_VAR_LIGHT_CONTROL, 'order': 2, 'type': 'select', 'options': self.LIGHT_CTRL_NAMES,
                 'display': {'conditions': {'field': SLOT_VAR_MODE, 'op': '==', 'value': self.MODE_LIGHT_CTRL}}},
                {'name': SLOT_VAR_AUTOMATION_CONTROL, 'order': 2, 'type': 'select', 'options': self.AUTOMATION_NAMES,
                 'display': {'conditions': {'field': SLOT_VAR_MODE, 'op': '==', 'value': self.MODE_AUTOMATION_CTRL}}},
                {'name': SLOT_VAR_ADDRESS_TYPE, 'order': 3, 'type': 'select', 'options': self.ADDR_TYPE_NAMES,
                 'display': {'conditions': {'field': SLOT_VAR_MODE, 'op': 'in',
                             'values': [self.MODE_LIGHT_CTRL,self.MODE_AUTOMATION_CTRL]}}},
                {'name': SLOT_VAR_ADDRESS,'order': 4,'type': 'address',
                 'display': {'conditions': {'op': 'and', 'conditions': [
                 {'field': SLOT_VAR_MODE, 'op': 'in', 'values': [self.MODE_LIGHT_CTRL,self.MODE_AUTOMATION_CTRL]},
                 {'field': SLOT_VAR_ADDRESS_TYPE, 'op': '==', 'value': self.ADDR_TYPE_P2P}]}}},
                {'name': SLOT_VAR_AREA, 'order': 4, 'type': 'area',
                 'display': {'conditions': {'op': 'and','conditions': [
                 {'field': SLOT_VAR_MODE, 'op': 'in', 'values': [self.MODE_LIGHT_CTRL, self.MODE_AUTOMATION_CTRL]},
                 {'field': SLOT_VAR_ADDRESS_TYPE, 'op': '==', 'value': self.ADDR_TYPE_AREA}]}}},
                {'name': SLOT_VAR_GROUP, 'order': 4, 'type': 'group',
                 'display': {'conditions': {'op': 'and','conditions': [
                 {'field': SLOT_VAR_MODE, 'op': 'in', 'values': [self.MODE_LIGHT_CTRL, self.MODE_AUTOMATION_CTRL]},
                 {'field': SLOT_VAR_ADDRESS_TYPE, 'op': '==', 'value': self.ADDR_TYPE_GROUP}]}}},
                {'name': SLOT_VAR_REF_ADDRESS, 'order': 5,'type': 'address',
                 'display': {'conditions': {'op': 'and','conditions': [
                 {'field': SLOT_VAR_MODE, 'op': 'in', 'values': [self.MODE_LIGHT_CTRL, self.MODE_AUTOMATION_CTRL]},
                 {'field': SLOT_VAR_ADDRESS_TYPE, 'op': 'in', 'values': [self.ADDR_TYPE_AREA, self.ADDR_TYPE_GROUP]}]}}},
                {'name': SLOT_VAR_DELAY, 'order': 5, 'type': 'select', 'options': self.DELAYS_NAMES,
                 'display': {'conditions': {'op': 'and', 'conditions': [
                 {'field': SLOT_VAR_MODE, 'op': '==', 'value': self.MODE_LIGHT_CTRL},
                 {'field': SLOT_VAR_LIGHT_CONTROL, 'op': '==', 'value': self.LIGHT_CTRL_TIMED_ON}]}}},
                {'name': SLOT_VAR_CEN_PLUS, 'order': 2, 'type': 'integer', 'min': self.CEN_PLUS_MIN, 'max': self.CEN_PLUS_MAX,
                 'display': {'conditions': {'field': SLOT_VAR_MODE, 'op': '==', 'value': self.MODE_CEN_PLUS}}},
                {'name': SLOT_VAR_BUTTON_UP, 'order': 3, 'type': 'integer', 
                 'min': self.CEN_PLUS_BUTTON_MIN, 'max': self.CEN_PLUS_BUTTON_MAX,
                 'display': {'conditions': {'field': SLOT_VAR_MODE, 'op': '==', 'value': self.MODE_CEN_PLUS}}},
                {'name': SLOT_VAR_BUTTON_DOWN, 'order': 4, 'type': 'integer', 
                 'min': self.CEN_PLUS_BUTTON_MIN, 'max': self.CEN_PLUS_BUTTON_MAX,
                 'display': {'conditions': {'field': SLOT_VAR_MODE, 'op': '==', 'value': self.MODE_CEN_PLUS}}}
            ]
        }
        return options

    @property
    def web_data(self):
        slot = {}
        options = self.slot_options
        if len(options) > 0:
            slot['options'] = options
        values = {}
        mode = self.get_value(SLOT_VAR_MODE, None)
        if mode is not None:
            values[SLOT_VAR_MODE] = mode
        if mode == self.MODE_LIGHT_CTRL:
            light_control = self.get_value(SLOT_VAR_LIGHT_CONTROL, None)
            if light_control is not None:
                values[SLOT_VAR_LIGHT_CONTROL] = light_control
        if mode == self.MODE_AUTOMATION_CTRL:
            automation_control = self.get_value(SLOT_VAR_AUTOMATION_CONTROL, None)
            if automation_control is not None:
                values[SLOT_VAR_AUTOMATION_CONTROL] = automation_control
        if mode in (self.MODE_LIGHT_CTRL, self.MODE_AUTOMATION_CTRL):
            address_type = self.get_value(SLOT_VAR_ADDRESS_TYPE, None)
            if address_type is not None:
                values[SLOT_VAR_ADDRESS_TYPE] = address_type
                if address_type == self.ADDR_TYPE_P2P:
                    a = self.get_value(SLOT_VAR_A, None)
                    pl = self.get_value(SLOT_VAR_PL, None)
                    if a is not None and pl is not None:
                        values[SLOT_VAR_ADDRESS] = {SLOT_VAR_A: a, SLOT_VAR_PL: pl}
                if address_type == self.ADDR_TYPE_AREA:
                    area = self.get_value(SLOT_VAR_AREA, None)
                    if area is not None:
                        values[SLOT_VAR_AREA] = area
                if address_type == self.ADDR_TYPE_GROUP:
                    group = self.get_value(SLOT_VAR_GROUP, None)
                    if group is not None:
                        values[SLOT_VAR_GROUP] = group
                if address_type in (self.ADDR_TYPE_AREA, self.ADDR_TYPE_GROUP):
                    ref_a = self.get_value(SLOT_VAR_REF_A, None)
                    ref_pl = self.get_value(SLOT_VAR_REF_PL, None)
                    if ref_a is not None and ref_pl is not None:
                        values[SLOT_VAR_REF_ADDRESS] = {SLOT_VAR_A: ref_a, SLOT_VAR_PL: ref_pl}
        if mode == self.MODE_CEN_PLUS:
            cen_plus = self.get_value(SLOT_VAR_CEN_PLUS, None)
            if cen_plus is not None:
                values[SLOT_VAR_CEN_PLUS] = cen_plus
            button_up = self.get_value(SLOT_VAR_BUTTON_UP, None)
            if button_up is not None:
                values[SLOT_VAR_BUTTON_UP] = button_up
            button_down = self.get_value(SLOT_VAR_BUTTON_DOWN, None)
            if button_down is not None:
                values[SLOT_VAR_BUTTON_DOWN] = button_down
        slot['values'] = values
        return slot

    # ========================================================================
    #
    # json loading function
    #
    # ========================================================================

    def loads(self, data):
        self.log('%s.loads : %s'
                 % (self.__class__.__name__, str(data)),
                 LOG_DEBUG)
        mode = self.get_mode(data)
        if mode is None:
            return False

        self.set_value(SLOT_VAR_MODE, mode)

        if mode == self.MODE_LIGHT_CTRL:
            light_control = get_check(data, 0, SLOT_VAR_LIGHT_CONTROL,
                                      self.LIGHT_CTRL, self.LIGHT_CTRL_IDS)
            if light_control is None:
                return False
            self.set_value(SLOT_VAR_LIGHT_CONTROL, light_control)

            if light_control == self.LIGHT_CTRL_TIMED_ON:
                delay = get_check(data, 17, SLOT_VAR_DELAY,
                                  range(0, len(self.DELAYS_IDS)),
                                  self.DELAYS_IDS)
                if delay is None:
                    return False
                self.set_value(SLOT_VAR_DELAY, delay)

        if mode == self.MODE_AUTOMATION_CTRL:
            automation_control = get_check(
                data, 0, SLOT_VAR_AUTOMATION_CONTROL,
                self.AUTOMATION, self.AUTOMATION_IDS)
            if automation_control is None:
                return False
            self.set_value(SLOT_VAR_AUTOMATION_CONTROL, automation_control)

        if mode in (self.MODE_LIGHT_CTRL, self.MODE_AUTOMATION_CTRL):
            address_type = get_check(data, 1, SLOT_VAR_ADDRESS_TYPE,
                                     self.ADDR_TYPE, self.ADDR_TYPE_IDS)
            if address_type is None:
                return False
            self.set_value(SLOT_VAR_ADDRESS_TYPE, address_type)

            if address_type == self.ADDR_TYPE_P2P:
                # this is not fatal as we have other options
                address = get_check(data, 2, SLOT_VAR_ADDRESS,
                                    check_byte_addr, None, warn=False)
                if address is None:
                    # look for a and pl
                    a = get_check_value(data, SLOT_VAR_A, range(0, 11), None)
                    pl = get_check_value(data, SLOT_VAR_PL, range(0, 16), None)
                    if a is None or pl is None:
                        return False
                else:
                    a, pl = split_byte_addr(address)
                self.set_value(SLOT_VAR_A, a)
                self.set_value(SLOT_VAR_PL, pl)

            if address_type == self.ADDR_TYPE_AREA:
                area = get_check(data, 2, SLOT_VAR_AREA,
                                 range(0, 11), None)
                if area is None:
                    return False
                self.set_value(SLOT_VAR_AREA, area)

            if address_type == self.ADDR_TYPE_GROUP:
                group = get_check(data, 2, SLOT_VAR_GROUP,
                                  range(1, 255), None)
                if group is None:
                    return False
                self.set_value(SLOT_VAR_GROUP, group)

            if address_type in (self.ADDR_TYPE_AREA, self.ADDR_TYPE_GROUP,):
                ref_address = get_check(data, 5, SLOT_VAR_REF_ADDRESS,
                                        check_byte_addr, None, warn=False)
                if ref_address is None:
                    # look for a and pl
                    ref_a = get_check_value(data, SLOT_VAR_REF_A,
                                            range(0, 11), None)
                    ref_pl = get_check_value(data, SLOT_VAR_REF_PL,
                                             range(0, 16), None)
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

            cen_plus = get_check_value(data, SLOT_VAR_CEN_PLUS,
                                       range_cen_plus, None)
            if cen_plus is None:
                # TODO: look for params 0 and 1
                return False
            self.set_value(SLOT_VAR_CEN_PLUS, cen_plus)

            range_cen_plus_button = range(
                self.CEN_PLUS_BUTTON_MIN,
                self.CEN_PLUS_BUTTON_MAX + 1)

            button_up = get_check(data, 2, SLOT_VAR_BUTTON_UP,
                                  range_cen_plus_button, None)
            if button_up is None:
                return False
            self.set_value(SLOT_VAR_BUTTON_UP, button_up)

            button_down = get_check(data, 3, SLOT_VAR_BUTTON_DOWN,
                                    range_cen_plus_button, None)
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
            data[SLOT_VAR_LIGHT_CONTROL] = \
                json_find_value(light_control, self.LIGHT_CTRL_IDS)
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
                ref_a = self.json_set_var(SLOT_VAR_REF_A, data)
                ref_pl = self.json_set_var(SLOT_VAR_REF_PL, data)
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
                    val = map_value(val_par, self.LIGHT_CTRL)
                    self.set_value(SLOT_VAR_LIGHT_CONTROL, val)
                    return True
                if index == 17:
                    light_control = self.get_value(
                        SLOT_VAR_LIGHT_CONTROL, None)
                    if light_control == self.LIGHT_CTRL_TIMED_ON:
                        self.set_value(SLOT_VAR_DELAY, val_par)
                        return True
            if mode == self.MODE_AUTOMATION_CTRL:
                if index == 0:
                    val = map_value(val_par, self.AUTOMATION)
                    self.set_value(SLOT_VAR_AUTOMATION_CONTROL, val)
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
