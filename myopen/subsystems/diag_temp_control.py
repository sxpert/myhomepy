# -*- coding: utf-8 -*-
from .subsystem import OWNSubSystem


class DiagTempControl(OWNSubSystem):
    SYSTEM_WHO = 1004
    SYSTEM_DIAG_WHO = 4
    SYSTEM_IS_SCANNABLE = True