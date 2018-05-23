# -*- coding: utf-8 -*-

import datetime
import inspect

__all__ = (
    'LOG_EMERG', 'LOG_ALERT', 'LOG_CRITICAL', 'LOG_ERROR',
    'LOG_WARNING', 'LOG_NOTICE', 'LOG_INFO', 'LOG_DEBUG',
    'COLOR_RED', 'COLOR_GREEN', 'COLOR_YELLOW',
    'COLOR_BLUE', 'COLOR_MAGENTA', 'COLOR_CYAN',
    'COLOR_LT_RED', 'COLOR_LT_GREEN', 'COLOR_LT_YELLOW',
    'COLOR_LT_BLUE', 'COLOR_LT_MAGENTA', 'COLOR_LT_CYAN',
    'COLOR_DEFAULT',
    'Logger', 'SYSTEM_LOGGER', 'get_logger',
)

# --------------------------------------------------------------------------------------------------
#
# System Logger
#

LOG_EMERG = 0
LOG_ALERT = 1
LOG_CRITICAL = 2
LOG_ERROR = 3
LOG_WARNING = 4
LOG_NOTICE = 5
LOG_INFO = 6
LOG_DEBUG = 7

COLOR_RED = '\33[31m'
COLOR_GREEN = '\33[32m'
COLOR_YELLOW = '\33[33m'
COLOR_BLUE = '\33[34m'
COLOR_MAGENTA = '\33[35m'
COLOR_CYAN = '\33[36m'
COLOR_LT_RED = '\033[91m'
COLOR_LT_GREEN = '\033[92m'
COLOR_LT_YELLOW = '\033[93m'
COLOR_LT_BLUE = '\033[94m'
COLOR_LT_MAGENTA = '\033[95m'
COLOR_LT_CYAN = '\033[96m'
COLOR_DEFAULT = '\033[0m'


class Logger(object):
    _logfile = None
    _level = LOG_ERROR
    _debug = False

    def __init__(self, logfile=None):
        self._logfile = logfile

    @property
    def logfile(self):
        return self._logfile

    @logfile.setter
    def logfile(self, _logfile):
        self._logfile = _logfile

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, value):
        self._debug = value

    def log(self, msg, level=LOG_ERROR, header='',
            color=COLOR_DEFAULT):
        if self._debug:
            print('%s \'%s\' %d \'%s\'' %
                  (str(self), msg, level, header))
            return

        if level > self._level:
            return

        # generate datetime string
        current_date = datetime.datetime.today()
        date_string = "%04d-%02d-%02d %02d:%02d:%02d" % (
            current_date.year,
            current_date.month,
            current_date.day,
            current_date.hour,
            current_date.minute,
            current_date.second)
        if type(msg) is not str:
            msg = str(msg)

        # find name of caller

        if self._level == LOG_DEBUG:
            try:
                for _caller in inspect.stack():
                    _frame = _caller.frame
                    _locals = _frame.f_locals
                    _self = _locals.get('self', None)
                    _caller_class = None
                    if isinstance(_self, list) and len(_self) == 1:
                        _self = _self[0]
                    if not isinstance(_self, list):
                        _caller_class = _self.__class__
                    else:
                        _caller_class = _locals.get('__class__', None)
                    if _caller_class:
                        _class_name = _caller_class.__name__
                    # skip functions for the logger class
                    if _class_name == 'logger':
                        continue
                    _func_name = _caller.function
                    if _func_name != 'log':
                        # print(_caller)
                        break
            except:
                # inspect.stack() may fail
                _class_name = None
            if not _class_name:
                _class_name = "<unknown>"

            _caller_name = "%s.%s" % (_class_name, _func_name)
            msg = "%s : %s" % (_caller_name, msg)

        hdr = ''
        if header != '':
            hdr = header+' '
        logmsg = '%s %s%s' % (date_string, hdr, msg)
        prtmsg = logmsg
        if color != COLOR_DEFAULT:
            prtmsg = '%s %s%s%s%s' % \
                (date_string, color, hdr, msg, COLOR_DEFAULT)
        print(prtmsg, flush=True)

        # log to file
        if self._logfile:
            try:
                # TODO: syslog ?
                log_file = open(self._logfile, "a+")
                log_file.write(logmsg+'\n')
                log_file.close()
            except:
                pass

SYSTEM_LOGGER = Logger()


def get_logger(level=LOG_ERROR, header='', color=COLOR_DEFAULT):
    _l = SYSTEM_LOGGER
    # if level != SYSTEM_LOGGER.level:
    #     _l = Logger(SYSTEM_LOGGER.logfile)
    #     _l.level = level

    class logger(object):
        def __init__(self, _msg, _level=level, _header=header, _color=color):
            _l.log(_msg, _level, _header, _color)

        @property
        def debug(self):
            return _l.debug

        @debug.setter
        def debug(self, value):
            _l.debug = True

    return logger
