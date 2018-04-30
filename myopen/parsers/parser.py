# -*- coding: utf-8 -*-


class OWNParser(object):

    def __init__(self, monitor=None):
        self.monitor = monitor

    def parse(self, mode, msg):
        self.monitor.log(msg)
        pass
