# -*- coding: utf-8 -*-

from ..dialog import CommandDialog


class CmdScanDeviceIds(CommandDialog):
    def ready_callback(self):
        self.log("about to request device ids to the network")
        self.stopping = True
        self.notify()

    def data_callback(self):
        pass
