# -*- coding: utf-8 -*-
from .subsystem import OWNSubSystem


class DiagGateway(OWNSubSystem):
    SYSTEM_NAME = "DIAG_GATEWAY"
    SYSTEM_WHO = 1013
    SYSTEM_DIAG_WHO = 13
