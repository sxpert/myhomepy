# -*- coding: utf-8 -*-


class DiagTempControl(object):
    SYSTEM_WHO = 1004

    def __init__(self, monitor=None):
        self.monitor = monitor

    def parse(self, mode, msg):
        pass
