#!/usr/bin/python2.7 -3
# -*- coding: utf-8 -*-

#
# (c) Raphael Jacquot 2014
# Licenced under the terms of the GNU GPL v3.0 or later
#

import re
import os
import sys
import json

import config
from . import layer1

PLUGINS_DIRS = "plugins/"

SYSTEM__LIGHTING = 1
SYSTEM__TEMP_CONTROL = 4
SYSTEM__GATEWAY = 13
SYSTEM__DIAG__LIGHTING = 1001
SYSTEM__DIAG__TEMP_CONTROL = 1004

LIGHTING__OFF = 0
LIGHTING__ON = 1

TEMP_CONTROL__REPORT_TEMP = 0

SYSTEM_NAMES = {
    "LIGHTING": {
        "id": SYSTEM__LIGHTING,
        "orders": {
            "OFF": LIGHTING__OFF,
            "ON":  LIGHTING__ON
        }
    },
    "TEMP_CONTROL": {
        "id": SYSTEM__TEMP_CONTROL,
        "orders": {
            "REPORT_TEMP": TEMP_CONTROL__REPORT_TEMP
        }
    }
}


def map_device_lighting(device):
    if (type(device) is dict) and ('group' in device.keys()):
        return 'G-'+str(device['group'])
    return None


def map_device_temp_control(device):
    if (type(device) is dict) and \
       ('zone' in device.keys()) and \
       ('sensor' in device.keys()):
        return '['+str(device['zone'])+'-'+str(device['sensor'])+']'
    return None

DEVICE_MAPPINGS = {
    SYSTEM__LIGHTING:       map_device_lighting,
    SYSTEM__TEMP_CONTROL:   map_device_temp_control
}


class OWNMonitor(object):
    COMMAND = 0
    STATUS = 1
    MSG_TYPES = ['Command', 'Status', ]

    def __init__(self, system_loop, system_id):
        self.system_id = system_id
        self.plugins = None
        self.sl = system_loop
        # prepare the app startup
        self.routes = [{'1': self.cmd_lighting},
                       {'4': self.status_tempcontrol,
                        '13': self.status_gateway}, ]
        # initializes callbacks
        self.callbacks = None
        system = config.config[system_id]
        gw = system['gateway']
        self.monitor_socket = layer1.OwnSocket(
                gw['ip'],
                gw['port'],
                gw['password'],
                layer1.OwnSocket.MONITOR)
        # set the callback to get messages from the layer 1
        self.monitor_socket.set_data_callback(self.data_callback)
        self.update_callbacks(system)
        # add the monitor socket to the system loop
        self.sl.add_task(self.monitor_socket)

    def log(self, msg):
        msg = str(msg)
        if self.monitor_socket is not None:
            self.monitor_socket.log(msg)
        else:
            print (msg)

    #
    # getters and setters
    #
    @property
    def database(self):
        try:
            db = self._db
        except AttributeError as e:
            system = config.config[self.system_id]
            if "database" not in system.keys():
                self.log("WARNING: unable to find a value for "
                         "\'database\' in the config for the system")
                return None
            db_name = system["database"]
            # open database, and store a link
            import database
            self._db = database.Database(db_name, self.log)
            return self._db
        else:
            return db

    # ----------------------------------------------------------------------------------------------
    # this is called for each open web net packet received
    # parses the packet type, and calls the right function depending on the
    # source.
    # logs the packet as is if not understood
    #
    def data_callback(self, msg):
        msgtype = None
        # skip useless *1001*3*0## frame
        if msg == '*1001*3*0##':
            return
        # analyze the content of messages passed from the layer 1
        m = re.match('^\*(?P<who>\d+)(?P<msg>\*.*)', msg)
        if m is not None:
            msgtype = self.COMMAND
        else:
            m = re.match('^\*#(?P<who>\d+)(?P<msg>\*.*)', msg)
            if m is not None:
                msgtype = self.STATUS
        if msgtype is not None:
            r = self.routes[msgtype]
            who, msg = m.groups()
            if who in r:
                func = r[who]
                if func is not None:
                    func(msg)
                    return
            msg = 'found ' + self.MSG_TYPES[msgtype] + ' message \'' + who + \
                  '\' remains \'' + msg + '\''
        else:
            msg = 'Unknown first character in message '+msg
        # log something
        self.log(msg)

    # ----------------------------------------------------------------------------------------------
    # managing callbacks
    #

    def update_callback(self, key, action):
        if self.callbacks is None:
            self.callbacks = {}
        self.callbacks[key] = action

    def register_callback(self, system, order, device, callback, params):
        k = self.callback_key(system, order, device)
        self.update_callback(k, (callback, params,))

    def execute_callback(self, system, order, device, data=None):
        if self.callbacks is None:
            return
        k = self.callback_key(system, order, device)
        if k in self.callbacks.keys():
            func, params = self.callbacks[k]
            func(self, params, device, data)

    def callback_key(self, system, order, device):
        k = str(system)+"-"+str(order)
        dk = DEVICE_MAPPINGS[system](device)
        if dk is None:
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
        if system not in SYSTEM_NAMES.keys():
            self.log("WARNING: unknown system \'"+system+"\'")
            return None
        sys = SYSTEM_NAMES[system]
        system = sys["id"]
        orders = sys["orders"]

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
        if "callbacks" not in system.keys():
            system["callbacks"] = []
        callbacks = system["callbacks"]
        for cb in callbacks:
            print (str(cb))
            # generate the key
            ck = self.map_key(cb["conditions"])
            print (str(ck))
            action = self.map_action(cb)
            if (ck is not None) and (action is not None):
                print ("action", action)
                self.update_callback(ck, action)
            else:
                self.log("WARNING: problem while parsing callback definition")
        print ("Callbacks updated")

    # ------------------------------------------------------------------------------------------------------------------
    #
    # message parsers by system, calls appropriate registered callbacks
    #

    # Lighting systems

    def cmd_lighting(self, msg):
        # light command
        # '*0*#1##'
        m = re.match('^\*(?P<command>[01])\*(?P<light>\d{2,4})##$', msg)
        if m is not None:
            data = m.groupdict()
            self.log(str(data))
            device = {'light': data['light']}
            self.execute_callback(SYSTEM__LIGHTING,
                                  data['command'],
                                  device, None)
            return
        m = re.match('^\*(?P<command>[01])\*#(?P<group>\d{1,3})##$', msg)
        if m is not None:
            data = m.groupdict()
            self.log(str(data))
            device = {'group': data['group']}
            self.execute_callback(SYSTEM__LIGHTING,
                                  data['command'],
                                  device, None)
            return
        self.log('lighting command '+msg)

    # Temperature control systems

    def status_tempcontrol(self, msg):
        # temperature report
        # '101*0*0270##'
        m = re.match('^\*(?P<probe>\d{3})\*0\*(?P<temperature>\d{4})##$', msg)
        if m is not None:
            data = m.groupdict()
            js_data = json.dumps(data)
            self.log(js_data)
            # generate the device key
            zone = int(data['probe'][0])
            sensor = int(data['probe'][1:])
            device = {'zone': zone, 'sensor': sensor}
            temp = float(data['temperature'])/10.0
            data = {'temp': temp, 'unit': '°C'}
            self.execute_callback(SYSTEM__TEMP_CONTROL,
                                  TEMP_CONTROL__REPORT_TEMP,
                                  device, data)
            return
        self.log('temp control status ' + msg)

    # gateway

    def status_gateway(self, msg):
        self.log('gateway status ' + msg)

    def send_command(self, command):
        print("sending command", command)
        return True
