# -*- coding: utf-8 -*-
from ..constants import (
    SLOT_VAR_ADDR, SLOT_VAR_KEYO, SLOT_VAR_MODE,
    SLOT_VAR_STATE, SLOT_VAR_SYS, 
    VAR_KOS, VAR_MODE_IDS, VAR_PARAMS_KEY, )
from .dev_utils import map_value
from core.logger import LOG_ERROR 
from myopen.device_db import device_db

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
        self._tmp_values = None
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
    def kos_for_slot(self):
        dev = self._slots.parent
        who = dev.subsystem.SYSTEM_WHO
        kos = device_db.find_kos_for_device(who, dev.model_id, dev.fw_version)
        values = []
        widths = []
        ids = []
        names = []
        for ko in kos:
            ko_data = device_db.get_ko_details(ko)
            if ko_data is not None:
                w, i, n = ko_data
                # skip those that would be too wide
                if self.number + w <= len(dev.slots):
                    values.append(ko)
                    widths.append(w)
                    ids.append(i)
                    names.append(n)
        return {
            'values': values,
            'widths': widths,
            'ids': ids,
            'names': names
        }

    @property
    def slot_options(self):
        kos = self.kos_for_slot
        ko_values = kos['values']
        integers = {}
        conds = {}
        fields = {}
        lists = {}
        for ko in ko_values:
            index = ko_values.index(ko)
            params = device_db.get_params_for_ko(ko)
            # gets lists and conditions
            for p in params:
                cond = p['cond']
                if cond is not None:
                    c = device_db.get_condition_details(cond)
                    conds.update(c)
                field_type = p['field_type']
                if field_type == 'INTEGER':
                    field_type_detail = p['field_type_detail']
                    integer_details = device_db.get_integer_details(field_type_detail)
                    integers[field_type_detail] = integer_details
                if field_type == 'LIST':
                    field_type_detail = p['field_type_detail']
                    list_details = device_db.get_list_details(field_type_detail)
                    lists[field_type_detail] = list_details
            ko_id = kos['ids'][index]
            fields[ko_id] = params
        options = {}
        options['conds'] = conds
        options['fields'] = fields
        options['integers'] = integers
        options['kos'] = kos
        options['lists'] = lists
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
            # KO should be a symbol
            if ko not in kos:
                device_db.log("BaseSlot.loads ERROR: invalid KO %s for object" % str(ko))
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
                access_mode, field_type, field_type_detail = field
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
                if access_mode == 'array':
                    for i in range(0, len(value)):
                        if value[i] is None:
                            # none is an acceptable value in arrays
                            continue
                        o, v = device_db.parse_value(value[i], field_type, field_type_detail)
                        if not o: 
                            self.log('BasicSlot.loads WARNING: invalid value \'%s\' for %s[%d]' % (value[i], var_name, i))
                        ok = ok and o
                else:
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
                        _, field_type, field_type_detail = field
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

    def get_value(self, key, default, values=None):
        if values is None:
            values = self._values
        return values.get(key, default)

    def set_value(self, key, value, values=None):
        if values is None:
            values = self._values
        values[key] = value
        device_db.log(values)
        return True

    def del_value(self, key, values=None):
        if values is None:
            values = self._values
        if key in values:
            del(values[key])
        return True

    # ========================================================================
    #
    # config-reactor functions
    #
    # ========================================================================

    def cmd_reset_ko(self):
        if self._tmp_values is None:
            self._tmp_values = {}
        else:
            self.log("BaseSlot.cmd_reset_ko ERROR: _tmp_values was not empty %s" % (self._tmp_values))
        return True

    def res_conf_ok(self):
        self.log('BaseSlot.res_conf_ok: %s' % (str(self._tmp_values)), LOG_ERROR)
        self._values = self._tmp_values
        self._tmp_values = None
        return True

    def do_ko_value(self, keyo, state):
        dev = self._slots.parent
        who = dev.subsystem.SYSTEM_WHO
        kos = device_db.find_kos_for_device(who, dev.model_id, dev.fw_version)
        if keyo in kos:
            return keyo
        self.log("BaseSlot.do_ko_value ERROR: invalid KO for object %s" % (str(keyo)))
        return None

    def res_ko_value(self, keyo, state):
        keyo = self.do_ko_value(keyo, state)
        if keyo is not None:
            return self.set_value(F_KO, keyo)
        self.log("BaseSlot.res_ko_value ERROR: WTF KO is  '%s' ??" % (str(keyo)), LOG_ERROR)
        return False

    def cmd_ko_value(self, keyo):
        keyo = self.do_ko_value(keyo, 0)
        if keyo is not None:
            return self.set_value(F_KO, keyo, self._tmp_values)
        self.log("BaseSlot.cmd_ko_value ERROR: WTF KO is  '%s' ??" % (str(keyo)), LOG_ERROR)
        return False

    def do_ko_sys(self, sys, addr):
        # hah, can't handle addresses all the same way, they are parsed differently
        # between systems !!
        dev = self._slots.parent
        who = dev.subsystem.SYSTEM_WHO
        if sys != who:
            self.log("ERROR: sys is different from SYSTEM_WHO %d != %d" % (sys, who), LOG_ERROR)
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
        return (ok, var_name, value,)

    def res_ko_sys(self, sys, addr):
        ok, var_name, value = self.do_ko_sys(sys, addr)
        if ok:
            return self.set_value(var_name, value)
        device_db.log("res_ko_sys: Unable to set %s => %s" % (var_name, str(value)))
        device_db.log(self._values)
        return False

    def cmd_ko_sys(self, sys, addr):
        ok, var_name, value = self.do_ko_sys(sys, addr)
        if ok:
            return self.set_value(var_name, value, self._tmp_values)
        device_db.log("cmd_ko_sys: Unable to set %s => %s" % (var_name, str(value)))
        return False

    def do_param_ko(self, index, val_par, _get_value=None):
        if _get_value is None:
            _get_value = self.get_value
        var_name = None
        value = None

        # value for F_KO should never be None here !
        field = device_db.find_field(_get_value(F_KO, None), index, _get_value)
        if field is not None:
            access_mode, field_type, field_type_detail, var_name, array_index = field
            # should check value
            ok, value = device_db.parse_value(val_par, field_type, field_type_detail)
            if ok is not None:
                if access_mode == 'array':
                    try:
                        val = _get_value(var_name, [])
                        while len(val) <= array_index:
                            val.append(None)
                        val[array_index] = value
                        value = val
                    except:
                        import traceback
                        traceback.print_exc()
                elif access_mode == 'bool_invert':
                    if value is not None:
                        value = not value
                elif access_mode == 'low_8':
                    if value is not None:
                        val = _get_value(var_name, 0)
                        value = (val & 0xff00) | (value & 0xff)
                elif access_mode == 'high_8':
                    if value is not None:
                        val = _get_value(var_name, 0)
                        value = ((value << 8) & 0xff00) | (val & 0xff)
                elif access_mode == 'value':
                    pass
                else:
                    # more complicated modes
                    device_db.log('UNIMPLEMENTED: %s %s' % (str(field), str(value)))
            else:
                device_db.log("ERROR: value returned is None")
        return (var_name, value)

    def res_param_ko(self, index, value):
        var_name, value = self.do_param_ko(index, value)
        if var_name is not None and value is not None:
            return self.set_value(var_name, value)
        return False

    def cmd_param_ko(self, index, value):
        def _get_value(var_name, default_value):
            return self.get_value(var_name, default_value, self._tmp_values)
        var_name, value = self.do_param_ko(index, value, _get_value)
        if var_name is not None and value is not None:
            return self.set_value(var_name, value, self._tmp_values)
        return False
