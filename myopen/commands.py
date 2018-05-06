# -*- coding: utf-8 -*-

from .dialog import CommandDialog
from .subsystems import Lighting


class CmdGeneralOff(CommandDialog):
    def dialog_ready(self):
        self.log("Sending GeneralOff commnand")
        l = Lighting(self)
        command = l.gen_command(l.OP_LIGHTING_OFF, l.TARGET_GENERAL)
        self.log(command)
        self.send(command)

    def dialog_data(self, msg):
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
