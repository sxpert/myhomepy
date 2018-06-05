# -*- coding: utf-8 -*-
from core.logger import LOG_ERROR, LOG_DEBUG

from ...constants import (SLOT_VAR_A, SLOT_VAR_ADDR, SLOT_VAR_GROUPS,
                         SLOT_VAR_MODE, SLOT_VAR_PL, SLOT_VAR_STATE,
                         SLOT_VAR_SYS, VAR_PARAMS_KEY)
from ..baseslot import F_KO, F_SYS_ADDRESS, BaseSlot
from ..dev_utils import split_long_addr

KO_UNCONFIGURED = 510
KO_LIGHT_ACTUATOR = 6
KO_AUTOMATION_ACTUATOR = 7

KOS = {
    'values': [KO_UNCONFIGURED, KO_LIGHT_ACTUATOR, KO_AUTOMATION_ACTUATOR],
    'ids': ['UNCONFIGURED', 'LIGHT_ACTUATOR', 'AUTOMATION_ACTUACTOR'],
    'names': ['Unconfigured', 'Light actuator', 'Automation actuator']
}

LA_MASTER = 0
LA_SLAVE = 11
LA_MASTER_PUL = 15
LA_SLAVE_AND_PUL = 16

LIGHT_ACTUATOR = {
    'values': [LA_MASTER, LA_SLAVE, LA_MASTER_PUL, LA_SLAVE_AND_PUL],
    'ids': ['LA_MASTER', 'LA_SLAVE', 'LA_MASTER_PUL', 'LA_SLAVE_AND_PUL'],
    'names': ['Master', 'Slave', 'Master momentary', 'Slave and momentary']
}

GROUP_INVALID = 0
GROUP_MIN = 1
GROUP_MAX = 255
GROUP_MIN_IDX = 240
GROUP_MAX_IDX = 249
GROUPS_NB = GROUP_MAX_IDX - GROUP_MIN_IDX + 1
GROUP_IDX_RANGE = range(GROUP_MIN_IDX, GROUP_MAX_IDX + 1)
GROUPS_RANGE = range(GROUP_MIN, GROUP_MAX + 1)

F_LIGHT_ACTUATOR = 'light_actuator'

FIELDS = {
    F_KO: {
        'param': F_KO,
        'values': ['list', KOS],
        'disp': {'label': 'Operating mode', 'order': 0}
    },
    F_LIGHT_ACTUATOR: {
        'param': 0,
        'values': ['list', LIGHT_ACTUATOR],
        'cond': ('==', F_KO, KO_LIGHT_ACTUATOR),
        'disp': {'label': 'Light actuator mode', 'order': 1}
    },
    F_SYS_ADDRESS: {
        'param': F_SYS_ADDRESS,
        'values': ['address', 'string'],
        'cond': ['in', F_KO, [KO_LIGHT_ACTUATOR, KO_AUTOMATION_ACTUATOR]],
        'disp': {'label': 'Address', 'order': 2}
    }
}

class DeviceF411_Slot(BaseSlot):
    FIELDS = FIELDS
