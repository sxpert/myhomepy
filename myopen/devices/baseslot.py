# -*- coding: utf-8 -*-
from ..constants import (
    SLOT_VAR_ADDR, SLOT_VAR_KEYO, SLOT_VAR_MODE,
    SLOT_VAR_STATE, SLOT_VAR_SYS, 
    VAR_KOS, VAR_MODE_IDS, VAR_PARAMS_KEY, )
from .dev_utils import map_value
from core.logger import LOG_ERROR 
from myopen.conf_db import device_db

__all__ = ['F_KO', 'MissingFieldsDefinitionError', 'BaseSlot', ]

F_KO = 'KO'
F_EMPTY = '_empty'


class MissingFieldsDefinitionError(Exception):
    pass


class BaseSlot(object):
    log = None

    def __init__(self, slots):
        self.log = slots.log
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
    # front-end related
    #
    # ========================================================================

    @property
    def slot_options(self):
        options = {
            # 'fields': self._FIELDS
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
        if not isinstance(data, dict):
            device_db.log("BaseSlot.loads ERROR: data must be a dict")
            return False
        keys = data.keys()
        if len(keys) == 0:
            device_db.log("BaseSlot.loads WARNING: we're missing info for slot %d" % (self.number))
            device_db.log(self._slots.parent)
            device_db.log(data)
            return False
        ko = data.get(F_KO, None)
        if ko is None:
            # we don't have a ko, slot is probably empty
            empty = data.get(F_EMPTY, None)
            if empty is None:
                device_db.log("BaseSlot.loads ERROR: there should be an '%s' value in this case" % (F_EMPTY))
                return False
            if empty != True:
                device_db.log("BaseSlot.loads ERROR: %s should be True" % (F_EMPTY))
                return False
            self.set_value(F_EMPTY, empty)
        else:
            dev = self._slots.parent
            who = dev.subsystem.SYSTEM_WHO
            kos = device_db.find_symbolic_kos_for_device(who, dev.model_id, dev.fw_version)
            if ko not in kos:
                device_db.log("BaseSlot.loads ERROR: invalid KO %d for object" % ko)
                return False
            ko_value, width = kos[ko]    
            if self.number + width > len(dev.slots):
                device_db.log("BaseSlot.loads ERROR: KO %d is too wide (%d) to be set on slot %d" % (ko_value, width, self.number))
                return False
            self.set_value(F_KO, ko_value)

            fields = device_db.find_fields_for_ko(ko_value)
            for v in fields:
                var_name, var_old = v
                field = device_db.find_named_field(ko_value, var_name, self.get_value)
                if field is None:
                    # this field is not valid at this point
                    continue
                field_type, field_type_detail = field
                ok = False
                # try var_old first
                if var_old is not None:
                    if var_old in keys:
                        value = data.get(var_old, None)
                        ok = True
                # try var_name next
                if not ok:
                    if var_name in keys:
                        value = data.get(var_name, None)
                        ok = True
                # unable to find variable...
                if not ok:
                    value = None
                    device_db.log("BasicSlot.loads WARNING: unable to find a value for %s" % (var_name))
                    # skip to next field name
                    continue
                if value is None:
                    # skip...
                    continue
                ok, value = device_db.parse_value(value, field_type, field_type_detail)
                if ok:
                    self.set_value(var_name, value)

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

        empty = self.get_value(F_EMPTY, None)
        if empty:
            data[F_EMPTY] = empty
        else:
            ko_value = self.get_value(F_KO, None)
            if ko_value is None:
                device_db.log("__internal_json__ ERROR: can't find a KO value and %s is not set" % (F_EMPTY))
            else:
                ko_id = device_db.find_symbolic_ko_value(ko_value)
                data[F_KO] = ko_id
                fields = device_db.find_fields_for_ko(ko_value)
                for f in fields:
                    field_name, _ = f
                    field = device_db.find_named_field(ko_value, field_name, self.get_value)
                    if field is not None:
                        field_type, field_type_detail = field
                        value = self.get_value(field_name, None)
                        ok, value = device_db.export_value(value, field_type, field_type_detail)
                        if ok:
                            data[field_name] = value
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
        dev = self._slots.parent
        who = dev.subsystem.SYSTEM_WHO
        kos = device_db.find_kos_for_device(who, dev.model_id, dev.fw_version)
        if keyo in kos:
            self.set_value(F_KO, keyo)
        else: 
            # should not happen ;-)
            self.log("ERROR: invalid KO for object")
        return True

    def res_ko_sys(self, sys, addr):
        # hah, can't handle addresses all the same way, they are parsed differently
        # between systems !!
        dev = self._slots.parent
        who = dev.subsystem.SYSTEM_WHO
        if sys != who:
            self.log("ERROR: sys is different from SYSTEM_WHO %d != %d" % (sys, who))
            # not worth bailing though...
        # not sure this is any useful !
        # get the addr record 
        # note: ko => None should not happen
        addr_rec = device_db.find_sys_addr(self.get_value(F_KO, None))
        if addr_rec is None:
            # bail
            return False
        _, _, _, field_type, field_type_detail, var_name, _ = addr_rec
        ok, value = device_db.parse_value(addr, field_type, field_type_detail)
        if ok:
            self.set_value(var_name, value)
        else:
            device_db.log("res_ko_sys: Unable to set %s => %s" % (var_name, str(value)))
        device_db.log(self._values)
        return True

    def res_param_ko(self, index, val_par):
        # value for F_KO should never be None here !
        field = device_db.find_field(self.get_value(F_KO, None), index, self.get_value)
        if field is not None:
            access_mode, field_type, field_type_detail, var_name, array_index = field
            # should check value
            ok, value = device_db.parse_value(val_par, field_type, field_type_detail)
            if ok is not None:
                if access_mode == 'array':
                    try:
                        val = self.get_value(var_name, [])
                        while len(val) <= array_index:
                            val.append(None)
                        val[array_index] = value
                        self.set_value(var_name, val)
                    except:
                        import traceback
                        traceback.print_exc()
                elif access_mode == 'bool_invert':
                    if value is not None:
                        self.set_value(var_name, not value)
                elif access_mode == 'low_8':
                    if value is not None:
                        val = self.get_value(var_name, 0)
                        n_value = (val & 0xff00) | (value & 0xff)
                        self.set_value(var_name, n_value) 
                elif access_mode == 'high_8':
                    if value is not None:
                        val = self.get_value(var_name, 0)
                        n_value = ((value << 8) & 0xff00) | (val & 0xff)
                        self.set_value(var_name, n_value)
                elif access_mode == 'value':
                    if value is not None:
                        self.set_value(var_name, value)
                else:
                    # more complicated modes
                    device_db.log('UNIMPLEMENTED: %s %s' % (str(field), str(value)))
            else:
                device_db.log("ERROR: value returned is None")
        device_db.log(self._values)
        return True