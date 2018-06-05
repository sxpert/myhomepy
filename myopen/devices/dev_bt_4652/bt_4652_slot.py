# -*- coding: utf-8 -*-
from core.logger import LOG_DEBUG

from ...constants import (SLOT_VAR_A, SLOT_VAR_ADDRESS, SLOT_VAR_ADDRESS_TYPE,
                         SLOT_VAR_AREA, SLOT_VAR_AUTOMATION_CONTROL,
                         SLOT_VAR_BUTTON_DOWN, SLOT_VAR_BUTTON_UP,
                         SLOT_VAR_CEN_PLUS, SLOT_VAR_DELAY, SLOT_VAR_GROUP,
                         SLOT_VAR_LIGHT_CONTROL, SLOT_VAR_MODE, SLOT_VAR_PL,
                         SLOT_VAR_REF_A, SLOT_VAR_REF_ADDRESS, SLOT_VAR_REF_PL,
                         SLOT_VAR_STATE)
from ..baseslot import F_KO, BaseSlot
from ..dev_utils import (check_byte_addr, get_check, get_check_value,
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
        'values': ['list', KOS],
        'disp': {'label': 'Operating mode', 'order': 0}
    },
    F_LIGHT_CONTROL: {
        'param': 0,
        'values': ['list', LIGHT_CONTROL],
        'cond': ('==', F_KO, KO_LIGHT_CONTROL),
        'disp': {'label': 'Light op. mode', 'order': 1}
    },
    F_AUTOMATION_CONTROL: {
        'param': 0,
        'values': ['list', AUTOMATION_CONTROL],
        'cond': ('==', F_KO, KO_AUTOMATION_CONTROL),
        'disp': {'label': 'Automation op. mode', 'order': 1}
    },
    F_CEN: {
        'param': 0,
        'values': ['list', CEN],
        'cond': ('==', F_KO, KO_CEN),
        'disp': {'label': 'CEN command', 'order': 1}
    },
    F_CEN_PLUS: {
        'param': {0: 'low_8', 1: 'high_8'},
        'values': ['int', CEN_PLUS_MIN, CEN_PLUS_MAX],
        'cond': ('==', F_KO, KO_CEN_PLUS),
        'disp': {'label': 'CEN+ command', 'order': 1}
    },
    F_ADDRESS_TYPE: {
        'param': 1,
        'values': ['list', ADDRESS_TYPE],
        'cond': ('in', F_KO, (KO_LIGHT_CONTROL, KO_AUTOMATION_CONTROL)),
        'disp': {'label': 'Addressing mode', 'order': 2}
    },
    F_BUTTON_UP: {
        'param': 2,
        'values': ['int', CEN_PLUS_BUTTON_MIN, CEN_PLUS_BUTTON_MAX],
        'cond': ('==', F_KO, KO_CEN_PLUS),
        'disp': {'label': 'Top button', 'order': 2}
    },
    F_ADDRESS: {
        'param': 2,
        'values': ['address', '8_bit'],
        'cond': ('and', (('in', F_KO, (KO_LIGHT_CONTROL, KO_AUTOMATION_CONTROL)), ('==', F_ADDRESS_TYPE, AT_P2P))),
        'disp': {'label': 'Address', 'order': 3}
    },
    F_AREA: {
        'param': 2,
        'values': ['area'],
        'cond': ('and', (('in', F_KO, (KO_LIGHT_CONTROL, KO_AUTOMATION_CONTROL)), ('==', F_ADDRESS_TYPE, AT_AREA))),
        'disp': {'label': 'Area', 'order': 3}
    },
    F_GROUP: {
        'param': 2,
        'values': ['group'],
        'cond': ('and', (('in', F_KO, (KO_LIGHT_CONTROL, KO_AUTOMATION_CONTROL)), ('==', F_ADDRESS_TYPE, AT_GROUP))),
        'disp': {'label': 'Group', 'order': 3}
    },
    F_REF_ADDRESS: {
        'param': 5,
        'values': ['address', '8_bit'],
        'cond': ('and', (('in', F_KO, (KO_LIGHT_CONTROL, KO_AUTOMATION_CONTROL)), ('in', F_ADDRESS_TYPE, (AT_AREA, AT_GROUP)))),
        'disp': {'label': 'Status address', 'order': 4}
    },
    F_BUTTON_DOWN: {
        'param': 3,
        'values': ['int', CEN_PLUS_BUTTON_MIN, CEN_PLUS_BUTTON_MAX],
        'cond': ('==', F_KO, KO_CEN_PLUS),
        'disp': {'label': 'Bottom button', 'order': 3}
    },
    F_DELAY: {
        'param': 17,
        'values': ['list', DELAYS],
        'cond': ('and', (('==', F_KO, KO_LIGHT_CONTROL), ('==', F_LIGHT_CONTROL, LC_TIMED_ON))),
        'disp': {'label': 'Duration', 'order': 5}
    }
}

class Device4652_Slot(BaseSlot):
    FIELDS = FIELDS
    
    @property
    def slot_options(self):
        options = super().slot_options
        options['slot_type']= '4652'
        return options
