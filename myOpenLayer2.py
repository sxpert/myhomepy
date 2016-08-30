#!/usr/bin/python2.7 -3
#-*- coding: utf-8 -*-

#
# (c) Raphael Jacquot 2014
# Licenced under the terms of the GNU GPL v3.0 or later
#

import config
import json
import myOpenLayer1
import re

SYSTEM__LIGHTING            = 1
SYSTEM__TEMP_CONTROL        = 4
SYSTEM__DIAG__LIGHTING      = 1001
SYSTEM__DIAG__TEMP_CONTROL  = 1004

class Monitor (object) :
    COMMAND                   = 0
    STATUS                    = 1
    MSG_TYPES                 = [ 'Command', 'Status', ]

    LIGHTING__OFF             = 0
    LIGHTING__ON              = 1

    TEMP_CONTROL__REPORT_TEMP = 0

    def __init__ (self, system_loop) :
        self.sl = system_loop
        # prepare the app startup
        self.routes = [ { '1' : self.cmd_lighting, },
                        { '4' : self.status_tempcontrol}, ]
        # initializes callbacks
        self.callbacks = None
        self.monitor_socket = myOpenLayer1.OwnSocket(
                config.host,
                config.port,
                config.password,
                myOpenLayer1.OwnSocket.MONITOR)
        # set the callback to get messages from the layer 1
        self.monitor_socket.set_data_callback(self.data_callback)
        # add the monitor socket to the system loop
        self.sl.add_socket(self.monitor_socket)

    def log (self, msg) :
        msg = unicode(msg)
        if self.monitor_socket is not None: 
            self.monitor_socket.log (msg)
        else:
            print (msg)
    
    def get_number (self, msg) :
        v = '' 
        while True :
            if len(msg) == 0 :
                break
            c = msg[0]
            if c >= '0' and c <= '9' :
                v += c
                msg = msg[1:]
            else :
                break
        return v, msg

    def data_callback (self, msg) :
        msgtype = None
        # skip useless *1001*3*0## frame
        if msg == '*1001*3*0##':
            return
        # analyze the content of messages passed from the layer 1
        m = re.match('^\*(?P<who>\d+)(?P<msg>\*.*)', msg)
        if m is not None :
            msgtype = self.COMMAND
        else :
            m = re.match('^\*#(?P<who>\d+)(?P<msg>\*.*)', msg)
            if m is not None :
                msgtype = self.STATUS
        if msgtype is not None :
            r = self.routes[msgtype]
            who, msg = m.groups()
            if who in r :
                func = r[who]
                if func is not None :
                    func (msg)
                    return
            msg = 'found '+self.MSG_TYPES[msgtype]+' message \''+who+'\' remains \''+msg+'\''
        else :
            msg = 'Unknown first character in message '+msg
        # log something
        self.log (msg)

    #
    # api to higher level layers
    # 
    def register_callback (self, system, order, device, callback):
        if self.callbacks is None :
            self.callbacks={}
        # generate callback key
        k = unicode(system)+'-'+unicode(order)+'-'
        if system == SYSTEM__LIGHTING:
            if (type(device) is dict) and ('group' in device.keys()):
                k+='G-'+unicode(device['group'])
        if system == SYSTEM__TEMP_CONTROL:
            if (type(device) is dict) and ('zone' in device.keys()) and ('sensor' in device.keys()):
                k+='['+unicode(device['zone'])+'-'+unicode(device['sensor'])+']'
        self.callbacks[k] = callback
        #print (unicode(self.callbacks))

    def execute_callback (self, system, order, device, data=None):
        k = unicode(system)+'-'+unicode(order)+'-'
        if system == SYSTEM__LIGHTING:
            if (type(device) is dict) and ('group' in device.keys()):
                k+='G-'+unicode(device['group'])
        if system == SYSTEM__TEMP_CONTROL:
            if (type(device) is dict) and ('zone' in device.keys()) and ('sensor' in device.keys()):
                k+='['+unicode(device['zone'])+'-'+unicode(device['sensor'])+']'
        if k in self.callbacks.keys() :
            func = self.callbacks[k]
            func (device, data)

    #------------------------------------------------------------------------------------------------------------------
    #
    # message parsers by system, calls appropriate registered callbacks
    #

    # Lighting systems

    def cmd_lighting (self, msg) :
        # light command
        # '*0*#1##'
        m = re.match('^\*(?P<command>[01])\*(?P<light>\d{2,4})##$',msg)
        if m is not None:
            data = m.groupdict()
            self.log (unicode(data))
            device = { 'light': data['light'] }
            self.execute_callback(SYSTEM__LIGHTING, data['command'], device, None)
            return
        m = re.match('^\*(?P<command>[01])\*#(?P<group>\d{1,3})##$',msg)
        if m is not None:
            data = m.groupdict()
            self.log (unicode(data))
            device = { 'group': data['group'] }
            self.execute_callback(SYSTEM__LIGHTING, data['command'], device, None)
            return
        self.log ('lighting command '+msg)

    # Temperature control systems

    def status_tempcontrol (self, msg) :
        # temperature report
        # '101*0*0270##'
        m = re.match('^\*(?P<probe>\d{3})\*0\*(?P<temperature>\d{4})##$',msg)
        if m is not None:
            data = m.groupdict()
            self.log (unicode(data))
            # generate the device key
            zone = int(data['probe'][0])
            sensor = int(data['probe'][1:])
            device = { 'zone': zone, 'sensor': sensor }
            temp = float(data['temperature'])/10.0
            data = { 'temp': temp, 'unit': '°C' }
            self.execute_callback(SYSTEM__TEMP_CONTROL, self.TEMP_CONTROL__REPORT_TEMP, device, data)
            return
        self.log ('temp control status '+msg)

        
    #------------------------------------------------------------------------------------------------------------------
    #
    # system scanning
    #

class Scanner (object):

    def __init__ (self, system_loop, ready):
        self.devices=[]
        self.sl = system_loop
        self.sock = myOpenLayer1.OwnSocket(
                config.host,
                config.port,
                config.password,
                myOpenLayer1.OwnSocket.COMMAND)
        # set the callback to get messages from the layer 1
        self.sock.set_ready_callback(ready)
        # add the monitor socket to the system loop
        self.sl.add_socket(self.sock)

    def get_diag_system(self, system):
        if system == SYSTEM__LIGHTING:
            return SYSTEM__DIAG__LIGHTING
        if system == SYSTEM__TEMP_CONTROL:
            return SYSTEM__DIAG__TEMP_CONTROL

    def init_scan (self, system, finish):
        self.finish_callback = finish
        self.current_system = system
        self.sock.set_data_callback(self.read_serials)
        self.sock.send("*#"+unicode(self.get_diag_system(self.current_system))+"*0*13##")

    def read_serials (self, msg):
        self.sock.log (msg)
        # parse the *#1001*0*13*[mac address in decimal]## messages
        m = re.match('^\*#'+unicode(self.get_diag_system(self.current_system))+'\*(?P<address>\d+)\*13\*(?P<macaddr>\d+)##$',msg)
        if m is not None:
            data = m.groupdict()
            self.sock.log('mac address '+unicode(data['macaddr']))
            self.devices.append({'system': self.current_system, 'macaddr': int(data['macaddr'])})
            return
        if msg==self.sock.ACK:
            self.sock.log(unicode(self.devices))
            self.current_device = 0
            self.select_device ()

    def select_device (self):
        dev = self.devices[self.current_device]
        self.sock.set_data_callback(self.confirm_selected)
        self.sock.send("*"+unicode(self.get_diag_system(self.current_system))+"*10#"+unicode(dev['macaddr'])+"*0##")

    def confirm_selected (self, msg):
        if msg==self.sock.ACK:
            # request the config to be sent
            self.sock.set_data_callback(self.receive_conf)
            self.sock.send("*#"+unicode(self.get_diag_system(self.current_system))+"*0*38#0##")
        else:
            # in case we don't get an ACK here...              
            dev = self.devices[self.current_device]
            self.sock.log ("ERROR while attempting to select device with ID "+unicode(dev['macaddr']))
            self.finish ()

    def receive_conf (self, msg):
        self.sock.log (msg)
        d = self.devices[self.current_device]
        if 'data' in d.keys():
            v = d['data']
        else:
            v = []
        v.append(msg)
        d['data'] = v
        self.devices[self.current_device] = d

        if msg==self.sock.ACK:
            # end of config data for this device
            self.current_device+=1
            if self.current_device < len(self.devices):
                self.select_device()
            else:
                self.finish_callback()
    
    def finish (self):
        f = open('devices.txt','w')
        f.write (json.dumps(self.devices, indent=4))
        f.close ()
        self.sl.remove_socket(self.sock)
        self.sock.close()
