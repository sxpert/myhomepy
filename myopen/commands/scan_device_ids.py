# -*- coding: utf-8 -*-

from ..dialog import CommandDialog
from ..message import Message
from .. import subsystems as subs


class CmdScanDeviceIds(CommandDialog):
    STATE_START = 0
    STATE_SCANNING = 1
    STATE_FINISH = 2


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

    def get_scan_command(self):
        _who = self._scannable[self._current].SYSTEM_WHO
        _vars = {'who': _who}
        return subs.replace_in_command(subs.TX_CMD_SCAN_SYSTEM, _vars)

    def get_reset_command(self):
        _who = self._scannable[self._current].SYSTEM_WHO
        _vars = {'who': _who}
        return subs.replace_in_command(subs.TX_CMD_RESET, _vars)

    def run(self):
        self._scenario_state = self.STATE_START
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
        self.log("about to request device ids to the network")
        if not self.next_scannable_system():
            return self._stop_task('no next scannable system')
        _cmd = self.get_reset_command()
        self.send(_cmd)

    def _stop_task(self, msg=None):
        if msg is not None:
            self.log(msg)
        self.stopping = True
        self.notify()

    def data_callback(self, data):
        _cmd = None
        if data == self.NACK:
            return self._stop_task('NACK received, something went very wrong')

        if data == self.ACK:
            if self._scenario_state == self.STATE_START:
                # received ACK for reset command, 
                # send the scan system command
                self._scenario_state = self.STATE_SCANNING
                _cmd = self.get_scan_command()
            elif self._scenario_state == self.STATE_SCANNING:
                # scaning is finished, send the reset command
                self._scenario_state = self.STATE_FINISH
                _cmd = self.get_reset_command()
            elif self._scenario_state == self.STATE_FINISH:
                # received ACK for the second reset command,
                # go to next system, and send reset command
                if not self.next_scannable_system():
                    return self._stop_task('should be finished')
                self._scenario_state = self.STATE_START
                _cmd = self.get_reset_command()
            
            # _cmd should always be defined here
            self.send(_cmd)
            return

        # neither ACK nor NACK...
        message = Message(data, self)
        message.dispatch()
