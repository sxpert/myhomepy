#!/usr/bin/python
# myOpenApplication webserver

import re
import urllib
from myopen import layer1
from config import config


class OW_list_temperatures (object):

    def do_GET(self, request):
        if config.nb_systems == 1:
            sensors = config.monitors[0].database.list_temperature_sensors()

        else:
            sensors = None
        data = {
            'start': '2017-07-01T23:53',
            'end': '2018-01-25T23:59',
            'temperatures': [],
            'sensors': sensors,
        }
        request.json_response(data)
