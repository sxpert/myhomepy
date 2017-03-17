#!/usr/bin/python
import myOpenLayer1
from config import config

class ProtoObject (object):
    def __init__ (self, proto = None):
        self._proto = proto
        self._error = False

    def _abort (self, msg):
        self._error = True
        return self._proto.abort (msg)

    def _must (self, varname, dataset, options = None):
        if self._error:
            return None
        if varname not in dataset.keys():
            self._abort ("Unable to find '"+varname+"' item in "+unicode(dataset)+" from "+self.name)
            return None
        v = dataset[varname]
        if options :
            if v in options:
                v = options.index(v)
            else:
                self._abort ("Unable to find '"+v+"' in options "+unicode(options)+" for item '"+varname+"' from "+self.name)
        return v

    def _optional (self, varname, dataset):
        if self._error:
            return None
        if varname in dataset.keys():
            return dataset[varname]
        else:
            return False

    def _boolean (self, varname, dataset):
        v = self._optional (varname, dataset)
        if v is None:
            return False

class Sentence (ProtoObject):
    RX = 0
    TX = 1

    def setup (self, name, data):
        self.name = name
        self.id = self._must ("id", data)
        self.description = self._must ("description", data)
        self.type = self._must ("type", data, ["RX", "TX"])
        self.str = self._must ("str", data)
        self.has_address = self._boolean ("has_address", data)
        self.has_params = self._boolean ("has_params", data)
        self.diag_open = self._boolean ("diag_open", data)
        self.error = self._optional ("error", data)
        return self

    def __repr__ (self):
        return self.str

class SequenceItem (ProtoObject):

    def setup (self, name, data):
        self.name = name
        self.id = self._must ("id", data)
        if self.id not in self._proto.sentences.keys():
            return self._abort ("unable to find "+self.id+" in sentences list")
        self.sentence = self._proto.sentences[self.id]
        self.mandatory = self._boolean ("mandatory", data)
        self.repeat = self._boolean ("repeat", data)
        self.onNAK = self._optional ("onNAK", data)
        self.onERR = self._optional ("onERR", data)
        return self

    def __repr__ (self):
        return unicode(self.sentence)

class Sequence (ProtoObject):

    def setup (self, name, data):
        self.name = name
        self.id = self._must ("id", data)
        ol = self._must ("openlist", data)
        if type(ol) is not list:
            return self._abort ("'openlist' is not list type in sequence '"+name+"'")
        self.openlist = []
        for o in ol:
            self.openlist.append(SequenceItem(self._proto).setup(self.name+" - "+unicode(len(self.openlist)+1), o))
        return self        

    def __repr__ (self):
        return self.name

class ScenarioItem (ProtoObject):

    def setup (self, name, data):
        self.name = name
        self.id = self._must ("id", data)
        if self.id not in self._proto.sequences.keys():
            return self._abort ("Unable to find "+self.id+" in sequences list")
        self.sequence = self._proto.sequences[self.id]
        self.repeat = self._boolean ("repeat", data)
        return self

    def __repr__ (self):
        return unicode(self.sequence)

class Scenario (ProtoObject):
    
    def setup (self, name, data):
        self.name = name
        self.id = self._must ("id", data)
        self.description = self._must("description", data)
        self.type = self._must ("type", data, ["readonly"])
        seq = self._must("sequences", data)
        if type(seq) is not list:
            return self._abort ("'sequences is not list type in scenario '"+name+"'")
        self.sequences = []
        for s in seq:
            self.sequences.append(ScenarioItem(self._proto).setup(self.name+" - "+unicode(len(self.sequences)+1), s))
        self._proto.log ("        "+unicode(self.sequences))
        return self

class Proto (object):
    def __init__ (self, proto, log = None):
        self.error = False
        self._log = log
        if not self.load_sentences (proto):
            return
        if not self.load_sequences (proto):
            return
        if not self.load_scenarios (proto):
            return

    def log (self, msg):
        if self._log is None:
            print (unicode(msg))
        else:
            self._log (msg)
            
    def abort (self, msg):
        self.log ("ERROR: "+msg+" - aborting")
        self.error = True
        return False
    
    def load_sentences (self, proto):
        self.log ("Loading sentences")
        if "sentences" not in proto:
            return self.abort ("unable to find 'sentences' in protocol description file")
        self.sentences = {}
        sentences = proto["sentences"]
        for name in sentences.keys():
            self.log ("    "+name)
            data = sentences[name]
            sentence = Sentence(self).setup(name, data)
            self.sentences[name] = sentence
        return True

    def load_sequences (self, proto):
        self.log ("Loading sequences")
        if "sequences" not in proto:
            return self.abort ("unable to find 'sequences' in protocol description file")
        self.sequences = {}
        sequences = proto["sequences"]
        for name in sequences.keys():
            self.log ("    "+name)
            data = sequences[name]
            sequence = Sequence(self).setup(name, data)
            self.sequences[name] = sequence
        return True
    
    def load_scenarios (self, proto):
        self.log ("Loading scenarios")
        if "scenarios" not in proto:
            return self.abort ("Unable to find 'scenarios' in protocol description file")
        self.scenarios = {}
        scenarios = proto["scenarios"]
        for name in scenarios.keys():
            self.log ("    "+name)
            data = scenarios[name]
            scenario = Scenario(self).setup(name, data)
            self.scenarios[name] = scenario
        return True

#
# takes data from actions.json
# executes the series of requests
#
class ActionEngine (object):
    def __init__ (self, logger = None):
        self.logger = logger
        # load the json
        self.load_protocol_data ("actions.json")

    def load_protocol_data (self, protocol_data_file):
        import json
        f = open(protocol_data_file, "r")
        s = f.read()
        f.close()
        _proto = json.loads(s)
        if "version" not in _proto:
            return self.abort ("unable to find protocol database version data")
        self.log ("Open protocol version "+_proto["version"]+" loaded")
        # parse protocol data into a new object
        self._proto = Proto (_proto, self.log)
    
    def log (self, msg):
        col_in = '\033[93m'
        col_out = '\033[0m'
        s = "[ActionEngine] " + col_in + unicode(msg) + col_out
        if self.logger is None: 
            print (s)
        else:
            self.logger.log (s)
    
    def abort (self, msg):
        self.log ("ERROR: "+msg+" - aborting")
        self.error = True
        return

    def run (self, context):
        self.context = context
        self.start_scenario ()
    
    def ready_callback (self, ownsock):
        if self._proto.error:
            self.log ("ERROR on ActionEngine initialization - not doing anything")
            return
        self.log ("ActionEngine ready")
        self.ownsock = ownsock
        # start the scenario
        self.run_open_sentence()

    def data_callback (self, msg):
        if self._proto.error:
            return
        self.log ("ActionEngine data '"+unicode(msg)+"'")
        if self.error:
            return

    def start_scenario (self):
        pass

    def run_open_sentence (self, msg = None):
        self._proto.log ("run next sentence")
        pass

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
