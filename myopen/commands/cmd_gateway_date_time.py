# -*- coding: utf-8 -*-

from ..dialog import CommandDialog
from ..subsystems import Gateway
from .. import subsystems as subs

class CmdGatewayUpdateDateTime(CommandDialog):
    def run(self, params):
        self._gateway = params.get('gateway', None)
        self._datetime = params.get('datetime', None)
        super().run()
        
    def ready_callback(self):
        self.log("Sending Set DateTime commnand")
        command = Gateway.gen_set_date_time(self._datetime)
        self.log(command)
        self.send(command)

    def data_callback(self, msg):
        self.log("reading response %s" % (msg))
        if msg == self.ACK:
            self.log("Command executed successfully")
            self._success = True
        elif msg == self.NACK:
            self.log("Command failed for unknown reason")
        else:
            self.log("Unexpected response '%s'" % (msg))
        self.stopping = True
        self.notify()
 
