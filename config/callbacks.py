# -*- coding: utf-8 -*-

from . import system
from . import callback
from myopen.subsystems import find_subsystem

class Callbacks(object):
    _callbacks = {}
    _log = None

    def __init__(self, obj=None):
        if obj is not None:
            if isinstance(obj, system.System):
                self.system = obj
                self._log = self.system.log
            else:
                self.log("WARNING: wrong object passed "
                         "to Callbacks.__init__ %s" % (str(obj)))

    def log(self, msg):
        if self._log is not None:
            self._log(msg)
        else:
            print(msg)

    def load(self, data):
        if not isinstance(data, list):
            self.log("expecting a list of callback elements")
            return
        for cb_data in data:
            cb = callback.Callback(self)
            cb.load(cb_data)
            # add callback to this dict
            key = cb.map_callback()
            if key in self.keys():
                self.log("a callback for key %s is already present" % (key))
            else:
                self[key] = cb

    def __to_json__(self):
        if len(self._callbacks) == 0:
            return None
        # make a list of devices
        data = []
        for k in self._callbacks.keys():
            # TODO: this may be a list of things
            data.append(self._callbacks[k])
        return data

    # dict interface

    def keys(self):
        return self._callbacks.keys()

    def __len__(self):
        return len(self._callbacks)

    def __getitem__(self, key):
        return self._callbacks[key]

    def __setitem__(self, key, item):
        self._callbacks[key] = item


    def execute(self, subsystem, order, device, data):
        # subsystem is a subsystem instance
        key = subsystem.map_callback(order, device)
        if key is not None:
            if key in self.keys():
                cb = self[key]
                if isinstance(cb, list):
                    self.log(".1 handling of lists of callbacks not implemented yet")
                    self.log(".2 %s" % (str(cb)))
                    return False
                else:
                    return cb.execute(self.system, order, device, data)
            else:
                self.log("key %s not in callbacks => return None" % (key))
        else:
            self.log("key is None => return None")
        return None
    