# -*- coding: utf-8 -*-

from .. import subsystems as subs
from ..subsystems import Gateway
from .asyncio_base_command import BaseCommand
from core.logger import LOG_ERROR


class GetGatewayInfo(BaseCommand):

    def start(self):
        self.request_gw_model()

    def request_gw_model(self):
        self.log("Requesting Gateway model", LOG_ERROR)
        self.msg_handler = self.receive_gw_model
        cmd = subs.TX_CMD_REQ_GATEWAY_MODEL
        self.send(cmd)

    def receive_gw_model(self, msg):
        self.log('receive_gw_model %s'% (str(msg)), LOG_ERROR)
        if msg.is_conn_command:
            self.msg_handler = self.receive_ack_for_model
            # pretend this is handled
            self.log('receive_gw_model conn_command message handled', LOG_ERROR)
            return True
        # not COMMAND
        return False

    def receive_ack_for_model(self, msg):
        self.log('receive_ack_for_model %s'% (str(msg)), LOG_ERROR)
        if msg.is_conn_command:
            if msg.is_ack:
                self.request_gw_fw_version()
                return True
            elif msg.is_nack:
                self.log("Command failed for unknown reason", LOG_ERROR)
            else:
                self.log("Unexpected response '%s'" % (msg), LOG_ERROR)
            return self.end()
        # not COMMAND
        return False

    def request_gw_fw_version(self):
        self.log("Requesting Gateway model", LOG_ERROR)
        self.msg_handler = self.receive_gw_fw_version
        cmd = subs.TX_CMD_REQ_GATEWAY_FW_VERSION
        self.send(cmd)
        
    def receive_gw_fw_version(self, msg):
        self.log('receive_gw_fw_version %s'% (str(msg)), LOG_ERROR)
        if msg.is_conn_command:
            # TODO: check the nature of the message here
            self.msg_handler = self.receive_ack_for_fw_version
            # pretend this is handled
            return True
        # not COMMAND
        return False

    def receive_ack_for_fw_version(self, msg):
        self.log('receive_ack_for_fw_version %s'% (str(msg)), LOG_ERROR)
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
