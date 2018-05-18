from myopen.asyncio_connection import *
from myopen.devices import BaseDevice
from myopen.subsystems import *

from .asyncio_base_command import *

__all__ = ['CmdDiagAid']


class CmdDiagAid(BaseCommand):
    def start(self):
        self.devices = self.params.get('devices', None)
        self.device = self.params.get('device', None)

        if self.device is None:
            self.log('device is None, aborting')
            return self.end()

        if not issubclass(self.device.__class__, BaseDevice):
            self.log('device invalid \'%s\'' % (str(self.device)))
            return self.end()

        self.hw_addr = getattr(self.device, 'hw_addr', None)
        if self.hw_addr is None:
            self.log('device %s has no _hw_addr registered, aborting'
                     % (self.device))
            return self.end()

        self.subsystem = self.device.subsystem
        if self.subsystem is None:
            self.log('subsystem is None, aborting')
            return self.end()

        if not issubclass(self.subsystem.__class__, DiagScannable):
            self.log('subsystem %s is not fit for purpose'
                     % (str(self.subsystem)))
            return self.end()

        self.who = getattr(self.subsystem, 'SYSTEM_WHO', None)
        if self.who is None:
            self.log('subsystem has no SYSTEM_WHO value, aborting')
            return self.end()

        self.log('Launching diagnostic on %s' % (str(self.device)))

        self.start_diag()

    def start_diag(self):

        vars = {'who': self.who,
                'id': self.hw_addr}

        cmd = replace_in_command(TX_CMD_DIAG_ID, vars)
        self.devices.set_active_device(self, self.hw_addr)
        self.msg_handler = self.read_base_device_config
        self.send(cmd)

    def read_base_device_config(self, msg):
        self.log(msg)
        if msg.conn is MODE_COMMAND:
            if msg.is_ack:
                self.log('Got the ACK on command socket')
                return True
        if msg.name == 'RES_TRANS_END':

            vars = {'who': self.who}

            self.log('vars: %s' % (str(vars)))
            cmd = replace_in_command(TX_CMD_PARAM_ALL_KO, vars)
            self.log('command to send %s' % (cmd))
            self.msg_handler = self.read_keyo
            self.send(cmd)

    def read_keyo(self, msg):
        """
        we are only interested in RES_PARAM_KO at this point
        """
        self.log(msg)
        if msg.name == 'RES_PARAM_KO':
            if msg.conn is MODE_COMMAND:
                # handle the messages from the command socket
                return False
            # pretend those from the monitor socket are handled
            return True
        # let the rest handle itself
        if msg.conn is MODE_COMMAND:
            if msg.is_ack:
                self.end_diag()
        return False

    def end_diag(self):
        vars = {'who': self.who}
        self.log('vars: %s' % (str(vars)))
        cmd = replace_in_command(TX_CMD_DIAG_ABORT, vars)
        self.log('command to send %s' % (cmd))
        self.msg_handler = self.wait_for_ack
        self.send(cmd)

    def wait_for_ack(self, msg):
        if msg.conn is MODE_COMMAND:
            if msg.is_ack:
                return self.end()
            self.log('Unexpected messsge %s' % (str(msg)))
        return False
