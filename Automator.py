#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

"""
Main application module
"""

#
# (c) Raphael Jacquot 2014
# Licenced under the terms of the GNU GPL v3.0 or later
#

import website
from config import Config
from core.logger import Logger
from core.mainloop import MainLoop
from webserver import OpenWeb

DEBUG = True
LOGFILE = 'myopenlog-2.log'


class Automator(object):
    """
    This is the test application object
    """

    def __init__(self):
        # create the system loop
        self.system_logger = Logger(LOGFILE)
        self.system_loop = MainLoop(self.system_logger)
        self.config = Config(self)
        self.config.set_main_loop(self.system_loop)

        # initializes the web server
        addr = ('', 8000)
        self.web = OpenWeb(self, addr)

        self.web.default_route(website.ow_static.OW_static)
        self.web.register_routes(
            [
                ["^/$", website.ow_index.OW_index],
                ["^/API/test$", website.ow_index.OW_test],
                ["^/API/add_system(.*)$", website.ow_add_system.OW_add_system],
                ["^/API/GeneralOff$", website.ow_general_off.OW_general_off],
                ["^/API/temperatures(.*)$",
                 website.ow_temperatures.OW_list_temperatures],
            ]
        )

        self.system_loop.add_task(self.web)

        self.system_loop.run()

# main program
if __name__ == '__main__':
    # create the application object, run the main loop
    Automator()
