# -*- coding: utf-8 -*-

from config._json import Json
from .basedevice import BaseDevice

class Devices(dict, Json):
    _system = None

    def __init__(self, system):
        self._system = system

    def log(self, msg):
        self._system.log(msg)

    def serialize(self):
        if len(self) == 0:
            return None
        return self

    # def __str__(self):
    #     _s = '<%s>' % (self.__class__.__name__)
    #     return _s

    def register(self, subsystem, data):
        # build proxy device
        d = BaseDevice(subsystem, data)
        if not d.valid:
            self.log('ERROR: malformed device register request, missing \'hw_addr\' value %s %s' %
                (str(subsystem), str(data)))        
            return None
        k = d.hw_addr_hex_str
        # if device already registered, return that
        if k in self.keys():
            return self[k]
        # insert proxy device
        self[k] = d
        return d


