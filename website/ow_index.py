#!/usr/bin/python
# myOpenApplication webserver

import re
import urllib
import myOpenLayer1
import config
import BaseHTTPServer

#--------------------------------------------------------------------------------------------------
#
# TODO: use a templating system
#

#----
# index page
# 

class OW_index (object):
    def do_GET(self, request):
        nb_systems = len(config.config)
        if nb_systems == 0: 
            request.redirect ('/add_system')
            return
        request.html_response('<html><body>'+unicode(len(config.config))+' systems configured</body></html>')

