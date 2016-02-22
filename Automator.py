#!/usr/bin/python2.7 -3
#-*- coding: utf-8 -*-

#
# (c) Raphael Jacquot 2014
# Licenced under the terms of the GNU GPL v3.0 or later
#

import config
from myOpenApplication import *

class TestApplication (object) :
    def __init__ (self) :
        self.ok = MyOpenApplication()

        self.ok.register_callback (self.ok.SYSTEM__TEMP_CONTROL, self.ok.TEMP_CONTROL__REPORT_TEMP, { 'zone': 1, 'sensor': 1}, self.TempReportAction)
        self.ok.run ()

    def TempReportAction (self, sensor, temp) :
        self.ok.log (unicode(sensor)+'  -  '+unicode(temp))

# main program
if __name__ == '__main__' :
    # create the application object, run the main loop
    TestApplication ()
