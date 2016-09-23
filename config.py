#
# (c) Raphael Jacquot 2014
# Licenced under the terms of the GNU GPL v3.0 or later
#

CONFIG_FILE_NAME = 'config.json'

import myOpenLayer1

class Config (object):
    def __init__ (self, config_file=None):
        if config_file is None:
            self.config_file = CONFIG_FILE_NAME
        self.systems = []
        self.load()

    def log(self, msg):
        myOpenLayer1.system_logger.log ('[CONF] '+msg)

    def load(self):
        try: 
            f = open(self.config_file, 'r')
        except IOError as e:
            if e.errno == 2:
                self.log ('unable to find a configuration file to load')
        else:
            self.log ('configuration file opened successfully')
            # read the configuration file
            
    def __len__(self):
        return len(self.systems)

    def __getitem__(self, key):
        # key must be an integer, between 0 and len-1
        return self.systems[key]

config = Config()
