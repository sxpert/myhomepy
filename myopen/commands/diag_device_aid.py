# -*- coding: utf-8 -*-

import threading

from .. import subsystems as subs
from ..devices import BaseDevice
from ..dialog import CommandDialog
from ..message import Message
from ..subsystems import DiagScannable


class CmdDiagDeviceByAid(CommandDialog):
    STATE_START = 0
    STATE_WAIT_HEADER_EOT = 0
    STATE_READ_KEYO = 1
    STATE_END_DIAG = 2

    CALLBACKS = [
        'state_wait_header_eot',
        'state_read_keyo',
        'state_end_diag'
    ]

    def run(self, params):
        self._diag_event = threading.Event()
        self.log(params)
        self._scenario_state = self.STATE_START
        self._devices = params.get('devices', None)
        self._device = params.get('device', None)
        if self._device is None:
            self.log('device is None, aborting')
            return self.notify()
        if not issubclass(self._device.__class__, BaseDevice):
            self.log('device invalid \'%s\'' % (str(self._device)))
            return self.notify()
        self._hw_addr = getattr(self._device, '_hw_addr', None)
        if self._hw_addr is None:
            self.log('device %s has no _hw_addr registered, aborting' % (self._device))
            return self.notify()
        self._subsystem = self._device._subsystem
        if self._subsystem is None:
            self.log('subsystem is None, aborting')
            return self.notify()
        if not issubclass(self._subsystem.__class__, DiagScannable):
            self.log('subsystem %s is not fit for purpose' % (str(self._subsystem)))
            return self.notify()
        self._who = getattr(self._subsystem, 'SYSTEM_WHO', None)
        if self._who is None:
            self.log('subsystem has no SYSTEM_WHO value, aborting')
            return self.notify()
        super().run()

    def ready_callback(self):
        self.log("about to request configuration info for device")
        _vars = {'who': self._who,
                 'id': self._hw_addr}
        self.log('vars: %s' % (str(_vars)))
        _cmd = subs.replace_in_command(subs.TX_CMD_DIAG_ID, _vars)
        self.log('command to send %s' % (_cmd))
        self.system.devices.set_active_device(self, self._hw_addr)
        self.send(_cmd)

        
    def _stop_task(self, msg=None):
        if msg is not None:
            self.log(msg)
        self.stopping = True
        self.notify()

    def data_callback(self, data):
        try:
            _cb = self.CALLBACKS[self._scenario_state]
        except IndexError:
            return self._stop_task('there is no state number %d' % self._scenario_state)
        _func = getattr(self, _cb, None)
        if _func is None:
            return self._stop_task('CmdDiagDeviceByAid.data_callback unable to find callback %s' % (_cb))
        if not callable(_func):
            return self._stop_task('CmdDiagDeviceByAid.data_callback %s is not callable' % (str(_func)))
        _func(data)

    def notify_diag_sync(self):
        self._diag_event.set()
        return True

    def state_wait_header_eot(self, data):
        self.log('_wait_header_eot : %s' % (data))
        if data == self.NACK:
            self.log('requesting configuration for device id %s failed' %
                (self._devices.format_hw_addr(self._hw_addr)))
            return self.end_diag()

        # stuff comes in via the MONITOR channel 
        # NOTE: 
        # who the fuck comes with this funky as hell protocol,
        # must be some crazy italian

        self._diag_event.wait()
        self.log('diag_event was set, continuing')

        self._scenario_state = self.STATE_READ_KEYO

        _vars = {'who': self._who}
        self.log('vars: %s' % (str(_vars)))
        _cmd = subs.replace_in_command(subs.TX_CMD_PARAM_ALL_KO, _vars)
        self.log('command to send %s' % (_cmd))
        self.send(_cmd)

    def state_read_keyo(self, data):
        if data == self.NACK:
            return
        if data == self.ACK:
            # end of keyo list
            return self.end_diag()
        
        message = Message(data, self)
        message.dispatch()
        

    def end_diag(self):
        self._scenario_state = self.STATE_END_DIAG
        _vars = {'who': self._who}
        self.log('vars: %s' % (str(_vars)))
        _cmd = subs.replace_in_command(subs.TX_CMD_DIAG_ABORT, _vars)
        self.log('command to send %s' % (_cmd))
        self.send(_cmd)

    def state_end_diag(self, data):
        self.log('state_end_diag %s' % (data))
        if data == self.ACK or data == self.NACK:
            self._stop_task()

