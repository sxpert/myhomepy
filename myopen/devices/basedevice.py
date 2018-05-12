# -*- coding: utf-8 -*-

import json

#from config._json import Json

class BaseDevice(json.JSONEncoder):
    _subsystem = None
    _virt_id = None
    _hw_addr = None

    def __init__(self, subsystem, params):
        self._subsystem = subsystem
        self._virt_id = params.get('virt_id', None)
        self._hw_addr = params.get('hw_addr', None)
        if isinstance(self._hw_addr, str):
            # TODO: check if we get an exception
            self._hw_addr = int(self._hw_addr)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        _class = '<%s ' % (self.__class__.__name__)
        if self.valid:
            from . import Devices
            return '%sid: %s>' % (_class, Devices.format_hw_addr(self._hw_addr))
        return '%sINVALID>' % (_class)

    def __to_json__(self):
        data = {}
        data['virt_id'] = self._virt_id
        data['hw_addr'] = self._hw_addr
        return data

    @property
    def valid(self):
        return self._subsystem is not None and \
               self._virt_id is not None and \
               self._hw_addr is not None

    @property
    def hw_addr(self):
        return self._hw_addr
        