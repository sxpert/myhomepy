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
import threading

from .socket import OWNSocket

from .dialog import CommandDialog
from .message import Message
from .subsystems import SubSystems

PLUGINS_DIRS = "plugins/"


class OWNMonitor(OWNSocket):
    system = None
    plugins = None
    callbacks = None

    def __init__(self, system):
        self.system = system
        self.mode = self.MONITOR

        # system information
        self.log("OWNMonitor.__init__ Known systems :")
        for s in SubSystems:
            subsystem = s()
            self.log("    %s (%d)" % (
                     subsystem.__class__.__name__,
                     subsystem.SYSTEM_WHO))
        # end of system info

        address, port, passwd = system.gateway.socket_info
        super().__init__(address, port, passwd)

        # add self to the system loop
        self.system.main_loop.add_task(self)

    def ready_callback(self):
        self.log("MONITOR is ready")

        # do a scan of system devices
        from .commands import CmdScanDeviceIds
        self.send_command(CmdScanDeviceIds, False)

    # ----------------------------------------------------------------------------------------------
    # this is called for each open web net packet received
    #
    def data_callback(self, msg):
        message = Message(msg, self)
        message.dispatch()

    def send_command(self, command=CommandDialog, wait=True):
        # todo: implement a queue, one command at a time

        socket = command(self)
        event = threading.Event()
        socket.event = event
        self.log("OWNMonitor.send_command %s" % (socket.__class__.__name__))
        self.system.main_loop.add_task(socket)
        socket.start()
        if wait:
            event.wait()
        return socket.success
