# -*- coding: utf-8 -*- 

from ._json import Json
from . import config



class Tls(Json):
    cert = None
    key = None
    available = False

    def __init__(self, obj=None):
        if obj is not None:
            if isinstance(obj, config.Config):
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
        if data is None:
            pass
        elif type(data) is not dict:
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
        if self.key is None and self.cert is None:
            return None
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
            f.read()
            f.close()
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

