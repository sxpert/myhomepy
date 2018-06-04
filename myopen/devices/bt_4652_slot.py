# -*- coding: utf-8 -*-
from core.logger import LOG_DEBUG

from ..constants import (SLOT_VAR_A, SLOT_VAR_ADDRESS, SLOT_VAR_ADDRESS_TYPE,
                         SLOT_VAR_AREA, SLOT_VAR_AUTOMATION_CONTROL,
                         SLOT_VAR_BUTTON_DOWN, SLOT_VAR_BUTTON_UP,
                         SLOT_VAR_CEN_PLUS, SLOT_VAR_DELAY, SLOT_VAR_GROUP,
                         SLOT_VAR_LIGHT_CONTROL, SLOT_VAR_MODE, SLOT_VAR_PL,
                         SLOT_VAR_REF_A, SLOT_VAR_REF_ADDRESS, SLOT_VAR_REF_PL,
                         SLOT_VAR_STATE)
from .baseslot import F_KO, BaseSlot
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

    # # ========================================================================
    # #
    # # values checking function
    # #
    # # ========================================================================

    # def recurse_conditions(self, cond):
    #     op = cond[0]
    #     result = False
    #     if op == '==':
    #         field = cond[1]
    #         value = cond[2]
    #         field_value = self.get_value(field, None)
    #         if field_value is None:
    #             return False
    #         result = (field_value == value)
    #     elif op == 'in':
    #         field = cond[1]
    #         values = cond[2]
    #         field_value = self.get_value(field, None)
    #         if field_value is None:
    #             return False
    #         result = field_value in values
    #     elif op == 'and':
    #         result = True
    #         conds = cond[1]
    #         for cond in conds:
    #             result = result and self.recurse_conditions(cond)
    #     else:
    #         self.log('unknown operator %s' % (str(op)))
    #     return result

    # def field_conditions_test(self, field_name):
    #     """
    #     Tests if field conditions are met with the data currently available
    #     """
    #     field = self.FIELDS[field_name]
    #     cond = field.get('cond', None)
    #     # no conditions, always ok
    #     if cond is None:
    #         return True
    #     return self.recurse_conditions(cond)

    # def find_field(self, param_id):
    #     """
    #     Finds which field corresponds to the param_id, 
    #     depending on data already there in the slot
    #     """
    #     found = False
    #     fields = []
    #     ok = False
    #     for f in self.FIELDS.keys():
    #         field = self.FIELDS[f]
    #         param = field['param']
    #         ok = False
    #         if isinstance(param, dict):
    #             for p in param.keys():
    #                 if p == param_id:
    #                     # append to list of tried fields
    #                     fields.append(f)
    #                     found = True
    #                     ok = self.field_conditions_test(f)  
    #         elif isinstance(param, int):
    #             if param == param_id:
    #                 # append to list of tried fields
    #                 fields.append(f)
    #                 found = True
    #                 ok = self.field_conditions_test(f)
    #         # else skip field...
    #         if ok:
    #             return (found, ok, f)
    #     # should not happen ;-)
    #     return (found, ok, fields)

    # def set_check_value(self, field_name, value, loads=False):
    #     field = self.FIELDS[field_name]
    #     values = field['values']
    #     if isinstance(values, tuple) or isinstance(values, list):
    #         v_type = values[0]
    #     elif isinstance(values, str):
    #         v_type = values
    #     else:
    #         self.log('unknown values type %s' % (values.__class__.__name__))
    #     v_parse = None
    #     if v_type == 'address':
    #         if loads:
    #             if isinstance(value, dict):
    #                 a = value.get('a', None)
    #                 pl = value.get('pl', None)
    #                 if a is None or pl is None:
    #                     self.log('%s : malformed address %s' % (field_name, str(value)))
    #                     return False
    #                 addr = (a & 0xf) << 4 | (pl & 0xf)
    #                 if addr <= 0 or addr > 175:
    #                     self.log('%s : address %s invalid' % (field_name, str(value)))
    #                     return False
    #         else:
    #             v_parse = values[1]
    #             if v_parse == '8_bit':
    #                 if value > 0 and value <= 175:
    #                     a = (value & 0xf0) >> 4
    #                     pl = value & 0xf
    #                     value = {'a': a, 'pl': pl}
    #                 else:
    #                     self.log('%s : address %d invalid (should be in (1..175)' % (field_name, value))
    #                     return False
    #     elif v_type == 'area':
    #         if value < 0 or value > 10:
    #             self.log('%s : area %d invalid (should be in (0..10)' % (field_name, value))
    #             return False
    #     elif v_type == 'group':
    #         if value < 0 or value > 255:
    #             self.log('%s : group %d invalid (should be in (1..255)' % (field_name, value))
    #             return False
    #     elif v_type == 'int':
    #         v_min = values[1]
    #         v_max = values[2]
    #         if value < v_min or value > v_max:
    #             self.log('%s : int %d invalid (should be in (%d..%d)' % (field_name, value, v_min, v_max))
    #             return False
    #     elif v_type == 'list':
    #         v_dict = values[1]
    #         index = None
    #         if loads:
    #             v_list = v_dict['ids']
    #             if value in v_list:
    #                 index = v_list.index(value)
    #         v_list = v_dict['values']
    #         if loads and index is not None:
    #             value = v_list[index]
    #         if value not in v_list:
    #             self.log('%s : list %d invalid (should be in %s' % (field_name, value, str(v_list)))
    #             return False
    #     else:
    #         self.log('%s : unhandled type %s' % (field_name, v_type))
    #         return False
    #     self.log('setting value %s => %s' % (field_name, str(value)))
    #     self.set_value(field_name, value)
    #     return True

    # ========================================================================
    #
    # front-end functions
    #
    # ========================================================================
    
    @property
    def slot_options(self):
        options = {
            'slot_type': '4652',
            'fields': self.FIELDS
        }
        return options

    @property
    def web_data(self):
        slot = {}
        options = self.slot_options
        if len(options) > 0:
            slot['options'] = options
        values = self.__to_json__(True)
        slot['values'] = values
        return slot

    # # ========================================================================
    # #
    # # json loading function
    # #
    # # ========================================================================

    # def loads(self, data):
    #     loaded = []
    #     for f in data.keys():
    #         field = self.FIELDS.get(f, None)
    #         if field is None: 
    #             self.log('Unexpected field %s, %s' % (f, str(self.FIELDS.keys())))
    #         else:
    #             ok = self.field_conditions_test(f)
    #             if not ok:
    #                 self.log('We can\'t have field %s at this point' % (f))
    #             else:
    #                 # at this point, it's the contents that say if it's ok or not
    #                 if self.set_check_value(f, data[f], True):
    #                     loaded.append(f)
    #     self.log('loaded fields %s' % (str(loaded)))
    #     if len(loaded) == 0:
    #         # nothing loaded there's surely a problem
    #         return False
    #     # TODO: check for all required parameters 
    #     return True

    # # ========================================================================
    # #
    # # json generating
    # #
    # # ========================================================================

    # def __to_json__(self, numeric=False):
    #     data = {}
    #     self.log('-----------------------------------------------')
    #     self.log('id : %s | slot : %d' % (self._slots.parent.hw_addr_hex, self.number))
    #     for f in self.FIELDS.keys():
    #         ok = self.field_conditions_test(f)
    #         if ok:
    #             value = self.get_value(f, None)
    #             if value is not None:
    #                 field = self.FIELDS[f]
    #                 values = field['values']
    #                 v_type = None
    #                 if isinstance(values, tuple):
    #                     v_type = values[0]
    #                 elif isinstance(values, str):
    #                     v_type = values
    #                 if v_type == 'list':
    #                     if not numeric:
    #                         # map to a user readable value
    #                         list_values = values[1]
    #                         int_values = list_values['values']
    #                         id_values = list_values['ids']
    #                         try:
    #                             index = int_values.index(value)
    #                         except ValueError:
    #                             self.log('can\'t find %s in %s' % (str(value), str(int_values)))
    #                         else:
    #                             value = id_values[index]
    #                 self.log('%s : %s' % (f, str(value)))
    #                 data[f] = value 
    #             else:
    #                 self.log('for some reason, field %s is None' % f)
    #     return data

    # ========================================================================
    #
    # config-reactor functions
    #
    # ========================================================================

    # def res_ko_value(self, keyo, state):
    #     self.set_value(F_KO, keyo)
    #     # original code
    #     # mode = self.get_mode_from_keyo(keyo)
    #     # self.set_value(SLOT_VAR_MODE, mode)
    #     # if mode != self.MODE_UNCONFIGURED and state == 1 or \
    #     #    mode == self.MODE_UNCONFIGURED and state == 0:
    #     #     # should not happen
    #     #     self.log('Device4652_Slot.res_ko_value ERROR: '
    #     #              'mode %d and state %d don\'t match'
    #     #              % (mode, state))
    #     #     self.set_value(SLOT_VAR_STATE, state)
    #     return True

    # def res_param_ko(self, index, val_par):
    #     # parallel code
    #     found, ok, fields = self.find_field(index)
    #     self.log('PARAM %s %s %s => %s' % (str(index), str(found), str(fields), str(val_par)))
    #     if found:
    #         if ok:
    #             if not isinstance(fields, str):
    #                 self.log('%s.res_param_ko: ERROR: expected a field name, got %s \'%s\'' % 
    #                          (self.__class__.__name__, fields.__class__.__name__, str(fields)))
    #             else:
    #                 self.log('%s.res_param_ko: found %s' % (self.__class__.__name__, fields))
    #                 field_name = fields
    #                 field = self.FIELDS[field_name]
    #                 self.log(field)
    #                 param = field['param']
    #                 # those validity tests should not be necessary
    #                 if isinstance(param, int):
    #                     if param == index:
    #                         self.log('%s => %s' % (field_name, str(val_par)))
    #                         return self.set_check_value(field_name, val_par)
    #                     else:
    #                         # should never happen...
    #                         self.log('%s.res_param_ko: ERROR: For some reason, param changed param: %s index: %s' % 
    #                                  (self.__class__.__name__, str(param), str(index)))
    #                 elif isinstance(param, dict):
    #                     if index in param.keys():
    #                         action = param[index]
    #                         if action == 'low_8':
    #                             val = self.get_value(field_name, 0)
    #                             value = (val & 0xff00) | (val_par & 0xff)
    #                             self.log('%s: %08x %08x => %08x' % (action, val, val_par, value))
    #                             return self.set_check_value(field_name, value) 
    #                         elif action == 'high_8':
    #                             val = self.get_value(field_name, 0)
    #                             value = ((val_par << 8) & 0xff00) | (val & 0xff)
    #                             self.log('%s: %08x %08x => %08x' % (action, val, val_par, value))
    #                             return self.set_check_value(field_name, value)
    #                         else:
    #                             self.log('%s.res_param_ko: ERROR: unknown action %s' % 
    #                                  (self.__class__.__name__, str(action)))
    #                     else:
    #                         # should never happen either !
    #                         self.log('%s.res_param_ko: ERROR: For some reason, index is not in index: %s param: %s' % 
    #                                  (self.__class__.__name__, str(index), str(param)))
    #                 return True
    #         else:
    #             self.log('%s.res_param_ko: WARNING: none of %s validated conditions' % (self.__class__.__name__, str(fields))) 
    #             return True   
    #     else:
    #         self.log('%s.res_param_ko: WARNING: unable to find field for param %s' % (self.__class__.__name__, str(index)))
    #     return False
