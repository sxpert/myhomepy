#!/usr/bin/python
# myOpenApplication webserver

import os, sys
import re
import urllib
import myOpenLayer1
import config
import BaseHTTPServer

STATIC_FILES = "static"

#--------------------------------------------------------------------------------------------------
#
# TODO: use a templating system
#

#----
# handle static content
# 

class OW_static (object):
    def do_GET(self, request):
        # find this file in the static directory
        request.file_response(STATIC_FILES, request.path[1:])

