# -*- coding: utf-8 -*-

from .asyncio_base_command import BaseCommand
from ..subsystems import Gateway
from .. import subsystems as subs

__all__ = ['CmdGatewayUpdateDateTime']


class CmdGatewayUpdateDateTime(BaseCommand):

    def start(self):
        self.gateway = self.params.get('gateway', None)
        self.datetime = self.params.get('datetime', None)
        self.send_date_time_command()

    def send_date_time_command(self):
        self.log("Sending Set DateTime commnand")
        self.msg_handler = self.check_ack
        cmd = Gateway.gen_set_date_time(self.datetime)
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
