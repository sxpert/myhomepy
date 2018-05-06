# -*- coding: utf-8 -*-

from . import _json
from . import system
from . import callback
from myopen.subsystems import find_subsystem

class Callbacks(dict, _json.Json):
    _log = None

    def __init__(self, obj=None):
        super().__init__(self)
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

    def serialize(self):
        cb = []
        for k in self.keys():
            _cb = self[k]
            if isinstance(_cb, list):
                for __cb in _cb:
                    cb.append(__cb)
            else:
                cb.append(_cb)
        return [item.serialize() for item in cb]

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
    