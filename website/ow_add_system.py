#!/usr/bin/python
# myOpenApplication webserver

import re
import urllib
from myopen import layer1
import config

# --------------------------------------------------------------------------------------------------
#
# TODO: use a templating system
#

# ----
# adding a system
#


class OW_add_system(object):

    def generate_basic_form(self, request):
        try:
            errors = self.errors
        except:
            errors = {}

        gateway = request.quote_value(self.gateway)
        openwebnet_port = request.quote_value(self.openwebnet_port)
        password_open = request.quote_value(self.password_open)

        r = '<!DOCTYPE html>\n'\
            '<html><head>\n'\
            '<style type="text/css">\n'\
            '.error { color: red; }\n'\
            '.field { display: block; margin-bottom: 1pt; }\n'\
            'label { display: inline-block; width: 20em; }\n'\
            '</style>\n'\
            '</head><body>\n'\
            '<form method="post">\n'

        if 'gateway' in errors:
            r += '<div class="error">'+errors['gateway']+'</div>\n'
        r += '<div class="field"><label for="gateway">IP ou nom DNS de la'\
             ' passerelle</label><input type="text" name="gateway" '\
             'value="' + gateway + '"></input></div>\n'

        if 'openwebnet_port' in errors:
            r += '<div class="error">'+errors['openwebnet_port']+'</div>\n'
        r += '<div class="field"><label for="openwebnet_port">Port OpenWebNet'\
             '</label><input type="text" name="openwebnet_port" value="' + \
             openwebnet_port + '"></input></div>\n'

        if 'password_open' in errors:
            r += '<div class="error">'+errors['password_open']+'</div>\n'
        r += '<div class="field"><label for="password_open">Password OPEN'\
            '</label><input type="text" name="password_open" value="' + \
            password_open + '"></input></div>\n'

        r += '<button name="action" value="add_system">add gateway</button>\n'\
            '</form>\n'\
            '</body></html>'
        request.html_response(r)

    def do_GET(self, request):
        # initialize variables
        self.gateway = ""
        self.openwebnet_port = ""
        self.password_open = ""

        # do the deed
        nb_systems = len(config.config)
        if nb_systems == 0:
            # we have no systems configured, present the initial setup page
            self.generate_basic_form(request)
        else:
            # we already have a system, present the page integrated in the
            # menus
            pass

    def is_ipv4(self, value):
        # check if ipv4
        m = re.match("^(\d{1,3})\.(\d{1,3})\.(\d{1,3}).(\d{1,3})$", value)
        if m is not None:
            for v in m.groups():
                # should not fail at this point, also, values should only be
                # positive integers
                v = int(v)
                if v > 256:
                    return False
            return True
        return False

    def is_domain(self, value):
        names = value.split('.')
        if len(names) == 0:
            return False
        layer1.SYSTEM_LOGGER.log(str(names))
        for n in names:
            # TODO: check against the dns spec
            m = re.match("^[a-z][a-z0-9\-_]{0,62}$", n.lower())
            if m is None:
                return False
            layer1.SYSTEM_LOGGER.log(n)
        return True

    def is_ipv4_or_domain(self, value):
        return self.is_ipv4(value) or self.is_domain(value)

    def is_port(self, value):
        m = re.match("^\d{1,5}$", value)
        if m is not None:
            v = int(value)
            if v > 65535:
                return False
            return True
        return False

    def is_password_open(self, value):
        m = re.match("^\d{1,10}$", value)
        if m is not None:
            return True
        return False

    def do_POST(self, request):
        # get variables
        self.errors = {}
        self.action = request.get_variable('action')
        self.gateway = request.get_variable('gateway')
        self.openwebnet_port = request.get_variable('openwebnet_port')
        self.password_open = request.get_variable('password_open')
        # check variables for stuff
        if self.action is None or self.action != 'add_system':
            request.send_error(400, "unexpected value for \"action\"")
            return
        if self.gateway is None or not self.is_ipv4_or_domain(self.gateway):
            self.errors['gateway'] = "Expected value for gateway is IPv4 "\
                                     "or domain name"
        if self.openwebnet_port is None or\
           not self.is_port(self.openwebnet_port):
            self.errors['openwebnet_port'] = "Expected value for port is an "\
                "integer from 1 to 65535, default value is 20000"
        if self.password_open is None or\
           not self.is_password_open(self.password_open):
            self.errors['password_open'] = "Expected value for Password OPEN "\
                "is 1 to 10 digits from 0 to 9"
        if len(self.errors.keys()) > 0:
            self.generate_basic_form(request)
            return

        # add the new gateway
        config.config.add_system(self.gateway,
                                 int(self.openwebnet_port),
                                 self.password_open)

        request.html_response(('<pre>ok\n%s\n%s\n%s\n%s</pre>' %
                               (self.action,
                                self.gateway,
                                self.openwebnet_port,
                                self.password_open)))
