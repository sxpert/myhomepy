# -*- coding: utf-8 -*-

import datetime

# --------------------------------------------------------------------------------------------------
#
# System Logger
#


class Logger(object):
    def __init__(self, logfile):
        self.logfile = logfile

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
        logmsg = '%s %s' % (date_string, msg)
        print(logmsg)
        try:
            # TODO: syslog ?
            log_file = open(self.logfile, "a+")
            log_file.write(logmsg+'\n')
            log_file.close()
        except:
            pass
