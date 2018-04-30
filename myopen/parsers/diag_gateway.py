# -*- coding: utf-8 -*-


class DiagGateway(object):
    SYSTEM_WHO = 1013

    def __init__(self, monitor=None):
        self.monitor = monitor

    def parse(self, mode, msg):
        pass
