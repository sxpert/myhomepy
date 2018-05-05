# -*- coding: utf-8 -*-

from myopen.socket import OWNSocket
from myopen.monitor import OWNMonitor

from . import _json
from . import gateway


class System(_json.Json):
    #
    # NOTE: this should go, as OWNMonitor should
    # inherit from OWNSocket 
    #
    COMMAND = OWNSocket.COMMAND
    MONITOR = OWNSocket.MONITOR

    def __init__(self, log_func=None):
        self.log = log_func
        self.database = None
        self.gateway = None
        self.devices = None
        self.callbacks = None
        self.system = None
        self.monitor = None
        self.systems = None

    def load(self, data):
        if type(data) is not dict:
            self.log("ERROR loading System, dictionnary expected")
        else:
            self.database = data.get('database', None)
            self.log('database: %s' % (self.database))
            gateway_data = data.get('gateway', None)
            if gateway_data is not None:
                self.gateway = gateway.Gateway(self)
                self.gateway.load(gateway_data)
            else:
                self.log("WARNING: no gateway entry in system")
            self.devices = data.get('devices', None)
            self.log("system.devices %s" % (str(self.devices)))
            self.callbacks = data.get('callbacks', None)
            self.log("system.callbacks %s" % (str(self.callbacks)))
        return self

    def serialize(self):
        data = {}
        data['database'] = self.database
        data['gateway'] = self.gateway.serialize()
        data['devices'] = self.devices
        data['callbacks'] = self.callbacks
        return data

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
        self.log("added system with system id=%d" % (self.id))

    def execute_callback(self, *args, **kwargs):
        self.monitor.execute_callback(*args, **kwargs)

    def socket(self, mode):
        return self.gateway.socket(mode)
