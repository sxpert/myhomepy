# -*- coding: utf-8 -*-
import json
import threading

import core.core_json_encoder as cje
from core.logger import *

from . import gateway, system, systems, tls

CONFIG_FILE_NAME = 'config.json'


class Config(object):
    app = None
    _file_lock = None

    def __init__(self, app, config_file=None):
        self.log = get_logger(LOG_INFO, '[CONF]', COLOR_YELLOW)
        self.log('Initializing configuration')
        self.app = app
        if config_file is None:
            self.config_file = CONFIG_FILE_NAME
        self.tls = tls.Tls(self)
        self.systems = systems.Systems(self)
        self._file_lock = threading.RLock()
        self.load_file(self.config_file)

    def set_async_loop(self, al):
        self.async_loop = al
        self.systems.run()

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

    def __to_json__(self):
        data = {}
        data['tls'] = self.tls
        data['systems'] = self.systems
        return data

    def save(self):
        # get all data, if it crashes, no harm done to the
        # existing config file
        json_data = cje.dumps(self, indent=4)
        # dump the data to the file (this should not crash)
        self._file_lock.acquire()
        f = open(self.config_file, 'w')
        f.write(json_data)
        f.close()
        self._file_lock.release()

    def add_system(self, ip, port, password):
        # search if we already have this system
        # TODO: restore this functionnality

        # for s in self.systems:
        #     # TODO: fix
        #     try:
        #         gw = s['gateway']
        #     except KeyError:
        #         self.log("no gateway entry in system")
        #         continue
        #     try:
        #         gw_ip = gw['ip']
        #         gw_port = gw['port']
        #         gw_password = gw['password']
        #     except KeyError as e:
        #         self.log("gateway entry missing one of (ip, port, password)")
        #         continue
        #     if gw_ip == ip and gw_port == port and gw_password == password:
        #         self.log("a system with identical values has already been "
        #                  "configured")
        #         return False
        # # couldn't find system
        openwebnet_gateway = gateway.Gateway(ip, port, password)
        new_system = system.System(self.log)
        new_system.set_gateway(openwebnet_gateway)
        self.systems.append(new_system)
        new_system.run()
        self.save()

    @property
    def nb_systems(self):
        return len(self.systems)
