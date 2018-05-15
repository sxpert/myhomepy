# -*- coding: utf-8 -*-

import json
import re

from core.logger import SYSTEM_LOGGER


class OWNSubSystem(object):

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
            if isinstance(cb_data, bool):
                return cb_data
            return self._do_callback(cb_data)
        # say something only if we coudn't do anything with it
        self.log("STATUS %s -> %s" % (self.__class__.__name__, msg))
        return None

    def parse_command(self, msg):
        cb_data = self.parse_regexp(msg)
        if cb_data is not None:
            if isinstance(cb_data, bool):
                return cb_data
            return self._do_callback(cb_data)
        # say something only if we coudn't do anything with it
        self.log("COMMAND %s -> %s" % (self.__class__.__name__, msg))
        return None

    def parse_regexp(self, msg):
        return self._parse_regexp(msg, self.get_regexps(msg, 'SYSTEM_REGEXPS'))

    def get_regexps(self, msg, name):
        regexps = getattr(self, name, {})
        return regexps.get(msg.type_name, [])

    def _parse_regexp(self, msg, regexps):
        if len(regexps) > 0:
            for r, fname in regexps:
                m = re.match(r, msg.msg)
                if m is not None:
                    matches = m.groupdict()
                    f = getattr(self, fname, None)
                    if callable(f):
                        return f(matches)
                    else:
                        self.log("Unable to find method %s.%s" % (
                            self.__class__.__name__, fname))
                        return None
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
        # device may be none... (for instance in the case of the gateway)
        if _command is not None:
            return self.callback(_command, _device, _data)
        self.log('Subsystem._do_callback WARNING : %s' % (str(cb_data)))

    def map_device(self, device):
        return None

    def map_callback(self, order, device):
        who = getattr(self, 'SYSTEM_WHO', None)
        if who is not None:
            dev = self.map_device(device)
            if dev is None:
                # can't map it, no problem
                if SYSTEM_LOGGER.debug:
                    self.log('Subsystem.map_callback %d-%d-%s' %
                             (who, order, str(dev)))
                return None
            return "%d-%d-%s" % (who, order, dev)
        self.log("ERROR: Can't call %s.map_callback" % (
            self.__class__.__name__))

    @classmethod
    def _map_callback_name(cls, name, callbacks):
        if not isinstance(callbacks, dict):
            return None
        _cb_id = callbacks.get(name, None)
        return _cb_id

    @classmethod
    def map_callback_name(cls, name):
        print('OWNSubSystem.map_callback_name')
        sys_callbacks = getattr(cls, 'SYSTEM_CALLBACKS', None)
        if sys_callbacks is None:
            return None
        return cls._map_callback_name(name, sys_callbacks)

    def callback(self, order, device, data=None):
        if SYSTEM_LOGGER.debug:
            self.log("OWNSubSystem.callback %d %s %s" %
                     (order, str(device), str(data)))
        callback_ok = self.system.callback(self, order, device, data)
        if callback_ok is bool:
            if callback_ok:
                return True
            else:
                self.log('OWNSubsystem.callback WARNING: '
                         'unable to execute callback')
                return False
        # we had None here
        if SYSTEM_LOGGER.debug:
            self.log('OWNSubSystem.callback WARNING : no callback found')
        # lets say things were fine
        return True
