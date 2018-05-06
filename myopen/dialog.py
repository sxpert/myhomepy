# -*- coding: utf-8 -*-

from .socket import OWNSocket
from threading import Condition


class CommandDialog(OWNSocket):
    _event = None
    _success = False

    def __init__(self, clone):
        super().__init__(clone.address,
                         clone.port,
                         clone.passwd,
                         self.COMMAND,
                         clone.timeout,
                         # auto_reconnect is false
                         False)
        self.set_logger(clone._log)
        self.ready_callback = self.dialog_ready
        self.data_callback = self.dialog_data

    @property
    def event(self):
        return self._event

    @property
    def success(self):
        return self._success

    @event.setter
    def event(self, ev):
        self._event = ev

    def notify(self):
        if self._event is not None:
            self._event.set()

    def dialog_ready(self):
        self.log("DIALOG: ready")

    def dialog_data(self, msg):
        self.log("DIALOG: msg")
