#
# (c) Raphael Jacquot 2014
# Licenced under the terms of the GNU GPL v3.0 or later
#

CONFIG_FILE_NAME = 'config.json'

import json
import myOpenLayer1

class Config (object):
    def __init__ (self, config_file=None):
        if config_file is None:
            self.config_file = CONFIG_FILE_NAME
        self.systems = []
        self.monitors = []
        self.load()

    def log(self, msg):
        myOpenLayer1.system_logger.log ('[CONF] '+msg)

    # sets the main loop
    # starts up all loaded systems
    def set_main_loop(self, ml):
        self.main_loop = ml
        for sys_id in range(0, len(self.systems)):
            self._add_system(sys_id)

    def load(self):
        try: 
            f = open(self.config_file, 'r')
        except IOError as e:
            if e.errno == 2:
                self.log ('unable to find a configuration file to load')
        else:
            self.log ('configuration file opened successfully')
            # read the configuration file
            d = f.read()
            f.close()
            self.systems = json.loads(d)
        
    def save(self):
        f = open(self.config_file, 'w')
        f.write(json.dumps(self.systems))
        f.close()

    def __len__(self):
        return len(self.systems)

    def __getitem__(self, key):
        # key must be an integer, between 0 and len-1
        return self.systems[key]

    def add_system (self, ip, port, password):
        #search if we already have this system
        for s in self.systems:
            try:
                gw = s['gateway']
            except KeyError:
                self.log("no gateway entry in system")
                continue
            try:
                gw_ip = gw['ip']
                gw_port = gw['port']
                gw_password = gw['password']
            except KeyError as e:
                self.log("gateway entry missing one of (ip, port, password)")
                continue
            if gw_ip==ip and gw_port==port and gw_password==password:
                self.log("a system with identical values has already been configured")
                return False
        # couldn't find system
        system = {}
        gateway = {}
        gateway['ip'] = ip
        gateway['port'] = port
        gateway['password'] = password
        system['gateway'] = gateway
        sys_id = len(self.systems)
        self.systems.append(system)
        self.save()
       
        self._add_system(sys_id)

    def _add_system(self, sys_id):    
        self.log("added system with system id="+unicode(sys_id))
        import myOpenLayer2
        sys = myOpenLayer2.OWNMonitor(self.main_loop, sys_id)
        self.monitors.append(sys)

config = Config()
