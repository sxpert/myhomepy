# -*- coding: utf-8 -*-

import json

from core.logger import SYSTEM_LOGGER

from . import gateway, system, systems, tls

CONFIG_FILE_NAME = 'config.json'


class Config():
    app = None

    def __init__(self, app, config_file=None):
        self.app = app
        if config_file is None:
            self.config_file = CONFIG_FILE_NAME
        self.tls = tls.Tls(self)
        self.systems = systems.Systems(self)
        self.load_file(self.config_file)

    def log(self, msg):
        msg_s = '[CONF] '+str(msg)
        SYSTEM_LOGGER.log(msg_s)

    # sets the main loop
    # starts up all loaded systems
    def set_main_loop(self, ml):
        self.main_loop = ml
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
            self.load(d)

    def load(self, data):
            if len(data) > 0:
                data = json.loads(data)
                if type(data) is dict:
                    k = data.keys()
                    if 'tls' in k:
                        self.tls.load(data['tls'])
                    if 'systems' in k:
                        self.systems.load(data['systems'])
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
        f = open(self.config_file, 'w')
        # f.write(self.json())
        f.close()

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
