# -*- coding: utf-8 -*-

import json
import re


class OWNSubSystem(object):
    SYSTEM_NAME = "UNKNOWN"
    SYSTEM_WHO = None
    SYSTEM_CALLBACKS = None
    SYSTEM_REGEXPS = None
    system = None

    def __init__(self, system=None):
        self.system = system

    def log(self, msg):
        if self.system:
            self.system.log(msg)
        else:
            print(msg)

    def parse(self, msg):
        if msg.is_status:
            return self.parse_status(msg)
        if msg.is_command:
            return self.parse_command(msg)
        self.log("Unknown message type %s" % (str(msg)))
        return None

    def parse_status(self, msg):
        cb_data = self.parse_regexp(msg)
        if cb_data is not None:
            return self._do_callback(cb_data)
        # say something only if we coudn't do anything with it
        self.log("STATUS %s -> %s" % (self.__class__.__name__, msg))
        return None
        
    def parse_command(self, msg):
        cb_data = self.parse_regexp(msg)
        if cb_data is not None:
            return self._do_callback(cb_data)
        # say something only if we coudn't do anything with it
        self.log("COMMAND %s -> %s" % (self.__class__.__name__, msg))
        return None
        
    def parse_regexp(self, msg):
        if self.SYSTEM_REGEXPS is None:
            return None
        if not isinstance(self.SYSTEM_REGEXPS, dict):
            self.log("SYSTEM_REGEXPS is not dict")
            return None
        mode_regexps = self.SYSTEM_REGEXPS.get(msg.type_name, None)
        if mode_regexps is not None:
            for r, fname in mode_regexps:
                m = re.match(r, msg.msg)
                if m is not None:
                    matches = m.groupdict()
                    try:
                        f = getattr(self, fname)
                    except AttributeError:
                        self.log("Unable to find method %s.%s" % (
                            self.__class__.__name__, fname))
                        return None
                    else:
                        return f(matches)
        # nothing was found
        return None        

    def gen_callback_dict(self, order, device, data):
        return {
            'order': order,
            'device': device,
            'data': data
        }

    def _do_callback(self, cb_data):
        _command = cb_data.get('order', None)
        _device = cb_data.get('device', None)
        _data = cb_data.get('data', None)
        if _command is not None and _device is not None:
            return self.callback(_command, _device, _data)

    def map_device(self, device):
        return None

    def map_callback(self, order, device):
        who = self.SYSTEM_WHO
        if who is not None:
            dev = self.map_device(device)
            if dev is None:
                # can't map it, no problem
                return None
            return "%d-%d-%s" % (who, order, dev)
        self.log("ERROR: Can't call %s.map_callback" % (
            self.__class__.__name__))

    @classmethod
    def map_callback_name(cls, name):
        if cls.SYSTEM_CALLBACKS is None:
            return None
        if not isinstance(cls.SYSTEM_CALLBACKS, dict):
            return None
        _cb_id = cls.SYSTEM_CALLBACKS.get(name, None)
        return _cb_id   

    def callback(self, order, device, data=None):
        self.log("%s.callback %d %s %s" % (
            self.__class__.__name__, order,
            json.dumps(device), json.dumps(data)
        ))
        callback_ok = self.system.callback(self, order, device, data)
        self.log("callback_ok : %s %s" % (str(type(callback_ok)), str(callback_ok)))
        if callback_ok is bool and not callback_ok:
            self.log("WARNING: unable to execute callback")
        return callback_ok
