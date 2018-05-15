# -*- coding: utf-8 -*-
from .diag_scannable import DiagScannable


class DiagLighting(DiagScannable):
    SYSTEM_NAME = 'DIAG_LIGHTING'
    SYSTEM_WHO = 1001
    SYSTEM_DIAG_WHO = 1

    def _analyze_diagnostics(self, matches):
        self.log('DiagLighting dev diags : %s' % str(matches))
        return True
