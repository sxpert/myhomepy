# -*- coding: utf-8 -*-

from .socket import OWNSocket
from threading import Condition


class CommandDialog(OWNSocket):
    _event = None
    _success = False
    _system = None

    def __init__(self, clone):
        if 'system' in dir(clone):
            self._system = clone.system
        super().__init__(clone.address,
                         clone.port,
                         clone.passwd,
                         self.COMMAND,
                         clone.timeout,
                         # auto_reconnect is false
                         False)

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

    def ready_callback(self):
        self.log("DIALOG: ready")

    def data_callback(self, msg):
        self.log("DIALOG: msg")
