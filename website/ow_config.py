#!/usr/bin/python
# myOpenApplication webserver

import re
import urllib

from myopen import commands
from core.logger import SYSTEM_LOGGER

class OW_config (object):

    def do_GET(self, request):
        data = request.config.serialize()
        request.json_response(data)
