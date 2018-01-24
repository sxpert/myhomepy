#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

from config import config
from myopen import layer1
from actions import *

if __name__ == "__main__":
    logger = layer1.SYSTEM_LOGGER
    sl = layer1.MainLoop(logger)
    config.set_main_loop(sl)
    sn = actions.ScanNetwork(logger)
    cs = config.command_socket(config.nb_systems-1, sn.ready_callback, sn.data_callback)
    sl.add_task(cs)
    sl.run ()
