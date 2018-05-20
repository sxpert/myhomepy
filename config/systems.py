# -*- coding: utf-8 -*-

from . import config as conf
from . import system


class Systems(list):
    _log = None

    def __init__(self, config=None):
        super().__init__(self)
        if config is not None:
            if isinstance(config, conf.Config):
                self.config = config
                self.log = self.config.log

    def loads(self, data):
        if type(data) is not list:
            self.log("ERROR loading Systems, list expected")
        else:
            # enumerate all systems, and load each
            for s in data:
                s = system.System(self.log).loads(s)
                self.append(s)
        return self

    # def __to_json__(self):
    #     return self

    def append(self, obj):
        super().append(obj)
        obj.systems = self
        return obj

    @property
    def async_loop(self):
        if self.config is not None:
            al = getattr(self.config, 'async_loop', None)
            return al
        else:
            return None

    def run(self):
        for s in self:
            self.log("starting system %s" % (str(s.id)))
            s.run()
