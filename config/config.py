# -*- coding: utf-8 -*-
import json
import asyncio

import core.core_json_encoder as cje
from core.logger import (get_logger, LOG_INFO, COLOR_YELLOW)

import webserver
from . import system, systems, tls

CONFIG_FILE_NAME = 'config.json'


class Config(object):
    app = None
    _file_lock = None

    def __init__(self, app, config_file=None, loop=None):
        self.log = get_logger(LOG_INFO, '[CONF]', COLOR_YELLOW)
        self.log('Initializing configuration')

        # queue for websocket listeners
        self._websockets = []

        self.app = app
        if config_file is None:
            self.config_file = CONFIG_FILE_NAME

        self.web = webserver.WebServer(config=self)
        self.tls = tls.Tls(self)
        self.systems = systems.Systems(self)

        self.load_file(self.config_file)

    @property
    def async_loop(self):
        if self.app is None:
            return None
        l = getattr(self.app, 'loop', None)
        return l

    # ========================================================================
    #
    # loading the configuration from file
    #
    # ========================================================================

    def load_file(self, file):
        try:
            f = open(file, 'r')
        except IOError as e:
            if e.errno == 2:
                self.log('unable to find a configuration file to load')
        else:
            self.log('configuration file opened successfully')
            # read the configuration file
            d = f.read()
            f.close()
            self.loads(d)

    def loads(self, data):
            if len(data) > 0:
                data = json.loads(data)
                if type(data) is dict:
                    k = data.keys()
                    if 'web' in k:
                        self.web.loads(data['web'])
                    if 'tls' in k:
                        self.tls.loads(data['tls'])
                    if 'systems' in k:
                        self.systems.loads(data['systems'])
                else:
                    self.log("invalid configuration format")
            else:
                self.log("WARNING: configuration file is empty")

    # ========================================================================
    #
    # saving the configuration from file
    #
    # ========================================================================

    def __to_json__(self):
        data = {}
        data['web'] = self.web
        data['tls'] = self.tls
        data['systems'] = self.systems
        return data

    def save(self):
        json_data = cje.dumps(self, indent=4)
        f = open(self.config_file, 'w')
        f.write(json_data)
        f.close()

    # ========================================================================
    #
    # manage websocket handlers
    #
    # ========================================================================
    
    async def websocket_dispatch(self, obj):
        """
        Takes an object, and sends it to all registered websocket queues
        """
        self.log('Config.websocket_dispatch %s' % (str(obj)))
        for ws in self._websockets:
            # don't send if the websocket is closing...
            if not ws.closed:
                self.log('pushing to %s' % (str(ws)))
                if hasattr(obj, 'web_data'):
                    obj = obj.web_data
                try:
                    await ws.send_json(obj)
                except TypeError:
                    self.log('ERROR: %s can\'t be converted to json' % (str(obj)))
                except Exception as e:
                    self.log('Error: %s'%(str(e)))

    def websocket_send(self, msg):
        loop = asyncio.get_event_loop()
        asyncio.ensure_future(self.websocket_dispatch(msg), loop=loop)

    def websocket_register(self, ws):
        """
        Registers a queue for a websocket connection to receive messages on
        """
        self.log('websocket %s registered' % (str(ws)))
        self._websockets.append(ws)

    def websocket_unregister(self, ws):
        """
        Removes the given queue from the list of queues
        """
        self.log('unregister websocket %s' % (str(ws)))

    async def websocket_close_all(self):
        for ws in self._websockets:
            self.log('closing websocket %s' % (str(ws)))
            await ws.close()

    # ========================================================================
    #
    # start all tasks (only 2 for now)
    #
    # ========================================================================

    def run(self):
        # time to save the configuration
        self.save()
        self.web.run()
        self.systems.run()

    @property
    def nb_systems(self):
        return len(self.systems)
