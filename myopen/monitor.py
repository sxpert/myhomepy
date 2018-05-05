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

import database

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
        self.log("Known systems :")
        for s in SubSystems:
            subsystem = s()
            self.log("    %s (%d)" % (
                     subsystem.__class__.__name__,
                     subsystem.SYSTEM_WHO))
        # end of system info

        # TODO: move this
        # initializes callbacks
        self.update_callbacks(system)

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

    #
    # getters and setters
    # this should be from system...
    #
    @property
    def database(self):
        try:
            db = self._db
        except AttributeError:
            if self.system.database is None:
                self.log("WARNING: unable to find a value for "
                         "\'database\' in the config for the system")
                return None
            # open database, and store a link
            self._db = database.Database(self.system.database, self.log)
            return self._db
        else:
            return db

    # ----------------------------------------------------------------------------------------------
    # this is called for each open web net packet received
    #
    def data_callback(self, msg):
        message = Message(msg, self)
        message.dispatch()

    # ----------------------------------------------------------------------------------------------
    # managing callbacks
    #

    def update_callback(self, key, action):
        if self.callbacks is None:
            self.callbacks = {}
        self.callbacks[key] = action

    def register_callback(self, system, order, device, callback, params):
        k = self.callback_key(system, order, device)
        self.log("callback key %s => %s %s" % (k, callback, params))
        self.update_callback(k, (callback, params,))

    def execute_callback(self, system, order, device, data=None):
        if self.callbacks is None:
            self.log("no callbacks found")
            return
        k = self.callback_key(system, order, device)
        if k in self.callbacks.keys():
            func, params = self.callbacks[k]
            # self.log("found callback %s %s" % (str(func), str(params)))
            func(self, params, device, data)
        else:
            self.log("ERROR: key %s not in callbacks" % (k))

    def callback_key(self, system, order, device):
        k = str(system)+"-"+str(order)
        dk = None
        for s in SubSystems:
            if s.SYSTEM_WHO == system:
                dk = s().map_device(device)
                break
        if dk is None:
            self.log("unable to map device %s" % (str(device)))
            return None
        key = k+"-"+dk
        return key

    # ----------------------------------------------------------------------------------------------
    # mapping functions to parse the configuration
    #
    #

    def map_key(self, conditions):
        # system
        if "system" not in conditions.keys():
            self.log("WARNING: condition has no system")
            return None
        system = conditions["system"]
        # search for system in all parser SYSTEM_NAME variables
        sys = None
        for s in SubSystems:
            if hasattr(s, 'SYSTEM_NAME') and s.SYSTEM_NAME == system:
                sys = s()
        if not sys:
            self.log("WARNING: unknown system \'"+system+"\'")
            return None
        system = sys.SYSTEM_WHO
        orders = sys.SYSTEM_CALLBACKS
        self.log('subsystem %s (%d) => %s' % (
                 sys.__class__.__name__,
                 system, str(orders)))

        # order
        if "order" not in conditions:
            self.log("WARNING: conditions has no system")
            return None
        order = conditions["order"]
        if order not in orders.keys():
            self.log("WARNING: unknown order \'"+order+"\'")
            return None
        order = orders[order]

        # device
        if "device" not in conditions:
            self.log("WARNING: conditions has no device")
            return None
        device = conditions["device"]

        return self.callback_key(system, order, device)

    def map_action(self, conditions):
        # check for presence of proper variables
        if "action" not in conditions.keys():
            self.log("WARNING: condition has no action")
            return None
        action = conditions["action"]
        if "plugin" not in action:
            self.log("WARNING: no plugin definition in action")
            return None
        plugin = action["plugin"]
        if "module" not in plugin:
            self.log("WARNING: no module defined for plugin")
            return None
        module = plugin["module"]
        if "method" not in plugin:
            self.log("WARNING: no method defined for plugin")
            return None
        method = plugin["method"]
        params = None
        if "params" in action:
            params = action["params"]

        plugins_paths = PLUGINS_DIRS.split(os.pathsep)
        sys.path.extend(plugins_paths)
        # find the file
        m = None
        for path in plugins_paths:
            for filename in os.listdir(path):
                name, ext = os.path.splitext(filename)
                if ext.endswith(".py") and (name == module):
                    m = __import__(name, globals())
        # find method
        func = getattr(m, method)
        if params is not None:
            return (func, params,)
        else:
            return func

    # ----------------------------------------------------------------------------------------------
    # update all callbacks when reloading the configuration
    #

    def update_callbacks(self, system):
        if system.callbacks is None:
            return
        callbacks = system.callbacks
        for cb in callbacks:
            # generate the key
            ck = self.map_key(cb["conditions"])
            action = self.map_action(cb)
            if (ck is not None) and (action is not None):
                self.update_callback(ck, action)
            else:
                self.log("WARNING: problem while parsing callback definition")
        self.log("Callbacks updated")

    def send_command(self, command=CommandDialog):
        socket = command(self.monitor_socket)
        self.log("sending command %s" % (socket.__class__.__name__))
        self.system.main_loop.add_task(socket)
        socket.start()
        return True
