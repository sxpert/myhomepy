# -*- coding: utf-8 -*-

from config._json import Json

class BaseDevice(Json):
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
            return '%sid: %s>' % (_class, self.hw_addr_hex_str)
        return '%sINVALID>' % (_class)

    @property
    def valid(self):
        return self._subsystem is not None and \
               self._virt_id is not None and \
               self._hw_addr is not None

    # return the hw_addr as an 8 char hex string
    @property
    def hw_addr_hex_str(self):
        if self._hw_addr is None:
            return None
        return '%08X' % (self._hw_addr)