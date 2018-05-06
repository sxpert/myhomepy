#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
# (c) Raphael Jacquot 2014
# Licenced under the terms of the GNU GPL v3.0 or later
#

import json
import os
import re
import sys

from .dialog import CommandDialog
from .message import Message
from .subsystems import SubSystems

PLUGINS_DIRS = "plugins/"


class OWNMonitor(object):
    system = None
    plugins = None
    callbacks = None
    monitor_socket = None

    def __init__(self, system):
        self.system = system

        # system information
        self.log("OWNMonitor.__init__ Known systems :")
        for s in SubSystems:
            subsystem = s()
            self.log("    %s (%d)" % (
                     subsystem.__class__.__name__,
                     subsystem.SYSTEM_WHO))
        # end of system info

        self.monitor_socket = system.socket(system.MONITOR)
        self.monitor_socket.set_data_callback(self.data_callback)

        # add the monitor socket to the system loop
        self.system.main_loop.add_task(self.monitor_socket)

    def log(self, msg):
        msg = str(msg)
        if self.monitor_socket is not None:
            self.monitor_socket.log(msg)
        elif self.system is not None:
            self.system.log(msg)
        else:
            print(msg)

    # ----------------------------------------------------------------------------------------------
    # this is called for each open web net packet received
    #
    def data_callback(self, msg):
        message = Message(msg, self)
        message.dispatch()

    def send_command(self, command=CommandDialog):
        socket = command(self.monitor_socket)
        self.log("OWNMonitor.send_command %s" % (socket.__class__.__name__))
        self.system.main_loop.add_task(socket)
        socket.start()
        return True
