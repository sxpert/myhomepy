# -*- coding: utf-8 -*-
from ..constants import (
    SLOT_VAR_ADDR, SLOT_VAR_KEYO, SLOT_VAR_MODE,
    SLOT_VAR_STATE, SLOT_VAR_SYS, 
    VAR_KOS, VAR_MODE_IDS, VAR_PARAMS_KEY, )
from .dev_utils import map_value
from core.logger import LOG_ERROR

__all__ = ['BaseSlot']


class BaseSlot(object):
    log = None

    def __init__(self, slots):
        self._slots = slots
        self.log = slots.log
        self._values = {}
        self._params = {}

    def __str__(self):
        print(self._values, self._params)
        s = '<%s' % self.__class__.__name__
        for k, v in self._values.items():
            s += ' (%s: %s)' % (str(k), str(v))
        s += ' params{'
        for k, v in self._params.items():
            s += ' (%s: %s)' % (str(k), str(v))
        s += '}>'
        return s

    # ========================================================================
    #
    # json loading and generating functions
    #
    # ========================================================================

    def get_mode_from_keyo(self, keyo):
        mode = None
        if keyo is not None:
            KOS = getattr(self, VAR_KOS, None)
            if KOS is None:
                self.log('BaseSlot ERROR : '
                         '%s not defined in class'
                         % (VAR_KOS), LOG_ERROR)
                return None
            if keyo in KOS:
                mode = KOS.index(keyo)
            else:
                self.log('BaseSlot ERROR : '
                         'keyo %d unknown %s'
                         % (keyo, str(KOS)),
                         LOG_ERROR)
        return mode

    def get_mode(self, data):
        MODE_IDS = getattr(self, VAR_MODE_IDS, None)
        if MODE_IDS is None:
            self.log('BaseSlot ERROR: No %s in %s' %
                        (VAR_MODE_IDS, self.__class__.__name__))
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
                    m = map_value(m, MODE_IDS)
            if isinstance(m, int):
                if m in range(0, len(MODE_IDS)):
                    mode = m
        if mode is None:
            self.log('BaseSlot ERROR: '
                     'unable to read mode value',
                     LOG_ERROR)
        return mode

    def loads(self, data):
        if not isinstance(data, dict):
            return False
        for k, v in data.items():
            print(k, v)
            if k == VAR_PARAMS_KEY:
                if not isinstance(v, dict):
                    self.log('%s should be a dict in %s'
                             % (VAR_PARAMS_KEY, str(data)),
                             LOG_ERROR)
                    continue
                for pk, pv in v.items():
                    self.set_param(pk, pv)
            else:
                self.set_value(k, v)
        return True

    def json_set_var(self, var, data):
        val = self.get_value(var, None)
        if val is not None:
            data[var] = val
        return val

    def __to_json__(self):
        data = self._values
        if len(self._params) > 0:
            data[VAR_PARAMS_KEY] = self._params
        return data

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
        self.set_value(SLOT_VAR_KEYO, keyo)
        self.set_value(SLOT_VAR_STATE, state)
        return True

    def res_ko_sys(self, sys, addr):
        self.set_value(SLOT_VAR_SYS, sys)
        self.set_value(SLOT_VAR_ADDR, addr)
        return True

    def res_param_ko(self, index, val_par):
        self.set_param(index, val_par)
        return True
