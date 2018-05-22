# -*- coding: utf-8 -*-
import json
import threading

import core.core_json_encoder as cje
from core.logger import *

import webserver
from . import system, systems, tls

CONFIG_FILE_NAME = 'config.json'


class Config(object):
    app = None
    _file_lock = None

    def __init__(self, app, config_file=None, loop=None):
        self.log = get_logger(LOG_INFO, '[CONF]', COLOR_YELLOW)
        self.log('Initializing configuration')

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
                    if 'webserver' in k:
                        # webserver configuration data
                        pass
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
    # loading the configuration from file
    #
    # ========================================================================

    def __to_json__(self):
        data = {}
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
    # start all tasks (only 2 for now)
    #
    # ========================================================================

    def run(self):
        self.web.run()
        self.systems.run()

    @property
    def nb_systems(self):
        return len(self.systems)
