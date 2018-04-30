#!/usr/bin/python
# myOpenApplication webserver

import re
import urllib

from config import config
from myopen import commands


class OW_general_off (object):

    def do_GET(self, request):
        error = None
        if config.nb_systems == 1:
            monitor = config.monitors[0]
        else:
            ok = False
            monitor = None
            error = "ERROR: Too many systems"

        if monitor:
            ok = monitor.send_command(commands.CmdGeneralOff)
        data = {
            'ok': ok,
        }
        if error is not None:
            data['error'] = error
        request.json_response(data)
