# -*- coding: utf-8 -*-

from . import _json
from . import config
from . import system


class Systems(list, _json.Json):
    _log = None

    def __init__(self, obj=None):
        super().__init__(self)
        if obj is not None:
            if isinstance(obj, config.Config):
                self.config = obj
                self._log = self.config.log
            else:
                self.log("WARNING: wrong object passed "
                         "to Systems.__init__ %s" % (str(obj)))
        self.log("initializing systems")

    def log(self, msg):
        if self._log is not None:
            self._log(msg)
        else:
            print(msg)

    def load(self, data):
        if type(data) is not list:
            self.log("ERROR loading Systems, list expected")
        else:
            # enumerate all systems, and load each
            for s in data:
                s = system.System(self.log).load(s)
                self.append(s)
                self.log("added system %s" % str(s.id))
            self.log("systems => %s" % str(self))
        return self

    def serialize(self):
        data = []
        for s in self:
            data.append(s.serialize())
        return data

    def append(self, obj):
        super().append(obj)
        obj.systems = self
        return obj

    @property
    def main_loop(self):
        if self.config is not None:
            return self.config.main_loop
        else:
            return None

    def run(self):
        for s in self:
            self.log("starting system %s" % (str(s.id)))
            s.run()
