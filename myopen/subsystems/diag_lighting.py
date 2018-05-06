# -*- coding: utf-8 -*-
from .subsystem import OWNSubSystem


class DiagLighting(OWNSubSystem):
    SYSTEM_WHO = 1001
    SYSTEM_DIAG_WHO = 1
    SYSTEM_IS_SCANNABLE = True
