# -*- coding: utf-8 -*-
import json


class OWNParser(object):

    def __init__(self, monitor=None):
        self.monitor = monitor

    def log(self, msg):
        if self.monitor:
            self.monitor.log(msg)
        else:
            print(self.__class__.__name__, msg)

    def parse(self, mode, msg):
        self.log(msg)
        if mode == self.monitor.STATUS:
            return self.parse_status(msg)
        if mode == self.monitor.COMMAND:
            return self.parse_command(msg)
        self.log("unknow")

    def parse_status(self, msg):
        self.log("STATUS %s -> %s" % (self.__class__.__name__, msg))

    def parse_command(self, msg):
        self.log("COMMAND %s -> %s" % (self.__class__.__name__, msg))

    def map_device(self, device):
        return None

    def execute_callback(self, system, order, device, data=None):
        self.log("EXECUTING CALLBACK -> %d %d %s %s" % (
            system, order, json.dumps(device), json.dumps(data),
        ))
        self.monitor.execute_callback(system, order, device, data)
