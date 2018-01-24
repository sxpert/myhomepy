#!/usr/bin/python
# myOpenApplication webserver

import re
import urllib
from myopen import layer1
import config

class OW_list_temperatures (object):

    def do_GET(self, request):
        data = {
            'temperatures' : [ ],
        }
        request.json_response(data)