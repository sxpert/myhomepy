# -*- coding: utf-8 -*-
from myopen.subsystems import *

from .asyncio_base_command import *
from myopen.asyncio_connection import *

__all__ = ['CmdScanAid']


class CmdScanAid(BaseCommand):
    def start(self):
        self.msg_handler = self.receive_device_id
        self.scannable = find_scannable()
        self.current = None
        self.send_next_reset_cmd()

    def send_next_reset_cmd(self):
        if self.current is None:
            self.current = 0
        else:
            self.current += 1
        if self.current < len(self.scannable):
            self.msg_handler = self.send_next_scan_command
        else:
            self.msg_handler = self.receive_end_ack
            self.current = len(self.scannable) - 1
        self.send_reset_cmd()
        return True

    def send_reset_cmd(self):
        subsystem = self.scannable[self.current]
        who = subsystem.SYSTEM_WHO
        vars = {
            'who': who
        }
        cmd = replace_in_command(TX_CMD_RESET, vars)
        self.send(cmd)

    def send_next_scan_command(self, msg):
        if msg.conn is MODE_COMMAND:
            if msg.is_ack:
                subsystem = self.scannable[self.current]
                who = subsystem.SYSTEM_WHO
                vars = {
                    'who': who
                }
                self.msg_handler = self.receive_device_id
                cmd = replace_in_command(TX_CMD_SCAN_SYSTEM, vars)
                self.send(cmd)
                return True
            else:
                self.log('CmdScanAid.send_next_scan_command :'
                         'Unexpected message %s'
                         % (str(msg)))
        return False

    def receive_device_id(self, msg):
        if msg.conn is MODE_MONITOR:
            self.log('CmdScanAid.receive_device_id : monitor %s' % (str(msg)))
            if msg.name == 'DIAG_RES_ID':
                # pretend those are handled
                self.log('pretend message was handled')
                return True
            return False
        self.log('CmdScanAid.receive_device_id : command %s' % (str(msg)))
        if msg.is_ack:
            return self.send_next_reset_cmd()
        if msg.function is not None:
            f = msg.function
            self.log('call function %s' % (str(f)))
            f()
        return True

    def receive_end_ack(self, msg):
        if msg.conn is MODE_MONITOR:
            return False
        if msg.is_ack:
            return self.end()
        self.log('CmdScanAid.receive_end_ack : unexpected %s' % (str(msg)))
        return False
