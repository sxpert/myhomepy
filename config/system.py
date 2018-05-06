# -*- coding: utf-8 -*-

import database
from myopen.monitor import OWNMonitor
from myopen.socket import OWNSocket

from . import _json, callbacks, gateway


class System(_json.Json):
    #
    # NOTE: this should go, as OWNMonitor should
    # inherit from OWNSocket 
    #
    COMMAND = OWNSocket.COMMAND
    MONITOR = OWNSocket.MONITOR

    log = None
    _db = None
    _database = None
    gateway = None
    devices = None
    callbacks = None
    _callbacks = None
    # system = None
    monitor = None
    systems = None

    def __init__(self, log_func=None):
        self.log = log_func

    def load(self, data):
        if type(data) is not dict:
            self.log("ERROR loading System, dictionnary expected")
        else:
            self._database = data.get('database', None)
            self.log('database: %s' % (self._database))
            gateway_data = data.get('gateway', None)
            if gateway_data is not None:
                self.gateway = gateway.Gateway(self)
                self.gateway.load(gateway_data)
            else:
                self.log("WARNING: no gateway entry in system")
            self.devices = data.get('devices', None)
            self.log("system.devices %s" % (str(self.devices)))
            callbacks_data = data.get('callbacks', None)
            if callbacks_data is not None:
                self.callbacks = callbacks_data
                self._callbacks = callbacks.Callbacks(self)
                self._callbacks.load(callbacks_data)
        return self

    def serialize(self):
        data = {}
        data['database'] = self.database
        data['gateway'] = self.gateway.serialize()
        data['devices'] = self.devices
        data['callbacks'] = self.callbacks
        return data

    @property
    def database(self):
        if self._db is None:
            if self._database is None:
                self.log("No database specified anywhere")
            else:
                self.log("Opening database %s" % (self._database))
                self._db = database.Database(self._database, self.log)
        return self._db
        
    @property
    def id(self):
        if not self.systems:
            return None
        return self.systems.index(self)

    @property
    def main_loop(self):
        if not self.systems:
            self.log("ERROR: Unable to access the systems list object")
            return None
        return self.systems.main_loop

    def set_gateway(self, gateway):
        self.gateway = gateway
        gateway.set_system(self)
        return self

    def __repr__(self):
        return "<%s %s>" % (
            self.__class__.__name__, self.gateway)

    def run(self):
        if self.main_loop is None:
            self.log("ERROR: Unable to start system, there is no system loop")
            return False
        self.monitor = OWNMonitor(self)

    def callback(self, *args, **kwargs):
        return self._callbacks.execute(*args, **kwargs)

    def socket(self, mode):
        return self.gateway.socket(mode)
