# -*- coding: utf-8 -*-
from .subsystem import OWNSubSystem


class Gateway(OWNSubSystem):
    SYSTEM_WHO = 13

    def parse_status(self, msg):
        self.log('gateway status ' + msg)
