# -*- coding: utf-8 -*-

from .asyncio_base_command import BaseCommand
from myopen.subsystems import Lighting
from .. import subsystems as subs


class CmdGeneralOff(BaseCommand):

    def start(self):
        self.send_general_off_command()

    def send_general_off_command(self):
        self.log("Sending General Off command")
        self.msg_handler = self.check_ack
        # l = Lighting(self)
        # cmd = l.gen_command(l.OP_LIGHTING_OFF, l.TARGET_GENERAL)
        cmd = '*1*0*03##'
        self.send(cmd)

    def check_ack(self, msg):
        if msg.is_conn_command:
            if msg.is_ack:
                self.log("Command executed successfully")
                return self.end()
            elif msg.is_nack:
                self.log("Command failed for unknown reason")
            else:
                self.log("Unexpected response '%s'" % (msg))
            # fall down
        # tell the caller we didn't handle the packet
        self.end()
        return False
