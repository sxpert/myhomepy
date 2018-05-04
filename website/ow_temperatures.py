#!/usr/bin/python
# myOpenApplication webserver

import re
import urllib


class OW_list_temperatures (object):

    def do_GET(self, request):
        sensors = None
        if request.config.nb_systems == 1:
            # TODO: we may not have a database in this system
            system = request.config.systems[0]
            if system.database is not None:
                database = system.monitor.database
                sensors = database.list_temperature_sensors()
        data = {
            'start': '2017-07-01T23:53',
            'end': '2018-01-25T23:59',
            'temperatures': [],
            'sensors': sensors,
        }
        request.json_response(data)
