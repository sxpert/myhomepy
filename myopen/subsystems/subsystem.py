# -*- coding: utf-8 -*-

import json
import re

from core.logger import LOG_INFO, COLOR_LT_RED, get_logger


class OWNSubSystem(object):

    def __init__(self, system=None):
        if system is None:
            self.log = get_logger(LOG_INFO, COLOR_LT_RED)
            self.log.debug = True
            self.log('had to create logger')
            #raise SystemError
        else:
            self.system = system
            self.log = system.log

    # ---------------------------------------------------------------------
    #
    # Message parsing stuff
    #

    def parse(self, msg):
        return self.parse_regexp(msg)

    def parse_regexp(self, msg):
        return self._parse_regexp(msg, self.get_regexps(msg, 'SYSTEM_REGEXPS'))

    def get_regexps(self, msg, name):
        """
        returns a list of regexps according to the message type
        """
        regexps = getattr(self, name, {})
        return regexps.get(msg.type_name, [])

    def _parse_regexp(self, msg, regexps):
        """
        search for the function corresponding to the message
        in :
        Message object
        regexps list

        out, either:
        * a tuple (function, matches)
        * None
        """
        # step 1: find a regexp that matches
        func_info = None
        if len(regexps) > 0:
            for rec in regexps:
                if isinstance(rec, tuple):
                    r, f = rec
                    name = None
                if isinstance(rec, dict):
                    name = rec.get('name')
                    r = rec.get('re')
                    f = rec.get('func')
                m = re.match(r, msg.msg)
                if m is not None:
                    # package the info on the func
                    matches = m.groupdict()
                    func_info = (f, matches, name, )
        # either a tuple or none
        return func_info

    # ---------------------------------------------------------------------
    #
    # Callback stuff
    #

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
                self.log('Subsystem.map_callback %d-%d-%s' %
                         (who, order, str(dev)),
                         LOG_INFO)
                return None
            ck = "%d-%d-%s" % (who, order, dev)
            self.log('OWNSubSystem.map_callback %s' % (ck),
                     LOG_INFO)
            return ck
        self.log("ERROR: Can't call %s.map_callback" % (
            self.__class__.__name__))

    @classmethod
    def _map_callback_name(self, name, callbacks):
        if not isinstance(callbacks, dict):
            return None
        _cb_id = callbacks.get(name, None)
        return _cb_id

    def map_callback_name(self, name):
        self.log('OWNSubSystem.map_callback_name', LOG_INFO)
        sys_callbacks = getattr(self, 'SYSTEM_CALLBACKS', None)
        if sys_callbacks is None:
            return None
        return self.__class__._map_callback_name(name, sys_callbacks)

    def callback(self, order, device, data=None):
        logmsg = 'OWNSubSystem.callback %d %s %s' % \
                 (order, str(device), str(data))
        self.log(logmsg, LOG_INFO)
        callback_ok = self.system.callback(self, order, device, data)
        if isinstance(callback_ok, bool):
            if callback_ok:
                return True
            else:
                self.log('OWNSubsystem.callback WARNING: '
                         'unable to execute callback')
                return False
        # we had None here
        self.log('OWNSubSystem.callback WARNING : no callback found', LOG_INFO)
        # lets say things were fine
        return True
