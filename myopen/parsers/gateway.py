# -*- coding: utf-8 -*-


class Gateway(object):
    SYSTEM_WHO = 13

    def __init__(self, monitor=None):
        self.monitor = monitor

    def parse(self, mode, msg):
        if self.monitor:
            self.monitor.log(str(self.monitor))
        pass
