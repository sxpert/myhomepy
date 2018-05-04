#!/usr/bin/python
# myOpenApplication webserver

import re
import urllib
from myopen import layer1


class OW_list_temperatures (object):

    def do_GET(self, request):
        if request.config.nb_systems == 1:
            # TODO: we may not have a database in this system
            sensors = request.config.systems[0]\
                        .monitor.database.list_temperature_sensors()
        else:
            sensors = None
        data = {
            'start': '2017-07-01T23:53',
            'end': '2018-01-25T23:59',
            'temperatures': [],
            'sensors': sensors,
        }
        request.json_response(data)
