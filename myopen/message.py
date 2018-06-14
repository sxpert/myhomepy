# -*- coding: utf-8 -*-
import re
import sys
from datetime import time, date, datetime, timezone

from core.logger import LOG_ERROR, LOG_INFO

from .asyncio_connection import MODE_COMMAND, MODE_MONITOR
from .subsystems import find_subsystem

def jsonize(data):
    n_data = data
    if isinstance(data, dict):
        n_data = {}
        for k in data.keys():
            n_data[k] = jsonize(data[k])
    elif isinstance(data, list):
        n_data = []
        for v in data:
            n_data.append(jsonize(v))
    elif isinstance(data, datetime):
        n_data = {}
        n_data['year'] = data.year
        n_data['month'] = data.month
        n_data['day'] = data.day
        n_data['hour'] = data.hour
        n_data['minute'] = data.minute
        n_data['second'] = data.second
        n_data['microsecond'] = data.microsecond
        n_data['tzinfo'] = jsonize(data.tzinfo)
    elif isinstance(data, time):
        n_data = {}
        n_data['hour'] = data.hour
        n_data['minute'] = data.minute
        n_data['second'] = data.second
        n_data['microsecond'] = data.microsecond
        n_data['tzinfo'] = jsonize(data.tzinfo)
    elif isinstance(data, date):
        n_data = {}
        n_data['year'] = data.year
        n_data['month'] = data.month
        n_data['day'] = data.day
    elif isinstance(data, timezone):
        n_data = {}
        n_data['name'] = data.tzname(None)
        n_data['utc_offset'] = data.utcoffset(None).total_seconds()
    return n_data

class Message(object):
    MSG_NACK = 0
    MSG_ACK = 1
    MSG_COMMAND = 2
    MSG_STATUS = 3
    MSG_TYPES = ['NACK', 'ACK', 'COMMAND', 'STATUS', ]
    CNX_NAMES = ['CMD_CNX', 'MON_CNX', ]

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

        self._timestamp = datetime.now(timezone.utc)
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

    @property
    def web_data(self):
        data = {}
        data['msg'] = self._str
        data['timestamp'] = self._timestamp.isoformat()
        if self.system is not None:
            data['system_id'] = self.system.id
        if self._conn is not None:
            data['connection'] = self.CNX_NAMES[self._conn]
        if self._who is not None:
            data['who'] = self._who
        if self._type is not None:
            data['type'] = self.MSG_TYPES[self._type]
        if self._name is not None:
            data['name'] = self._name
        if self._fields is not None:
            if isinstance(self._fields, dict):
                fields_data = self._fields.get('data', None)
                if fields_data is not None:
                    data['fields'] = jsonize(self._fields['data'])
                
        elif self._fi is not None:
            data['fields'] = self._fi[1]
        obj = {}
        obj['type'] = self.__class__.__name__
        obj['data'] = data
        return obj

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
        m1 = re.match(r'^\*(?P<who>\d+)(?P<msg>\*.*)', self._str)
        m2 = re.match(r"^\*#(?P<who>\d+)(?P<msg>\*.*)", self._str)
        if m1 is not None:
            self._type = self.MSG_COMMAND
            m = m1
        if m2 is not None:
            self._type = self.MSG_STATUS
            m = m2
        msg = self._str
        if self._type is not None:
            who, self._msg = m.groups()
            self._who = int(who)
            # we're done here
            return
        # else...
        msg = 'Unknown first character in message '+msg
        # log something
        import inspect
        func = inspect.currentframe().f_code.co_name
        self.log("%s %s" % (func, msg))

    def __str__(self):
        s = '<%s' % (self.__class__.__name__)
        if self._type is not None:
            s += ' %s' % (self.MSG_TYPES[self._type])
        if self._conn is not None:
            s += ' %s' % (self.CNX_NAMES[self._conn])
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
    def is_conn_command(self):
        return self._conn == MODE_COMMAND

    @property
    def is_conn_monitor(self):
        return self._conn == MODE_MONITOR

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
            if self._sc is None:
                self.log('Message.parse : no appropriate subsystem to parse %s' % str(self))
                return False

            if self._sc is not None:
                self.subsystem = self._sc(self.system)
                self._fi = self.subsystem.parse(self)

            if self._fi is None:
                _sc_name = ''
                if self._sc is not None:
                    _sc_name = '%s ' % self._sc.__name__
                msg = "Message.parse : No regexp found to parse %s message \'%s\' %s\'%s\'" % \
                      (self.type_name, str(self._who), _sc_name, self._msg)
                self.log(msg, LOG_INFO)
                return False

            self._parsed = True
        # at this point, self._parsed should always be True
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
            self.log('Message._parse: expected a tuple of length 2 with (str, int)')
        # find the corresponding function object
        f = getattr(self.subsystem, fname, None)
        if f is None:
            # better logging ?
            self.log('Message._parse: Unable to find method %s.%s' %
                     (self._sc.__name__, fname))
            return None
        if not callable(f):
            self.log('Message._parse: not a callable method %s.%s' %
                     (self._sc.__name__, fname))
            return None
        if ver == 1:
            self._fields = f(matches)
        elif ver == 2:
            self._fields = f(self, matches)
        else:
            # ver is unknown
            self.log('Message._parse : expected an int for ver, got %s'
                     % (str(ver)), LOG_ERROR)
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
            try:
                return self._fields()
            except Exception as e:
                self.log('Message.dispatch (fields) FAILED: %s [%s]' % (sys._getframe(1).f_code.co_name, str(e)), LOG_ERROR)
                return False
        if self._fields is not None:
            return self.subsystem.do_callback(self._fields)
