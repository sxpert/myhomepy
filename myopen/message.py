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

    def __init__(self, msg=None, source=None):
        self._str = msg
        self._src = source
        self._identify_type()

    def log(self, msg):
        if self._src is not None:
            self._src.log(msg)
        else:
            print(msg)

    def _identify_type(self):
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
        func_info = None
        sub_class = find_subsystem(self._who)
        if sub_class is not None:
            subsystem = sub_class(self._src.system)
            func_info = subsystem.parse(self)
        if func_info is None:
            msg = "UNHANDLED %s message \'%s\' %s \'%s\'" % \
                  (self.type_name,
                   str(self._who),
                   sub_class.__name__,
                   self._msg)
            self.log(msg)
            return None
        # do something with func_info
        # finfo is either a str or a tuple
        finfo, matches = func_info
        if isinstance(finfo, str):
            fname = finfo
            ver = 1
            finfo = (fname, ver)
        if isinstance(finfo, tuple) and len(finfo) == 2:
            fname, ver = finfo
            # check types and complain ?
        else:
            self.log('Message.dispatch: '
                     'expected a tuple of length 2 with (str, int)')
        # find the corresponding function object
        f = getattr(subsystem, fname, None)
        if f is None:
            # better logging ?
            self.log('Message.dispatch: '
                     'Unable to find method %s.%s' %
                     (sub_class.__name__, fname))
            return None
        if not callable(f):
            self.log('Message.dispatch: '
                     'not a callable method %s.%s' %
                     (sub_class.__name__, fname))
            return None
        if ver == 1:
            cb_data = f(matches)
        elif ver == 2:
            cb_data = f(self, matches)
        else:
            # ver is unknown
            self.log('Message.dispatch : expected an int for ver, got %s'
                     (str(ver)))
            return False
        if cb_data is not None:
            if isinstance(cb_data, bool):
                return cb_data
            return subsystem._do_callback(cb_data)
