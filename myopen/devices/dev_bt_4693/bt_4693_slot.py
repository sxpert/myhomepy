# -*- coding: utf-8 -*-
from core.logger import LOG_ERROR, LOG_DEBUG

from ..baseslot import F_KO, F_SYS_ADDRESS, BaseSlot
from ..dev_utils import split_long_addr

KO_UNCONFIGURED = 508  # note: MyHomeSuite doesn't seem to use this !
KO_TEMP_CONTROL_PROBE = 36  # note: for firmware 5.2.0 
KO_MASTER_PROBE = 184  # note: for firmware 6.0.0
KO_SLAVE_PROBE = 221

KOS_FW_5_2_0 = {
    'values': [KO_UNCONFIGURED, KO_TEMP_CONTROL_PROBE, KO_SLAVE_PROBE],
    'ids': ['UNCONFIGURED', 'TEMP_CONTROL_PROBE', 'SLAVE_PROBE'],
    'names': ['Unconfigured', 'Temperature control probe', 'Slave probe']
}

KOS_FW_6_0_0 = {
    'values': [KO_UNCONFIGURED, KO_MASTER_PROBE, KO_SLAVE_PROBE],
    'ids': ['UNCONFIGURED', 'MASTER_PROBE', 'SLAVE_PROBE'],
    'names': ['Unconfigured', 'Master probe', 'Slave probe']
}

FIELDS = {
    F_KO: {
        'param': F_KO,
        'values': ['list', KOS_FW_6_0_0],
        'disp': {'label': 'Operating mode', 'order': 0}
    },
    F_SYS_ADDRESS: {
        'param': F_SYS_ADDRESS,
        'values': ['address', 'slave'],
        'cond': ['in', F_KO, [KO_SLAVE_PROBE]],
        'disp': {'label': 'Address', 'order': 2}
    }
}


class Device4693_Slot(BaseSlot):
    FIELDS = FIELDS
