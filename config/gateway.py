# -*- coding: utf-8 -*-

from myopen.socket import OWNSocket

from . import _json, system


class Gateway(_json.Json):
    address = None
    port = None
    passwd = None
    available = False
    _log = None
    system = None

    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            obj = args[0]
            if isinstance(obj, system.System):
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
        sock = OWNSocket(self.address, self.port, self.passwd, mode)
        # find the original system level logger
        sock.set_logger(self.system.main_loop.logger.log)
        return sock
