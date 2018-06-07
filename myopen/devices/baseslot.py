# -*- coding: utf-8 -*-
from ..constants import (
    SLOT_VAR_ADDR, SLOT_VAR_KEYO, SLOT_VAR_MODE,
    SLOT_VAR_STATE, SLOT_VAR_SYS, 
    VAR_KOS, VAR_MODE_IDS, VAR_PARAMS_KEY, )
from .dev_utils import map_value
from core.logger import LOG_ERROR

__all__ = ['F_KO', 'MissingFieldsDefinitionError', 'BaseSlot', ]

F_KO = 'KO'
F_STATE = 'state'
F_SYS_ADDRESS = 'sys_address'
F_SYSTEM = 'system'

BASE_FIELDS = {
}


class MissingFieldsDefinitionError(Exception):
    pass


class BaseSlot(object):
    _FIELDS = None
    log = None

    def __init__(self, slots):
        self.log = slots.log

        FIELDS = getattr(self, 'FIELDS', None)
        # don't complain for BaseSlot instances ...
        if (self.__class__.__name__ != BaseSlot.__name__) and (FIELDS is None):
            raise MissingFieldsDefinitionError('BaseSlot.__init__ ERROR: no FIELDS member')
        bf = BASE_FIELDS.copy()
        if FIELDS is not None:
            bf.update(FIELDS)
        self._FIELDS = bf
        self._slots = slots
        self._values = {}
        self._params = {}

    def __str__(self):
        s = '<%s' % self.__class__.__name__
        for k, v in self._values.items():
            s += ' (%s: %s)' % (str(k), str(v))
        s += ' params{'
        for k, v in self._params.items():
            s += ' (%s: %s)' % (str(k), str(v))
        s += '}>'
        return s

    @property
    def number(self):
        """
        The index of this slot in the slots container
        """
        if self._slots is not None:
            return self._slots.slots.index(self)
        return None

    # ========================================================================
    #
    # values checking methods
    #
    # ========================================================================

    def recurse_conditions(self, cond):
        """
        conditions checking engine
        """
        op = cond[0]
        result = False
        if op == '==':
            field = cond[1]
            value = cond[2]
            field_value = self.get_value(field, None)
            if field_value is None:
                return False
            result = (field_value == value)
        elif op == 'in':
            field = cond[1]
            values = cond[2]
            field_value = self.get_value(field, None)
            if field_value is None:
                return False
            result = field_value in values
        elif op == 'and':
            result = True
            conds = cond[1]
            for cond in conds:
                result = result and self.recurse_conditions(cond)
        else:
            self.log('unknown operator %s' % (str(op)))
        return result

    def field_conditions_test(self, field_name):
        """
        Tests if field conditions are met with the data currently available
        """
        field = self._FIELDS[field_name]
        cond = field.get('cond', None)
        # no conditions, always ok
        if cond is None:
            return True
        return self.recurse_conditions(cond)

    def find_field(self, param_id):
        """
        Finds which field corresponds to the param_id, 
        depending on data already there in the slot
        """
        found = False
        fields = []
        ok = False
        for f in self._FIELDS.keys():
            field = self._FIELDS[f]
            param = field['param']
            ok = False
            if isinstance(param, dict):
                for p in param.keys():
                    if p == param_id:
                        # append to list of tried fields
                        fields.append(f)
                        found = True
                        ok = self.field_conditions_test(f)  
            elif isinstance(param, int):
                if param == param_id:
                    # append to list of tried fields
                    fields.append(f)
                    found = True
                    ok = self.field_conditions_test(f)
            # else skip field...
            if ok:
                return (found, ok, f)
        # should not happen ;-)
        return (found, ok, fields)

    def set_check_value(self, field_name, value, loads=False):
        """
        sets a value in the values dict, after looking if it's all
        valid according to the _FIELDS definition data
        """
        try:
            field = self._FIELDS[field_name]
        except KeyError:
            self.log("set_check_value: unable to find key '%s' in FIELDS" % (field_name))
            self.log(self._FIELDS)
        values = field['values']
        if isinstance(values, tuple) or isinstance(values, list):
            v_type = values[0]
        elif isinstance(values, str):
            v_type = values
        else:
            self.log('unknown values type %s' % (values.__class__.__name__))
        if v_type == 'address':
            self.log(self._slots.parent.subsystem)
            sub = self._slots.parent.subsystem(self._slots.parent.devices.system)
            addr_type = values[1]
            # dict values only show up during loads from config file
            if isinstance(value, dict) and loads:
                func_name = 'parse_address_dict'
            else:
                func_name = 'parse_address_'+addr_type
            func = getattr(sub, func_name, None)
            if func is not None:
                # at this point, we may want to try/except ...
                value = func(field_name, value)
                self.log(value)
            else:
                raise NotImplementedError('missing %s.%s function' % (sub.__class__.__name__, func_name))
        elif v_type == 'area':
            if value < 0 or value > 10:
                self.log('%s : area %d invalid (should be in (0..10)' % (field_name, value))
                return False
        elif v_type == 'group':
            if value < 0 or value > 255:
                self.log('%s : group %d invalid (should be in (1..255)' % (field_name, value))
                return False
        elif v_type == 'int':
            v_min = values[1]
            v_max = values[2]
            if value < v_min or value > v_max:
                self.log('%s : int %d invalid (should be in (%d..%d)' % (field_name, value, v_min, v_max))
                return False
        elif v_type == 'list':
            v_dict = values[1]
            index = None
            if loads:
                v_list = v_dict['ids']
                if value in v_list:
                    index = v_list.index(value)
            v_list = v_dict['values']
            if loads and index is not None:
                value = v_list[index]
            if value not in v_list:
                self.log('%s : list %d invalid (should be in %s' % (field_name, value, str(v_list)))
                return False
        else:
            self.log('%s : unhandled type %s' % (field_name, v_type))
            return False
        self.log('setting value %s => %s' % (field_name, str(value)))
        self.set_value(field_name, value)
        return True

    # ========================================================================
    #
    # front-end related
    #
    # ========================================================================


    @property
    def slot_options(self):
        options = {
            'fields': self._FIELDS
        }
        return options

    @property
    def web_data(self):
        slot = {}
        options = self.slot_options
        if len(options) > 0:
            slot['options'] = options
        values = self.__internal_json__(False)
        slot['values'] = values
        return slot

    # ========================================================================
    #
    # json loading function
    #
    # ========================================================================

    def loads(self, data):
        loaded = []
        try:
            keys = data.keys()
        except AttributeError:
            # empty slot, we currently have this for f411 where a slot is 
            # configured in automation mode.
            # should do something else here
            self.log(self._slots.parent)
            self.log(self._slots)
            self.log(data)
            return False
        for f in keys:
            field = self._FIELDS.get(f, None)
            if field is None: 
                self.log('Unexpected field %s, %s' % (f, str(self._FIELDS.keys())))
            else:
                ok = self.field_conditions_test(f)
                if not ok:
                    self.log('We can\'t have field %s at this point' % (f))
                else:
                    # at this point, it's the contents that say if it's ok or not
                    if self.set_check_value(f, data[f], True):
                        loaded.append(f)
        self.log('loaded fields %s' % (str(loaded)))
        if len(loaded) == 0:
            # nothing loaded there's surely a problem
            return False
        # TODO: check for all required parameters 
        return True

    # ========================================================================
    #
    # json generating
    #
    # ========================================================================

    def __internal_json__(self, symbolic=True):
        data = {}
        self.log('-----------------------------------------------')
        self.log('id : %s | slot : %d | symbolic: %s' 
                 % (self._slots.parent.hw_addr_hex, self.number, str(symbolic)))
        for f in self._FIELDS.keys():
            ok = self.field_conditions_test(f)
            if ok:
                value = self.get_value(f, None)
                if value is not None:
                    field = self._FIELDS[f]
                    values = field['values']
                    v_type = values[0]
                    if v_type == 'list':
                        if symbolic:
                            # map to a user readable value
                            list_values = values[1]
                            int_values = list_values['values']
                            id_values = list_values['ids']
                            try:
                                index = int_values.index(value)
                            except ValueError:
                                self.log('can\'t find %s in %s' % (str(value), str(int_values)))
                            else:
                                value = id_values[index]
                    self.log('%s : %s' % (f, str(value)))
                    data[f] = value 
                else:
                    self.log('for some reason, field %s is None' % f)
        return data

    def __to_json__(self):
        return self.__internal_json__(True)

    # ========================================================================
    #
    # getters, setters and deleters
    #
    # ========================================================================

    def get_value(self, key, default):
        return self._values.get(key, default)

    def set_value(self, key, value):
        if key == VAR_PARAMS_KEY:
            return False
        self._values[key] = value

    def del_value(self, key):
        if key == VAR_PARAMS_KEY:
            return False
        if key in self._values:
            del(self._values[key])
        return True

    def check_param_key(self, key):
        if isinstance(key, int):
            return key
        if isinstance(key, str):
            if key.isnumeric():
                return int(key)
        raise AttributeError

    def get_param(self, key, default):
        i_key = self.check_param_key(key)
        return self._params.get(i_key, default)

    def set_param(self, key, value):
        i_key = self.check_param_key(key)
        self._params[i_key] = value

    def del_param(self, key):
        i_key = self.check_param_key(key)
        if i_key in self._params:
            del(self._params, i_key)

    # ========================================================================
    #
    # config-reactor functions
    #
    # ========================================================================

    def res_ko_value(self, keyo, state):
        self.set_value(F_KO, keyo)
        #self.set_value(F_STATE, state)
        return True

    def res_ko_sys(self, sys, addr):
        # hah, can't handle addresses all the same way, they are parsed differently
        # between systems !!
        self.set_value(F_SYSTEM, sys)
        self.set_check_value(F_SYS_ADDRESS, addr)
        self.log('>>>>>>>>>>> RES_KO_SYS sys: %s addr: %s <<<<<<<<<<<' 
                 % (sys, str(self.get_value(F_SYS_ADDRESS, addr))))
        return True

    def res_param_ko(self, index, val_par):
        found, ok, fields = self.find_field(index)
        self.log('PARAM %s %s %s => %s' % (str(index), str(found), str(fields), str(val_par)))
        if found:
            if ok:
                if not isinstance(fields, str):
                    self.log('%s.res_param_ko: ERROR: expected a field name, got %s \'%s\'' % 
                             (self.__class__.__name__, fields.__class__.__name__, str(fields)))
                else:
                    self.log('%s.res_param_ko: found %s' % (self.__class__.__name__, fields))
                    field_name = fields
                    field = self._FIELDS[field_name]
                    self.log(field)
                    param = field['param']
                    # those validity tests should not be necessary
                    if isinstance(param, int):
                        if param == index:
                            self.log('%s => %s' % (field_name, str(val_par)))
                            return self.set_check_value(field_name, val_par)
                        else:
                            # should never happen...
                            self.log('%s.res_param_ko: ERROR: For some reason, param changed param: %s index: %s' % 
                                     (self.__class__.__name__, str(param), str(index)))
                    elif isinstance(param, dict):
                        if index in param.keys():
                            action = param[index]
                            if action == 'low_8':
                                val = self.get_value(field_name, 0)
                                value = (val & 0xff00) | (val_par & 0xff)
                                self.log('%s: %08x %08x => %08x' % (action, val, val_par, value))
                                return self.set_check_value(field_name, value) 
                            elif action == 'high_8':
                                val = self.get_value(field_name, 0)
                                value = ((val_par << 8) & 0xff00) | (val & 0xff)
                                self.log('%s: %08x %08x => %08x' % (action, val, val_par, value))
                                return self.set_check_value(field_name, value)
                            else:
                                self.log('%s.res_param_ko: ERROR: unknown action %s' % 
                                     (self.__class__.__name__, str(action)))
                        else:
                            # should never happen either !
                            self.log('%s.res_param_ko: ERROR: For some reason, index is not in index: %s param: %s' % 
                                     (self.__class__.__name__, str(index), str(param)))
                    return True
            else:
                self.log('%s.res_param_ko: WARNING: none of %s validated conditions' % (self.__class__.__name__, str(fields))) 
                return True   
        else:
            self.log('%s.res_param_ko: WARNING: unable to find field for param %s' % (self.__class__.__name__, str(index)))
        return False
