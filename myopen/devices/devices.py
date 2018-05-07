# -*- coding: utf-8 -*-

from .basedevice import BaseDevice

class Devices(object):
    _system = None
    _devs = {}

    def __init__(self, system):
        self._system = system

    def log(self, msg):
        self._system.log(msg)
    
    def load(self, data):
        pass

    def __to_json__(self):
        if len(self._devs) == 0:
            return None
        # make a list of devices
        data = []
        for k in self._devs.keys():
            data.append(self._devs[k])
        return data

    # dict interface

    def keys(self):
        return self._devs.keys()

    def __len__(self):
        return len(self._devs)

    def __getitem__(self, key):
        return self._devs[key]

    def __setitem__(self, key, item):
        self._devs[key] = item

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


