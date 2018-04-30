# -*- coding: utf-8 -*-


class DiagLighting(object):
    SYSTEM_WHO = 1001

    def __init__(self, monitor=None):
        self.monitor = monitor

    def parse(self, mode, msg):
        pass
