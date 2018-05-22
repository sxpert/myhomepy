# -*- coding: utf-8 -*-

import os

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
        return v

class Sentence (ProtoObject):
    RX = 0
    TX = 1
    TYPES = ['RX', 'TX']

    def setup (self, name, data):
        self.name = name
        self.id = self._must ("id", data)
        self.description = self._must ("description", data)
        self.type = self._must ("type", data, self.TYPES)
        self.str = self._must ("str", data)
        self.has_address = self._boolean ("has_address", data)
        self.has_params = self._boolean ("has_params", data)
        self.diag_open = self._boolean ("diag_open", data)
        self.error = self._optional ("error", data)
        return self

    def __repr__(self):
        return self.TYPES[self.type]+'('+self.str+')'

    def is_tx(self):
        return self.type == self.TX

    def replace_vars(self, actionengine, data):
        out_sentence = ''
        var_name = ''
        actionengine.log('replacing vars in outgoing sentence \'%s\''%(self.__repr__()))
        for char in self.str:
            if char == '[':
                # var begin
                var_name += char
            elif char == ']':
                # other chars
                var_name = var_name[1:]
                actionengine.log('var: %s'%(var_name))
                if var_name not in data.keys():
                    actionengine.log('WARNING: can\'t find variable \'%s\' in %s'
                                     %(var_name, str(data)))
                    return False
                out_sentence += data[var_name]
                var_name = ''
            else:
                if len(var_name) > 0:
                    var_name += char
                else:
                    out_sentence += char
        return out_sentence

    def parse(self, actionengine, msg, data=None, vars_map=None):
        actionengine.log("parsing sentence \'%s\'"%(msg))
        actionengine.log("expecting format \'%s\'"%(self.str))
        var_name = ''
        for char in self.str:
            if len(var_name) > 0:
                # variable handling
                if char in ['*', '#']:
                    if len(var_name) > 0:
                        # consume stuff
                        var_value = ''
                        while True:
                            if len(msg) == 0:
                                actionengine.log("sentence does not match expected format")
                                return False
                            pchar = msg[0]
                            msg = msg[1:]
                            if pchar == char:
                                break
                            var_value += pchar
                        var_state = "ignored"
                        # if defined, set the variable into the proper location
                        if (data is not None) and (vars_map is not None):
                            if type(vars_map) is dict:
                                if var_name in vars_map.keys():
                                    var_path = vars_map[var_name]
                                    actionengine.log("%s => %s"%(var_path, str(type(var_path))))
                                    if type(var_path) in [str, unicode]:
                                        var_path = var_path.split(".")
                                        search_path = var_path[:-1]
                                        tmpvar = data
                                        for path_bit in search_path:
                                            if path_bit not in tmpvar.keys():
                                                tmpvar[path_bit] = {}
                                            tmpvar = tmpvar[path_bit]
                                        path_bit = var_path[-1]
                                        if path_bit in tmpvar.keys():
                                            values = tmpvar[path_bit]
                                            if type(values) is list:
                                                values.append(var_value)
                                            else:
                                                tmpvar[path_bit] = [values, var_value]
                                        else:
                                            tmpvar[path_bit] = var_value
                        var_name = ''
                elif char == ']':
                    var_name = var_name[1:]
                else:
                    var_name += char
            else:
                # normal mode
                if char == '[':
                    var_name += char
                else:
                    # consume
                    pchar = msg[0]
                    if char != pchar:
                        actionengine.log("sentence does not match expected format")
                        return False
                    msg = msg[1:]
        return True

    def execute(self, actionengine, msg, data, vars_map=None):
        if self.type == self.TX:
            sentence = self.replace_vars(actionengine, data)
            if sentence != False:
                actionengine.log(sentence)
                actionengine.ownsock.send(sentence)
                return actionengine.OK
        elif self.type == self.RX:
            state = self.parse(actionengine, msg, data, vars_map)
            actionengine.log("parse returned %d"%(state))
            if state:
                return actionengine.OK
            else:
                return actionengine.PARSE_ERROR
        else:
            actionengine.log('Type not handled %s'%(self.TYPES[self.type]))
        return actionengine.NOT_HANDLED

class SequenceItem (ProtoObject):

    def setup (self, name, data):
        self.name = name
        self.id = self._must ("id", data)
        if self.id not in self._proto.sentences.keys():
            return self._abort ("unable to find "+self.id+" in sentences list")
        self.sentence = self._proto.sentences[self.id]
        self.mandatory = self._boolean ("mandatory", data)
        self.repeat = self._boolean ("repeat", data)
        self.vars_map = self._optional ("vars_map", data)
        self.onNAK = self._optional ("onNAK", data)
        self.onERR = self._optional ("onERR", data)
        return self

    def __repr__ (self):
        return unicode(self.sentence)

    def is_tx(self):
        return self.sentence.is_tx()

    def expect_ack(self):
        # false or something
        return self.onNAK

    def execute(self, actionengine, msg, data):
        actionengine.log("SequenceItem.execute (%s)"%(str(self.repeat)))
        state = self.sentence.execute(actionengine, msg, data, self.vars_map)
        if state == actionengine.OK:
            if self.repeat:
                actionengine.log('Repeat == True')
                state = actionengine.SAME
        
        return state

class Sequence (ProtoObject):

    def setup (self, name, data):
        self.name = name
        self.id = self._must ("id", data)
        ol = self._must ("openlist", data)
        if type(ol) is not list:
            return self._abort ("'openlist' is not list type in sequence '"+name+"'")
        self.sentences = []
        for o in ol:
            self.sentences.append(SequenceItem(self._proto).setup(self.name+" - "+unicode(len(self.sentences)+1), o))
        return self        

    def __len__(self):
        return len(self.sentences)

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

    def __len__(self):
        return len(self.sequence)

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

    def __repr__ (self):
        return self.name

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

    def _get_scenario(self, scenario_name):
        if scenario_name not in self.scenarios.keys():
            self.log("ERROR: unable to find scenario '%s'"%(scenario_name))
            return None
        scenario = self.scenarios[scenario_name]
        self.log("scenario : %s"%(scenario_name))
        return scenario

    def _get_sequence(self, scenario, sequence_nb):
        nb_sequences = len(scenario.sequences)
        if sequence_nb >= nb_sequences:
            self.log("ERROR: sequence number requested (%d) larger than the number of sequences available in scenario (%d)"
                     %(sequence_nb, nb_sequences))
            return None
        self.log ("%d sequences in scenario"%(nb_sequences))
        sequence = scenario.sequences[sequence_nb]
        self.log ("sequence : "+unicode(sequence))
        return sequence

    def _get_sentence(self, sequence, sentence_nb):
        nb_sentences = len(sequence.sequence.sentences)
        if sentence_nb >= nb_sentences:
            self.log("ERROR: sentence number requested (%d) larger than the number of sentences available in sequence (%d)"
                     %(sentence_nb, nb_sentences))
            return None
        self.log ("%d sentences in sequence"%(nb_sentences))
        sentence = sequence.sequence.sentences[sentence_nb]
        self.log ("sentence : "+unicode(sentence))
        return sentence

class ProtoState(object):
    def __init__ (self, proto, scenario_name, variables):
        self.proto = proto
        self.scenario_name = scenario_name
        self.vars = variables
        self.reset()
    
    def reset(self):
        # setup internal state
        self.scenario = None
        self.sequence_nb = 0
        self.sequence = None
        self.sentence_nb = 0
        self.sentence = None
        self.expect_acknowledge = False

    def __repr__(self):
        return str(self.vars)

    def _find_current_sentence(self):
        if self.scenario is None:
            self.scenario = self.proto._get_scenario(self.scenario_name)
        if self.sequence is None:
            self.sequence = self.proto._get_sequence(self.scenario, self.sequence_nb)
        if self.sentence is None:
            self.sentence = self.proto._get_sentence(self.sequence, self.sentence_nb)

    def execute_one(self, actionengine, msg = None):
        self._find_current_sentence()
        if self.expect_acknowledge:
            actionengine.log("expecting acknowledge")
            if msg == actionengine.ownsock.ACK:
                # we got the ack... time to forget about it...
                self.expect_acknowledge = False
                actionengine.log("got ack, advancing")
                return self.advance(actionengine)
            # we didn't get ack... that's an error
            return False
        state = self.sentence.execute(actionengine, msg, self.vars)
        actionengine.log("sentence returned : %s"%(actionengine.STATES[state]))
        if state == actionengine.PARSE_ERROR:
            # error while parsing... advance and retry parsing
            if self.advance(actionengine):
                return self.execute_one(actionengine, msg)
            return False
        self.expect_acknowledge = self.sentence.expect_ack()
        if self.expect_acknowledge:
            # skip advancing if we're expecting ack
            return True
        if state == actionengine.OK:
            actionengine.log("repeat : %s"%(str(self.sentence.repeat)))
            if self.sentence.repeat:
                actionengine.log("repeat on")
            else:
                actionengine.log("next sentence")
                return self.advance(actionengine)

    def advance(self, actionengine):
        if (self.scenario is None) or (self.sequence is None) or (self.sentence is None):
            return False
        actionengine.log("%d elements in sequence"%(len(self.sequence)))
        if self.sentence_nb >= len(self.sequence):
            actionengine.log("went passed the end of the sequence")
            return False
        self.sentence_nb += 1
        self.sentence = self.proto._get_sentence(self.sequence, self.sentence_nb)
        actionengine.log("new sentence : '%s'"%(str(self.sentence)))
        if self.sentence.is_tx():
            return self.execute_one(actionengine)
        return True
#
# takes data from actions.json
# executes the series of requests
#
class ActionEngine (object):
    NOT_HANDLED = 0
    OK = 1
    SAME = 2
    PARSE_ERROR = 3
    STATES = ['NotHandled', 'OK', 'Same', 'ParseError']

    def __init__ (self, logger = None):
        self._logger = logger
        self._error = False
        # load the json
        protocol_data_file = os.path.join(os.path.dirname(__file__), "actions.json")
        self.log(protocol_data_file)
        self.load_protocol_data (protocol_data_file)

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
        if self._logger is None: 
            print (s)
        else:
            self._logger.log (s)
    
    def abort (self, msg):
        self.log ("ERROR: "+msg+" - aborting")
        self._error = True
        return

    def run (self, scenario_name, variables):
        self._state = ProtoState(self._proto, scenario_name, variables)
        
    def ready_callback (self, ownsock=None):
        if self._proto.error:
            self.log("ERROR: ActionEngine.ready_callback - not doing anything")
            return
        if ownsock is None:
            self.log("ERROR: ActionEngine.ready_callback - no OwnSock object")
            return
        self.ownsock = ownsock
        self._state.reset()
        # start the scenario
        self.log ("ActionEngine ready")
        self.run_open_sentence()
    
    def data_callback (self, msg=None):
        if self._proto.error:
            return
        if msg is None:
            self.log("ERROR: ActionEngine.data_callback - no data")
            return
        self.log ("ActionEngine data '"+unicode(msg)+"'")
        if self._error:
            return
        self.run_open_sentence(msg)
        self.log("ActionEngine.data_callback end : %s"%(repr(self._state)))

    def run_open_sentence (self, msg = None):
        self._proto.log ("Run next sentence")
        # get sentence
        status = self._state.execute_one(self, msg)

class ScanNetwork(ActionEngine):
    def __init__(self, logger = None):
        super(ScanNetwork, self).__init__(logger)
        variables = {}
        variables["who"] = "1001"
        self.run('ScanByAID', variables)
     