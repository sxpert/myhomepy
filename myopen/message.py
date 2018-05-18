# -*- coding: utf-8 -*-

import re
from .subsystems import find_subsystem


class Message(object):
    MSG_NACK = 0
    MSG_ACK = 1
    MSG_COMMAND = 2
    MSG_STATUS = 3
    MSG_TYPES = ['NACK', 'ACK', 'COMMAND', 'STATUS', ]

    def __init__(self, msg=None, source=None):
        from config.gateway import Gateway
        from config.system import System
        if isinstance(source, Gateway):
            self.system = source.system
        if isinstance(source, System):
            self.system = source
        if self.system is not None:
            self.log = self.system.log
        else:
            # should create a logger
            self.log = self._default_logger
        if isinstance(msg, tuple):
            self._str, self._conn = msg
        if isinstance(msg, str):
            self._str = msg

        # initialize other variables
        self._parsed = False
        self._type = None
        self._sc = None
        self._who = None
        self._name = None
        self._fi = None
        self._fields = None
        self._msg = None
        self._identify_type()

    def _default_logger(self, msg):
        print(msg)

    def _identify_type(self):
        if self._str == '*#*0##':
            self._type = self.MSG_NACK
            return
        if self._str == '*#*1##':
            self._type = self.MSG_ACK
            return
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
        s = '<%s' % (self.__class__.__name__)
        if self._type is not None:
            s += ' %s' % (self.MSG_TYPES[self._type])
        if self._sc is not None:
            s += ' %s' % (self._sc.__name__)
        if self._name is not None:
            s += ' \'%s\'' % (self._name)
        if self._fields is not None:
            s += ' %s' % (str(self._fields))
        s += ' \'%s\'>' % (self._str)
        return s

    @property
    def is_command(self):
        return self._type == self.MSG_COMMAND

    @property
    def is_status(self):
        return self._type == self.MSG_STATUS

    @property
    def is_ack(self):
        return self._type == self.MSG_ACK

    @property
    def is_nack(self):
        return self._type == self.MSG_NACK

    @property
    def type_name(self):
        if self._type is not None:
            return self.MSG_TYPES[self._type]

    @property
    def conn(self):
        return self._conn

    @property
    def who(self):
        return self._who

    @property
    def name(self):
        return self._name

    @property
    def msg(self):
        return self._msg

    def parse(self):
        if not self._parsed and (self.is_ack or self.is_nack):
            self._parsed = True

        if not self._parsed:
            self._sc = find_subsystem(self._who)
            if self._sc is not None:
                self.subsystem = self._sc(self.system)
                self._fi = self.subsystem.parse(self)

            if self._fi is None:
                _sc_name = ''
                if self._sc is not None:
                    _sc_name = '%s ' % self._sc.__name__
                msg = "UNHANDLED %s message \'%s\' %s\'%s\'" % \
                      (self.type_name,
                       str(self._who),
                       _sc_name,
                       self._msg)
                self.log(msg)

            self._parsed = True
        if self._parsed:
            self._parse()
        return self._parsed

    def _parse(self):
        if self._fi is None:
            return None

        # do something with func_info
        # finfo is either a str or a tuple
        finfo, matches, name = self._fi
        if name is not None:
            self._name = name
        if isinstance(finfo, str):
            fname = finfo
            ver = 1
            finfo = (fname, ver)
        if isinstance(finfo, tuple) and len(finfo) == 2:
            fname, ver = finfo
            # check types and complain ?
        else:
            self.log('Message._parse: '
                     'expected a tuple of length 2 with (str, int)')
        # find the corresponding function object
        f = getattr(self.subsystem, fname, None)
        if f is None:
            # better logging ?
            self.log('Message._parse: '
                     'Unable to find method %s.%s' %
                     (self._sc.__name__, fname))
            return None
        if not callable(f):
            self.log('Message._parse: '
                     'not a callable method %s.%s' %
                     (self._sc.__name__, fname))
            return None
        if ver == 1:
            self._fields = f(matches)
        elif ver == 2:
            self._fields = f(self, matches)
        else:
            # ver is unknown
            self.log('Message._parse : expected an int for ver, got %s'
                     (str(ver)))
            return False
        return True

    @property
    def function(self):
        if callable(self._fields):
            return self._fields
        return None

    def dispatch(self):
        self.parse()
        if isinstance(self._fields, bool):
            return self._fields
        if callable(self._fields):
            return self._fields()
        if self._fields is not None:
            return self.subsystem._do_callback(self._fields)
