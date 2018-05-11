# -*- coding: utf-8 -*-
from .subsystem import OWNSubSystem


class DiagScannable(OWNSubSystem):
    SYSTEM_IS_SCANNABLE = True

    SCAN_REGEXPS = {
        'STATUS': [
            # device diagnostics
            # see notes.txt
            (r'^\*(?P<virt_id>\d{1,4})\*11\*(?P<diag_bits>[01]{24})##$', '_analyze_diagnostics', ),
            # when scanning a system for devices, obtain the hardware address of
            # each device on the bus.
            (r'^\*(?P<virt_id>\d{1,4})\*13\*(?P<hw_addr>\d{1,10})##$', '_register_device', )
        ]
    }

    def parse_regexp(self, msg):
        sys_regexps = self.get_regexps(msg, 'SYSTEM_REGEXPS')
        scan_regexps = self.get_regexps(msg, 'SCAN_REGEXPS')
        regexps = sys_regexps + scan_regexps
        return self._parse_regexp(msg, regexps)

    def _analyze_diagnostics(self, matches):
        self.log('DiagScannable dev diags : %s' % str(matches))
        return True

    def _register_device(self, matches):
        self.log('registering device')
        self.system.devices.register(self, matches)
        return True
    