# -*- coding: utf-8 -*-
from .parser import OWNParser


class Gateway(OWNParser):
    SYSTEM_WHO = 13

    def parse_status(self, msg):
        self.log('gateway status ' + msg)

