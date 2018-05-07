# -*- coding: utf-8 -*-
from .subsystem import OWNSubSystem


class DiagTempControl(OWNSubSystem):
    SYSTEM_WHO = 1004
    SYSTEM_DIAG_WHO = 4
    SYSTEM_IS_SCANNABLE = True

    SYSTEM_REGEXPS = {
        'STATUS': [
            (r'^\*(?P<virt_id>\d{1,4})\*13\*(?P<hw_addr>\d{1,10})##$', '_register_temp_control_device')
        ]
    }

    def _register_temp_control_device(self, matches):
        self.system.devices.register(self, matches)
        return True