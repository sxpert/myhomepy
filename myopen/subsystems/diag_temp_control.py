# -*- coding: utf-8 -*-
from .diag_scannable import DiagScannable


class DiagTempControl(DiagScannable):
    SYSTEM_NAME = 'DIAG_TEMP_CONTROL'
    SYSTEM_WHO = 1004
    SYSTEM_DIAG_WHO = 4

    # ---------------------------------------------------------------------
    #
    # address parsing
    #
    def parse_address_sys(self, addr):
        self.log("parse_address_sys")


    