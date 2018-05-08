# -*- coding: utf-8 -*-

from ..dialog import CommandDialog
from ..message import Message
from .. import subsystems as subs


class CmdScanDeviceIds(CommandDialog):
    _scannable = []
    _current = None

    # better implemented by eating from the list
    def next_scannable_system(self):
        if len(self._scannable) == 0:
            return False
        if self._current is None:
            self._current = 0
        else:
            self._current += 1
            if self._current >= len(self._scannable):
                return False
        return True

    def get_next_scan_command(self):
        if not self.next_scannable_system():
            return None
        _who = self._scannable[self._current].SYSTEM_WHO
        _vars = {'who': _who}
        return subs.replace_in_command(subs.TX_CMD_SCAN_SYSTEM, _vars)

    def run(self):
        self.log('CmdScanDeviceIds.run: %s' % (str(self._tasks._tasks)))
        self.log(self._system.devices)
        self._scannable = subs.find_scannable()
        ok = True
        if not isinstance(self._scannable, list):
            ok = False
        if len(self._scannable) == 0:
            ok = False
        if not ok:
            self.log("No systems are scannable, aborting")
            self.notify()
            return
        super().run()

    def ready_callback(self):
        _cmd = self.get_next_scan_command()
        self.log("about to request device ids to the network")
        self.send(_cmd)

    def _stop_task(self):
        self.stopping = True
        self.notify()

    def data_callback(self, data):
        if data == self.NACK:
            return self._stop_task()            
        if data == self.ACK:
            # next system
            _cmd = self.get_next_scan_command()
            if _cmd is None:
                # we went to the end...
                self._success = True
                return self._stop_task()
            self.send(_cmd)
            return
        message = Message(data, self)
        message.dispatch()
