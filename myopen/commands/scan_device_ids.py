# -*- coding: utf-8 -*-

from ..dialog import CommandDialog
from ..message import Message
from ..subsystems import find_scannable


class CmdScanDeviceIds(CommandDialog):
    _scannable = []
    _current = None

    CMD_SCAN_SYSTEM = "*#[who]*0*13##"

    def gen_command(self, cmdstr, params):
        _cmd = ''
        _in_var = False
        _var = ''
        for c in cmdstr:
            if _in_var:
                if c == ']':
                    # replace var
                    if _var in params.keys():
                        _cmd += str(params[_var])
                    _in_var = False
                    _var = ''
                else:
                    _var += c
                continue
            if c == '[':
                _in_var = True
                continue
            _cmd += c
        return _cmd

    def get_next_scan_command(self):
        if len(self._scannable) == 0:
            return None
        if self._current is None:
            self._current = 0
        else:
            self._current += 1
            if self._current >= len(self._scannable):
                return None
        _who = self._scannable[self._current].SYSTEM_WHO
        _vars = {'who': _who}
        return self.gen_command(self.CMD_SCAN_SYSTEM, _vars)

    def run(self):
        self.log(self._system.devices)
        self._scannable = find_scannable()
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
                print(self.system.devices)
                return self._stop_task()
            self.send(_cmd)
            return
        message = Message(data, self)
        message.dispatch()
