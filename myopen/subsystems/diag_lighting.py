# -*- coding: utf-8 -*-
from .subsystem import OWNSubSystem


class DiagLighting(OWNSubSystem):
    SYSTEM_WHO = 1001
    SYSTEM_DIAG_WHO = 1
    SYSTEM_IS_SCANNABLE = True

    SYSTEM_REGEXPS = {
        'STATUS': [
            # device diagnostics
            # see notes.txt
            (r'^\*(?P<virt_id>\d{1,4})\*11\*(?P<diag_bits>[01]{24})##$', '_analyze_diagnostics', ),
            # when scanning a system for devices, obtain the hardware address of
            # each device on the bus.
            (r'^\*(?P<virt_id>\d{1,4})\*13\*(?P<hw_addr>\d{1,10})##$', '_register_light_device', )
        ]
    }

    def _analyze_diagnostics(self, matches):
        self.log('DiagLighting dev diags : %s' % str(matches))
        return True

    def _register_light_device(self, matches):
        self.system.devices.register(self, matches)
        return True