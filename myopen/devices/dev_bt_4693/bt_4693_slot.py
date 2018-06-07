# -*- coding: utf-8 -*-
from core.logger import LOG_ERROR, LOG_DEBUG

from ..baseslot import F_KO, F_SYS_ADDRESS, BaseSlot
from ..dev_utils import split_long_addr

KO_UNCONFIGURED = 221  # houston, we have a problem !
KO_MASTER_PROBE = 184
KO_SLAVE_PROBE = 221

KOS = {
    'values': [KO_MASTER_PROBE, KO_SLAVE_PROBE],
    'ids': ['MASTER_PROBE', 'SLAVE_PROBE'],
    'names': ['Master probe', 'Slave probe']
}

FIELDS = {
    F_KO: {
        'param': F_KO,
        'values': ['list', KOS],
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
