# -*- coding: utf-8 -*-

from core.logger import LOG_INFO
from myopen.subsystems import find_subsystem

from . import callback, system


class Callbacks(object):
    _callbacks = {}

    def __init__(self, obj=None):
        if obj is not None:
            if isinstance(obj, system.System):
                self.system = obj
                self.log = self.system.log
            else:
                self.log("WARNING: wrong object passed to Callbacks.__init__ %s" % (str(obj)))

    def loads(self, data):
        self.log('loading callbacks')
        if not isinstance(data, list):
            self.log("expecting a list of callback elements")
            return
        for cb_data in data:
            cb = callback.Callback(self)
            cb.loads(cb_data)
            # add callback to this dict
            key = cb.map_callback()
            if key in self.keys():
                self.log("a callback for key %s is already present" % (key))
            else:
                self[key] = cb
        self.log("callbacks loaded")

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
        self.log('config.Callbacks.execute : key %s' % (str(key)), LOG_INFO)
        if key is not None:
            if key in self.keys():
                cb = self[key]
                if isinstance(cb, list):
                    self.log('Callbacks.execute : .1 handling of lists of callbacks not implemented yet')
                    self.log('Callbacks.execute : .2 %s' % (str(cb)))
                    return False
                else:
                    self.log('config.Callbacks.execute : found callback %s' % (str(cb)), LOG_INFO)
                    return cb.execute(self.system, order, device, data)
            else:
                # there is no callback by this key, ignore
                # self.log('Callbacks.execute INFO : key %s not in callbacks => return None' % (key))
                pass
        else:
            self.log("Callbacks.execute WARNING : key is None => return None", LOG_INFO)
        return None
