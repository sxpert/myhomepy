#!/usr/bin/python
import json
import myOpenLayer1
from config import config

#
# takes data from actions.json
# executes the series of requests
#
class ActionEngine (object):
    def __init__ (self, logger = None):
        self.logger = logger
        # load the json
        f = open("actions.json", "r")
        s = f.read()
        f.close()
        self._proto = json.loads(s)
        if "version" not in self._proto:
            self.log ("ERROR: unable to find protocol database version data")
            return
        self.log ("Open protocol version "+self._proto["version"]+" loaded")

    def log (self, msg):
        col_in = '\033[93m'
        col_out = '\033[0m'
        s = "[ActionEngine] " + col_in + unicode(msg) + col_out
        if self.logger is None: 
            print (s)
        else:
            self.logger.log (s)

    def run (self, context):
        self.context = context
    
    def ready_callback (self, ownsock):
        self.log ("ActionEngine ready")
        self.ownsock = ownsock
        # start the scenario
        self.start_scenario ()

    def data_callback (self, msg):
        self.log ("ActionEngine data")

    def start_scenario (self):
        if "scenario" not in self.context:
            self.log ("ERROR: no scenario defined in context - aborting")
            return
        self.scenario_name = self.context["scenario"]
        # find scenario data
        if "scenarios" not in self._proto:
            self.log ("ERROR: can't find scenarios in protocol database - aborting")
            return
        scenarios = self._proto["scenarios"]
        if self.scenario_name not in scenarios:
            self.log ("ERROR: can't find scenario '"+self.scenario_name+"' in protocol database - aborting")
            return
        self.scenario = scenarios[self.scenario_name]
        self.log (self.scenario)

class ScanNetwork (object):
    def __init__ (self, logger = None):
        self.logger = logger
        self.ae = ActionEngine(logger)
        context = {}
        context["scenario"] = "ScanByAID"
        data = {}
        data["who"] = "1001"
        context["data"] = data
        self.ae.run (context)

    @property
    def ready_callback (self):
        return self.ae.ready_callback

    @property
    def scan_callback (self):
        return self.ae.data_callback

if __name__ == "__main__":
    logger = myOpenLayer1.system_logger
    sl = myOpenLayer1.MainLoop(logger)
    sn = ScanNetwork(logger)
    config.set_main_loop(sl)
    cs = config.command_socket(config.nb_systems-1, sn.ready_callback, sn.scan_callback)
    sl.add_socket(cs)
    sl.run ()
