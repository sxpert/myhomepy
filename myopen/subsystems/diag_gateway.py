# -*- coding: utf-8 -*-
from .subsystem import OWNSubSystem


class DiagGateway(OWNSubSystem):
    SYSTEM_WHO = 1013
    SYSTEM_DIAG_WHO = 13
