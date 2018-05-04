#!/usr/bin/python
# myOpenApplication webserver

import re
import urllib

# --------------------------------------------------------------------------------------------------
#
# TODO: use a templating system
#

# ----
# index page
#


class OW_index(object):
    def do_GET(self, request):
        nb_systems = request.config.nb_systems
        if nb_systems == 0:
            request.redirect('/API/add_system')
            return
        request.html_response('<html><body>' + str(nb_systems) +
                              ' systems configured</body></html>')


class OW_test(object):
    def do_GET(self, request):
        data = {}
        data['ok'] = True
        data['ping'] = 'pong'
        request.json_response(data)
