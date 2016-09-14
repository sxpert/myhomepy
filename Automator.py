#!/usr/bin/python2.7 -3
#-*- coding: utf-8 -*-

#
# (c) Raphael Jacquot 2014
# Licenced under the terms of the GNU GPL v3.0 or later
#

import config
import myOpenLayer1
import myOpenLayer2
import webserver
    
class TestApplication (object) :
    def init_scan (self):
        self.scan.init_scan (myOpenLayer2.SYSTEM__LIGHTING, self.scan_lights)
        #self.scan.init_scan (myOpenLayer2.SYSTEM__TEMP_CONTROL, self.scan_lights)

    def scan_lights (self):
        self.scan.finish()

    def __init__ (self) :
        # create the system loop
        self.sl = myOpenLayer1.MainLoop(myOpenLayer1.system_logger)

        # initializes the web server
        addr = ('', 8000)
        self.web = webserver.OpenWeb(addr)
        # should be included above...
        self.sl.add_socket (self.web)

        # setup the monitor socket 
        self.mon = myOpenLayer2.Monitor(self.sl)
        self.mon.register_callback (myOpenLayer2.SYSTEM__TEMP_CONTROL, self.mon.TEMP_CONTROL__REPORT_TEMP, { 'zone': 1, 'sensor': 1}, self.TempReportAction)
        self.mon.register_callback (myOpenLayer2.SYSTEM__LIGHTING, self.mon.LIGHTING__OFF, { 'group': 1}, self.CheckForGenOff)

        # setup the scanning process
        #self.scan = myOpenLayer2.Scanner(self.sl, self.init_scan)

        self.sl.run ()

    def TempReportAction (self, sensor, temp) :
        self.mon.log (unicode(sensor)+'  -  '+unicode(temp))

    def CheckForGenOff (self, command, light) :
        self.mon.log ('check for gen off : '+unicode(command)+'  -  '+unicode(light))

# main program
if __name__ == '__main__' :
    # create the application object, run the main loop
    TestApplication ()
