#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

"""
Main application module
"""

#
# (c) Raphael Jacquot 2014
# Licenced under the terms of the GNU GPL v3.0 or later
#

# import config
from myopen import layer1
import config
import webserver
import website


class TestApplication(object):
    """
    This is the test application object
    """

    def __init__(self):
        # create the system loop
        self.system_loop = layer1.MainLoop(layer1.SYSTEM_LOGGER)
        config.config.set_main_loop(self.system_loop)

        # initializes the web server
        addr = ('', 8000)
        self.web = webserver.OpenWeb(addr)

        self.web.register_routes(
            [
                ["^/$", website.ow_index.OW_index],
                ["^/API/add_system(.*)$", website.ow_add_system.OW_add_system],
                ["^/API/GeneralOff$", website.ow_general_off.OW_general_off],
                ["^/API/temperatures(.*)$",
                 website.ow_temperatures.OW_list_temperatures],
            ]
        )
        self.web.default_route(website.ow_static.OW_static)

        self.system_loop.add_task(self.web)

        self.system_loop.run()

# main program
if __name__ == '__main__':
    # create the application object, run the main loop
    TestApplication()
