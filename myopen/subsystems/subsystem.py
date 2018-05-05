# -*- coding: utf-8 -*-

import json

class OWNSubSystem(object):
    system = None

    def __init__(self, system=None):
        self.system = system

    def log(self, msg):
        if self.system:
            self.system.log(msg)
        else:
            print(self.__class__.__name__, msg)

    def parse(self, msg):
        if msg.is_status:
            return self.parse_status(msg)
        if msg.is_command:
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
        self.log(self.system)
        self.system.execute_callback(system, order, device, data)
