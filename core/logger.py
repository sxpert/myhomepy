# -*- coding: utf-8 -*-

import datetime
import inspect

# --------------------------------------------------------------------------------------------------
#
# System Logger
#


class Logger(object):
    _logfile = None
    _debug = False

    COLOR_RED = '\033[91m'
    COLOR_DEFAULT = '\033[0m'  

    def __init__(self, logfile=None):
        self._logfile = logfile

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, _debug):
        self._debug = _debug

    @property
    def logfile(self):
        return self._logfile
    
    @logfile.setter
    def logfile(self, _logfile):
        self._logfile = _logfile

    def log(self, msg):
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

        if self._debug:
            for _caller in inspect.stack():
                _func_name = _caller.function
                if _func_name != 'log':
                    #print(_caller)
                    break
            #_caller = inspect.stack()[2]
            _func_name = _caller.function
            _frame = _caller.frame
            _locals = _frame.f_locals
            _self = _locals.get('self', None)
            _class_name = None
            if isinstance(_self, list):
                if len(_self) == 1:
                    _self = _self[0]
                else:
                    print(self.COLOR_RED, _self, self.COLOR_DEFAULT)
            if not isinstance(_self, list): 
                _class_name = _self.__class__.__name__
            else:
                # print("looking for class name")
                # try:
                #     print(str(_locals))
                # except AssertionError as e:
                #     print(self.COLOR_RED, e, self.COLOR_DEFAULT)
                #     print(_locals.keys())
                _class = _locals.get('__class__', None)
                if _class:
                    _class_name = _class.__name__
            if not _class_name:
                _class_name = "<unknown>"
            
            _caller_name = "%s.%s" % (_class_name, _func_name)
            msg = "%s : %s" % (_caller_name, str(msg))

        logmsg = '%s %s' % (date_string, msg)
        print(logmsg)

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