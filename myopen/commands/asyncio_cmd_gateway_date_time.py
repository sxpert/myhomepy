# -*- coding: utf-8 -*-

from .asyncio_base_command import BaseCommand
from ..subsystems import Gateway
from .. import subsystems as subs

__all__ = ['CmdGatewayUpdateDateTime']


class CmdGatewayUpdateDateTime(BaseCommand):

    def start(self):
        self.gateway = params.get('gateway', None)
        self.datetime = params.get('datetime', None)
        self.send_date_time_command()

    def send_date_time_command(self):
        self.log("Sending Set DateTime commnand")
        self.msg_handler = self.check_ack
        cmd = Gateway.gen_set_date_time(self._datetime)
        self.send(cmd)

    def check_ack(self, msg):
        if msg.conn is MODE_COMMAND:
            if msg.is_ack:
                self.log("Command executed successfully")
                return self.end()
            elif msg == self.NACK:
                self.log("Command failed for unknown reason")
            else:
                self.log("Unexpected response '%s'" % (msg))
            return self.end()
        # tell the caller we didn't handle the packet
        return False
