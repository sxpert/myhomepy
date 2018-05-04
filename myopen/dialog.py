# -*- coding: utf-8 -*-

from .socket import OWNSocket


class CommandDialog(OWNSocket):
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

    def dialog_ready(self):
        self.log("DIALOG: ready")

    def dialog_data(self, msg):
        self.log("DIALOG: msg")
