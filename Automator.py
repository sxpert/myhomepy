#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

"""
Main application module
"""

#
# (c) Raphael Jacquot 2018
# Licenced under the terms of the GNU GPL v3.0 or later
#
import asyncio
import logging
import re

from config.config import Config
from core.logger import *


class Automator(object):
    def run(self):
        SYSTEM_LOGGER.level = LOG_ERROR
        self.loop = asyncio.get_event_loop()
        logging.basicConfig(level=logging.DEBUG)
        self.loop.set_debug(False)
        self.config = Config(self)
        # print(self.loop)
        self.config.set_async_loop(self.loop)
        # self.gateway = AsyncIOGateway(self.loop)
        # asyncio.ensure_future(self.gateway.run(), loop=self.loop)
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            return
        # # initializes the web server
        # addr = ('', 8000)
        # self.web = OpenWeb(self, addr)

        # self.web.default_route(website.ow_static.OW_static)
        # self.web.register_routes(
        #     [
        #         ["^/$", website.ow_index.OW_index],
        #         ["^/API/ping$", website.ow_index.OW_ping],
        #         ["^/API/config$", website.ow_config.OW_config],
        #         ["^/API/ScanIds$", website.ow_scan_ids.OW_scan_ids],
        #         ["^/API/add_system(.*)$",
        #             website.ow_add_system.OW_add_system],
        #         ["^/API/GeneralOff$", website.ow_general_off.OW_general_off],
        #         ["^/API/temperatures(.*)$",
        #          website.ow_temperatures.OW_list_temperatures],
        #     ]
        # )

        # self.system_loop.add_task(self.web)


# main program
if __name__ == '__main__':
    # create the application object, run the main loop
    a = Automator()
    a.run()
