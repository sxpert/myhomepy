#!/usr/bin/python3
# -*- conding: utf-8 -*-

#
# (c) Raphael Jacquot 2014
# Licenced under the terms of the GNU GPL v3.0 or later
#

import json
import sys

from myopen import layer1
from myopen import layer2

CONFIG_FILE_NAME = 'config.json'


class Json(object):
    def load(self, data):
        # do nothing
        pass

    def serialize(self):
        return None

    def json(self):
        return json.dumps(self.serialize(), indent=4)


class Tls(Json):
    def __init__(self, obj=None):
        self.cert = None
        self.key = None
        self.available = False
        if obj is not None:
            if isinstance(obj, Config):
                self.config = obj
                self._log = self.config.log
            else:
                self.log("WARNING: wrong object passed "
                         "to Systems.__init__ %s" % (str(obj)))
        self.log("TLS initialized")

    def log(self, msg):
        if self._log is not None:
            self._log(msg)
        else:
            print(msg)

    def load(self, data):
        if type(data) is not dict:
            self.log("ERROR loading TLS configuration, dictionnary expected")
        else:
            self.key = self.check_for_file('key', data)
            self.cert = self.check_for_file('cert', data)
            if self.available:
                self.log("TLS available")
            else:
                self.log("TLS unavailable")
        return self

    def serialize(self):
        data = {}
        data['key'] = self.key
        data['cert'] = self.cert
        return data

    def check_for_file(self, key, data):
        if key not in data.keys():
            self.log("ERROR: key '%s' not present in data %s" %
                     (key, str(data)))
            self.available = False
            return None
        fname = data[key]
        if fname is None:
            self.available = False
            return None
        try:
            f = open(fname)
        except OSError as e:
            self.log("ERROR: unable to open '%s' file '%s'" % (key, fname))
            self.log(str(e))
            self.available = False
        else:
            d = f.read()
            f.close()
            self.log("TLS '%s' file '%s' successfully loaded" % (key, fname))
            self.available = True
        return fname

    def __repr__(self):
        cert_s = None
        key_s = None
        if self.cert is not None:
            cert_s = "'%s'" % self.cert
        if self.key:
            key_s = "'%s'" % self.key
        avail_s = str(self.available)
        return "<%s cert: %s key: %s available: %s>" % (
            self.__class__.__name__, cert_s, key_s, avail_s)


class Gateway(Json):
    address = None
    port = None
    passwd = None
    available = False
    _log = None
    system = None

    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            obj = args[0]
            if isinstance(obj, System):
                self.system = obj
                self._log = obj.log
                return
        elif len(args) == 3:
            if isinstance(args[0], str) and \
               isinstance(args[1], int) and \
               isinstance(args[2], str):
                self.address = args[0]
                self.port = args[1]
                self.passwd = args[2]
                self.available = True
                return
        self.log("Invalid parameters on creating Gateway")
        self.log(args)
        self.log(kwargs)

    def set_system(self, system):
        self.system = system
        self._log = system.log

    def log(self, msg):
        if self._log is not None:
            self._log(str(msg))
        else:
            print(msg)

    def load(self, data):
        if type(data) is not dict:
            self.log("ERROR loading Gateway, dictionnary expected")
        else:
            self.address = data.get('ip', None)
            if not self.address:
                self.address = data.get('address', None)
            if not self.address:
                self.log("WARNING: no address specified for this "
                         "system's gateway")
            self.port = data.get('port', None)
            if not self.port:
                self.log("WARNING: no port specified for this system's "
                         "gateway, using default 20000")
                self.port = 20000
            self.passwd = data.get('password', None)
            if not self.passwd:
                self.passwd = data.get('passwd', None)
            if not self.passwd:
                self.log("WARNING: no open password specified for this "
                         "system's gateway")
            self.set_available()
            if not self.available:
                self.log("WARNING: problems in gateway configuration, "
                         "this system will not be available")
            else:
                self.log("Gateway %s ready" % str(self))
        return self

    def serialize(self):
        data = {}
        data['address'] = self.address
        data['port'] = self.port
        data['passwd'] = self.passwd
        return data

    def set_available(self):
        if self.address and self.port and self.passwd:
            self.available = True
        else:
            self.available = False

    def __repr__(self):
        address_s = str(self.address)
        port_s = str(self.port)
        # don't show password in logs
        passwd_s = '**********'
        return '<%s address: %s port: %s passwd: \'%s\'>' % (
            self.__class__.__name__, address_s, port_s, passwd_s)

    def socket(self, mode):
        if not self.available:
            self.log("ERROR attempting to create a socket for "
                     "unavailable gateway %s" % (str(self)))
            return None
        sock = layer1.OwnSocket(self.address, self.port, self.passwd, mode)
        return sock


class System(Json):
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
                self.gateway = Gateway(self)
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
        self.monitor = layer2.OWNMonitor(self)
        self.log("added system with system id=%d" % (self.id))

    def socket(self, mode):
        return self.gateway.socket(mode)


class Systems(list, Json):
    _log = None

    def __init__(self, obj=None):
        super().__init__(self)
        if obj is not None:
            if isinstance(obj, Config):
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
                s = System(self.log).load(s)
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


class Config(Json):
    def __init__(self, config_file=None):
        if config_file is None:
            self.config_file = CONFIG_FILE_NAME
        self.tls = Tls(self)
        self.systems = Systems(self)
        self.load_file(self.config_file)

    def log(self, msg):
        layer1.SYSTEM_LOGGER.log('[CONF] '+str(msg))

    # sets the main loop
    # starts up all loaded systems
    def set_main_loop(self, ml):
        self.main_loop = ml
        self.systems.run()

    def load_file(self, file):
        try:
            f = open(file, 'r')
        except IOError as e:
            if e.errno == 2:
                self.log('unable to find a configuration file to load')
        else:
            self.log('configuration file opened successfully')
            # read the configuration file
            d = f.read()
            f.close()
            self.load(d)

    def load(self, data):
            if len(data) > 0:
                data = json.loads(data)
                if type(data) is dict:
                    k = data.keys()
                    if 'tls' in k:
                        self.tls.load(data['tls'])
                    if 'systems' in k:
                        self.systems.load(data['systems'])
                else:
                    self.log("invalid configuration format")
            else:
                self.log("WARNING: configuration file is empty")

    def serialize(self):
        data = {}
        data['tls'] = self.tls.serialize()
        data['systems'] = self.systems.serialize()
        return data

    def save(self):
        f = open(self.config_file, 'w')
        f.write(self.json())
        f.close()

    def add_system(self, ip, port, password):
        # search if we already have this system

        # for s in self.systems:
        #     # TODO: fix
        #     try:
        #         gw = s['gateway']
        #     except KeyError:
        #         self.log("no gateway entry in system")
        #         continue
        #     try:
        #         gw_ip = gw['ip']
        #         gw_port = gw['port']
        #         gw_password = gw['password']
        #     except KeyError as e:
        #         self.log("gateway entry missing one of (ip, port, password)")
        #         continue
        #     if gw_ip == ip and gw_port == port and gw_password == password:
        #         self.log("a system with identical values has already been "
        #                  "configured")
        #         return False
        # # couldn't find system
        gateway = Gateway(ip, port, password)
        system = System(self.log)
        system.set_gateway(gateway)
        self.systems.append(system)
        system.run()
        self.save()

    @property
    def nb_systems(self):
        return len(self.systems)


config = Config()

if __name__ == '__main__':
    system_loop = layer1.MainLoop(layer1.SYSTEM_LOGGER)
    config.set_main_loop(system_loop)
    pass
