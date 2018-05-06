# -*- coding: utf-8 -*-

from ..dialog import CommandDialog


class CmdScanDeviceIds(CommandDialog):
    SCANNABLE_SYSTEMS = ['1001']
    _current = None

    CMD_SCAN_SYSTEM = "*#[who]*0*13##"

    def gen_command(self, cmdstr, params):
        _cmd = ''
        _in_var = False
        _var = ''
        self.log(cmdstr)
        self.log(str(params))
        for c in cmdstr:
            if _in_var:
                if c == ']':
                    # replace var

                    self.log(_var)
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
        if self._current is None:
            self._current = 0
        else:
            self._current += 1
        return self.gen_command(self.CMD_SCAN_SYSTEM, 
                                {'who': self.SCANNABLE_SYSTEMS[self._current]})

    def ready_callback(self):
        self.log("about to request device ids to the network")
        _cmd = self.get_next_scan_command()
        self.log(_cmd)
        self.send(_cmd)

    def _stop_task(self):
        self.stopping = True
        self.notify()

    def data_callback(self, data):
        if data == self.NACK:
            return self._stop_task()            
        if data == self.ACK:
            return self._stop_task()
        