# -*- coding: utf-8 -*-
from ..constants import *
from .dev_utils import *
from .baseslot import BaseSlot


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

    def __init__(self):
        super().__init__()
        self._groups = [None]*(self.GROUP_MAX_IDX - self.GROUP_MIN_IDX + 1)

    # ========================================================================
    #
    # slot-specific helper functions
    #
    # ========================================================================

    def set_group(self, group_idx, group):
        self._groups[group_idx] = group

    # ========================================================================
    #
    # json loading function
    #
    # ========================================================================

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

    def json_addr(self, data):
        addr = self.get_value(SLOT_VAR_ADDR, None)
        if addr is not None:
            a, pl = split_long_addr(addr)
            data[SLOT_VAR_A] = a
            data[SLOT_VAR_PL] = pl
        return addr

    def __to_json__(self):
        data = super().__to_json__()
        data['_source'] = super().__class__.__name__
        _data = {}
        mode = self.json_mode(_data)
        if mode is None:
            return data
        sys = self.json_set_var(SLOT_VAR_SYS, _data)
        if sys is None:
            return data
        addr = self.json_addr(_data)
        if addr is None:
            return data
        _data[SLOT_VAR_GROUPS] = self._groups
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
        self.set_value(SLOT_VAR_MODE, mode)
        if mode != self.MODE_UNCONFIGURED and state == 1 or \
           mode == self.MODE_UNCONFIGURED and state == 0:
            # should not happen
            self.log('DeviceF411_Slot.res_ko_value ERROR: '
                     'mode %d and state %d don\'t match'
                     % (mode, state))
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
        if index >= self.GROUP_MIN_IDX and index <= self.GROUP_MAX_IDX:
            group_idx = index - self.GROUP_MIN_IDX
            group = val_par
            if group == self.GROUP_INVALID:
                group = None
            elif group < self.GROUP_MIN or group > self.GROUP_MAX:
                group = None
            self.set_group(group_idx, group)
            return True
        self.set_param(index, val_par)
        return True
