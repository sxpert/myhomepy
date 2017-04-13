#!/usr/bin/python2.7 -3
#-*- coding: utf-8 -*-

#
# (c) Raphael Jacquot 2014
# Licenced under the terms of the GNU GPL v3.0 or later
#

#import config
import myOpenLayer1
import myOpenLayer2
import config
import webserver
import website
    
class TestApplication (object) :

    def __init__ (self) :
        # create the system loop
        self.sl = myOpenLayer1.MainLoop(myOpenLayer1.system_logger)
        config.config.set_main_loop(self.sl)

        # initializes the web server
        addr = ('', 8000)
        self.web = webserver.OpenWeb(addr)
    
        self.web.register_routes (
            [
                [ "^/API/$", website.ow_index.OW_index ],
                [ "^/API/add_system(.*)$", website.ow_add_system.OW_add_system ],
            ]
        )
        self.web.default_route (website.ow_static.OW_static)

        self.sl.add_server (self.web)

        self.sl.run ()

# main program
if __name__ == '__main__' :
    # create the application object, run the main loop
    TestApplication ()
