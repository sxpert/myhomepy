# -*- coding: utf-8 -*-

import re
from .subsystems import find_subsystem


class Message(object):
    MSG_COMMAND = 0
    MSG_STATUS = 1
    MSG_TYPES = ['COMMAND', 'STATUS', ]

    _src = None
    _str = None
    _type = None
    _who = None
    _msg = None

    def __init__(self, msg = None, source=None):
        self._str = msg
        self._src = source
        self._identify_type()

    def log(self, msg):
        if self._src is not None:
            self._src.log(msg)
        else:
            print(msg)

    def _identify_type(self):
        # # skip useless *1001*3*0## frame
        # if self._str == '*1001*3*0##':
        #     return
        # analyze the content of messages passed from the layer 1
        m = re.match(r'^\*(?P<who>\d+)(?P<msg>\*.*)', self._str)
        if m is not None:
            self._type = self.MSG_COMMAND
        else:
            m = re.match(r"^\*#(?P<who>\d+)(?P<msg>\*.*)", self._str)
            if m is not None:
                self._type = self.MSG_STATUS
        msg = self._str
        if self._type is not None:
            who, self._msg = m.groups()
            self._who = int(who)
            # we're done here
            return
        else:
            msg = 'Unknown first character in message '+msg
        # log something
        import inspect
        func = inspect.currentframe().f_code.co_name
        self.log("%s %s" % (func, msg))
        
    def __str__(self):
        return "<%s \'%s\'>" % (self.__class__.__name__, self._str)

    @property
    def is_command(self):
        return self._type == self.MSG_COMMAND

    @property
    def is_status(self):
        return self._type == self.MSG_STATUS

    @property
    def type_name(self):
        if self._type is not None:
            return self.MSG_TYPES[self._type]

    @property
    def who(self):
        return self._who

    @property
    def msg(self):
        return self._msg

    def dispatch(self):
        ok = False
        sub_class = find_subsystem(self._who)
        if sub_class is not None:
            subsystem = sub_class(self._src.system)
            ok = subsystem.parse(self)
            if ok is not None and ok:
                return
        if not ok:
            msg = "UNHANDLED %s message \'%s\' data \'%s\'" % \
                  (self.type_name, str(self._who), self._msg)
            self.log(msg)
        