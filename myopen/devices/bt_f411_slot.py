# -*- coding: utf-8 -*-
from core.logger import LOG_ERROR

from ..constants import (SLOT_VAR_A, SLOT_VAR_ADDR, SLOT_VAR_GROUPS,
                         SLOT_VAR_MODE, SLOT_VAR_PL, SLOT_VAR_STATE,
                         SLOT_VAR_SYS, VAR_PARAMS_KEY)
from .baseslot import BaseSlot
from .dev_utils import split_long_addr


class DeviceF411_Slot(BaseSlot):
    MODE_UNCONFIGURED = 0
    MODE_LIGHT_ACTUATOR = 1
    MODE_AUTOMATION_ACTUATOR = 2
    KOS = (510, 6, 7)
    MODE_IDS = ('UNCONFIGURED', 'LIGHT_CONTROL', 'AUTOMATION_CONTROL',)
    MODE_NAMES = ('Unconfigured', 'Light control', 'Automation control',)

    GROUP_INVALID = 0
    GROUP_MIN = 1
    GROUP_MAX = 255
    GROUP_MIN_IDX = 240
    GROUP_MAX_IDX = 249
    GROUPS_NB = 0
    GROUP_IDX_RANGE = None
    GROUPS_RANGE = None

    def __init__(self, slots):
        super().__init__(slots)
        self.GROUPS_NB = self.GROUP_MAX_IDX - self.GROUP_MIN_IDX + 1
        self.GROUP_IDX_RANGE = range(self.GROUP_MIN_IDX, self.GROUP_MAX_IDX + 1)
        self.GROUPS_RANGE = range(self.GROUP_MIN, self.GROUP_MAX + 1)
        self.groups = [None]*(self.GROUPS_NB)

    # ========================================================================
    #
    # slot-specific helper functions
    #
    # ========================================================================

    def set_group(self, group_idx, group):
        self.groups[group_idx] = group

    # ========================================================================
    #
    # json loading function
    #
    # ========================================================================

    def loads(self, data):
        mode = self.get_mode(data)
        if mode is None:
            return False
        self.set_value(SLOT_VAR_MODE, mode)      

        sys = data.get(SLOT_VAR_SYS, None)
        if sys is None:
            return False
        self.set_value(SLOT_VAR_SYS, sys)

        addr = data.get(SLOT_VAR_ADDR, None)
        if addr is not None:
            a, pl = split_long_addr(addr)
            if a is None or pl is None:
                addr = None
        if addr is None:
            a = data.get(SLOT_VAR_A, None)
            pl = data.get(SLOT_VAR_PL, None)
            if a is None or pl is None:
                return False
        self.set_value(SLOT_VAR_A, a)
        self.set_value(SLOT_VAR_PL, pl)

        groups = data.get(SLOT_VAR_GROUPS, None)
        if groups is None:
            return False
        if not isinstance(groups, list):
            return False
        if len(groups) != self.GROUPS_NB:
            return False
        for index in range(0, self.GROUPS_NB):
            group = groups[index]
            if group is not None and group not in self.GROUPS_RANGE:
                self.log('group %s invalid' % group, LOG_ERROR)
                return False
            self.set_group(index, group)

        params = data.get(VAR_PARAMS_KEY, data)
        if params is not None:
            self.load_params(data, params)

        return True

    # ========================================================================
    #
    # json generating
    #
    # ========================================================================

    def json_mode(self, data):
        mode = self.get_value(SLOT_VAR_MODE, None)
        self.log('DeviceF411_slot.json_mode : found mode %s in %s'
                 % (str(mode), str(self._values)), LOG_ERROR)
        if mode is not None:
            self.log('DeviceF411_slot.json_mode : mode is not none', LOG_ERROR)
            data[SLOT_VAR_MODE] = self.MODE_IDS[mode]
        self.log('DeviceF411_slot.json_mode : returning %d' % mode, LOG_ERROR)
        return mode

    def json_addr(self, data):
        addr = self.get_value(SLOT_VAR_ADDR, None)
        if addr is not None:
            a, pl = split_long_addr(addr)
            data[SLOT_VAR_A] = a
            data[SLOT_VAR_PL] = pl
        else:
            a = self.get_value(SLOT_VAR_A, None)
            pl = self.get_value(SLOT_VAR_PL, None)
            if a is not None and pl is not None:
                data[SLOT_VAR_A] = a
                data[SLOT_VAR_PL] = pl
                addr = True
        return addr

    def __to_json__(self):
        data = super().__to_json__()
        data['_source'] = super().__class__.__name__
        _data = {}
        mode = self.json_mode(_data)
        self.log('DeviceF411_Slot:__to_json__ : mode = %s' % str(mode), LOG_ERROR)
        if mode is None:
            self.log('DeviceF411_Slot:__to_json__ : mode is None', LOG_ERROR)
            return data
        if mode != self.MODE_UNCONFIGURED:
            sys = self.json_set_var(SLOT_VAR_SYS, _data)
            if sys is None:
                self.log('DeviceF411_Slot:__to_json__ : sys is None', LOG_ERROR)
                return data
            addr = self.json_addr(_data)
            if addr is None:
                self.log('DeviceF411_Slot:__to_json__ : addr is None', LOG_ERROR)
                return data
            _data[SLOT_VAR_GROUPS] = self.groups
            self.log('DeviceF411_Slot:__to_json__ : groups is %s' % (str(self.groups)), LOG_ERROR)
        if len(self._params) > 0:
            _data[VAR_PARAMS_KEY] = self._params
        return _data

    # ========================================================================
    #
    # config-reactor functions
    #
    # ========================================================================

    def res_ko_value(self, keyo, state):
        mode = self.get_mode_from_keyo(keyo)
        if mode is None:
            self.log('DeviceF411_Slot.res_ko_value ERROR: '
                     'keyo %s => mode %s' % (str(keyo), str(mode)),
                     LOG_ERROR)
        self.set_value(SLOT_VAR_MODE, mode)
        if mode != self.MODE_UNCONFIGURED and state == 1 or \
           mode == self.MODE_UNCONFIGURED and state == 0:
            # should not happen
            self.log('DeviceF411_Slot.res_ko_value ERROR: '
                     'mode %d and state %d don\'t match'
                     % (mode, state), LOG_ERROR)
            self.set_value(SLOT_VAR_STATE, state)
        return True

    def res_param_ko(self, index, val_par):
        mode = self.get_value(SLOT_VAR_MODE, None)
        if mode is not None:
            if mode == self.MODE_LIGHT_ACTUATOR:
                pass
            if mode == self.MODE_AUTOMATION_ACTUATOR:
                pass
        # there are groups for all modes
        if index in self.GROUP_IDX_RANGE:
            group_idx = index - self.GROUP_MIN_IDX
            group = val_par
            if group == self.GROUP_INVALID:
                group = None
            elif group not in self.GROUPS_RANGE:
                group = None
            self.set_group(group_idx, group)
            return True
        self.set_param(index, val_par)
        return True
