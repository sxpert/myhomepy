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
from optparse import OptionParser
from socket import gaierror

from config.config import Config
from core.logger import LOG_DEBUG, LOG_ERROR, LOG_INFO, SYSTEM_LOGGER


class Automator(object):
    def exception_handler(self, loop, context):
        exc = context.get('exception', None)
        if exc is not None:
            if exc.__class__ in (TimeoutError, gaierror, ):
                return
        print(context)

    def __init__(self, options):
        if options.debug:
            SYSTEM_LOGGER.level = LOG_DEBUG
            logging.basicConfig(level=logging.DEBUG)
        else:
            SYSTEM_LOGGER.level = LOG_ERROR
            logging.basicConfig(level=logging.DEBUG)
        SYSTEM_LOGGER.logfile = options.log_file

    def run(self):
        self.loop = asyncio.get_event_loop()
        self.loop.set_debug(False)
        self.loop.set_exception_handler(self.exception_handler)
        self.config = Config(self, loop=self.loop)
        self.config.run()
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            print('closing all websockets')
            self.loop.run_until_complete(self.config.websocket_close_all())
            print('websockets closed')
            tasks = asyncio.gather(
                        *asyncio.Task.all_tasks(loop=self.loop),
                        loop=self.loop,
                        return_exceptions=True)
            tasks.add_done_callback(lambda t: self.loop.stop())
            tasks.cancel()
            return

# main program
if __name__ == '__main__':
    parser = OptionParser()
    parser.set_defaults(config_file='config.json')
    parser.set_defaults(debug=False)
    parser.set_defaults(log_file='myopen.log')
    parser.add_option('-d', '--debug', action='store_true', dest='debug', help='Generate debug output')
    (options, args) = parser.parse_args() 
    # create the application object, run the main loop
    a = Automator(options)
    a.run()
