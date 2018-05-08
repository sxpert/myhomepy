#!/usr/bin/python
# myOpenApplication webserver

import re
import urllib
import threading

from myopen import commands
from core.logger import SYSTEM_LOGGER

class OW_scan_ids (object):
    success = False

    def do_GET(self, request):
        error = None
        if request.config.nb_systems == 1:
            monitor = request.config.systems[0].monitor
        else:
            monitor = None
            error = "ERROR: Too many systems"

        # socket = command(self)
        # event = threading.Event()
        # socket.event = event
        # self.log("OWNMonitor.send_command %s" % (socket.__class__.__name__))
        # self.system.main_loop.add_task(socket)
        # socket.start()
        # if wait:
        #     event.wait()
        # return socket.success
        
        monitor.log('before calling the task')

        event = threading.Event()
        
        _self = self

        def cb(self):
            self.log('notify event')
            self.log('in callback : success %s' % (str(self.success)))
            _self.success = self.success
            event.set()

        if monitor:
            monitor.push_task(commands.CmdScanDeviceIds, callback=cb)

        event.wait()
        
        # should list all ids found
        data = {
            'ok': self.success,
        }
        if error is not None:
            data['error'] = error
        request.json_response(data)
