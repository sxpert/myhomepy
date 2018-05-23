#!/usr/bin/env python3
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
from core.logger import SYSTEM_LOGGER, LOG_ERROR, LOG_INFO, LOG_DEBUG


class Automator(object):
    def run(self):
        SYSTEM_LOGGER.level = LOG_INFO
        SYSTEM_LOGGER.logfile = 'myopen.log'
        self.loop = asyncio.get_event_loop()
        logging.basicConfig(level=logging.DEBUG)
        self.loop.set_debug(False)
        self.config = Config(self, loop=self.loop)
        self.config.run()
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            tasks = asyncio.gather(
                        *asyncio.Task.all_tasks(loop=self.loop),
                        loop=self.loop,
                        return_exceptions=True)
            tasks.add_done_callback(lambda t: self.loop.stop())
            tasks.cancel()
            return


# main program
if __name__ == '__main__':
    # create the application object, run the main loop
    a = Automator()
    a.run()
