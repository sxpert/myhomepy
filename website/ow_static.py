#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

# myOpenApplication webserver

import os
import re
import sys
import urllib

import config
from myopen import layer1

STATIC_FILES = "static"


# --------------------------------------------------------------------------------------------------
#
# TODO: use a templating system
#

# ----
# handle static content
#

class OW_static (object):
    def do_GET(self, request):
        # find this file in the static directory
        request.file_response(STATIC_FILES, request.path[1:])
