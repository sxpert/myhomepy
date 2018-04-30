# -*- coding: utf-8 -*-


class TempControl(object):
    SYSTEM_WHO = 4

    def __init__(self, monitor=None):
        self.monitor = monitor

    def parse(self, mode, msg):
        pass
