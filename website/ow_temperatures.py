#!/usr/bin/python
# myOpenApplication webserver

import re
import urllib
from myopen import layer1
import config


class OW_list_temperatures (object):

    def do_GET(self, request):
        sensors = config.config.systems
        data = {
            'start': '2017-07-01T23:53',
            'end': '2018-01-25T23:59',
            'temperatures': [],
            'sensors': sensors,
        }
        request.json_response(data)
