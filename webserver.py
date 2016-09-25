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

#----
# adding a system
#

class OW_add_system (object):

    def generate_basic_form (self, request):
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
            r+= '<div class="error">'+errors['gateway']+'</div>\n'
        r+= '<div class="field"><label for="gateway">IP ou nom DNS de la passerelle</label>'\
                '<input type="text" name="gateway" value="'+gateway+'"></input></div>\n'
                
        if 'openwebnet_port' in errors:
            r+= '<div class="error">'+errors['openwebnet_port']+'</div>\n'
        r+= '<div class="field"><label for="openwebnet_port">Port OpenWebNet</label>'\
                '<input type="text" name="openwebnet_port" value="'+openwebnet_port+'"></input></div>\n'

        if 'password_open' in errors:
            r+= '<div class="error">'+errors['password_open']+'</div>\n'
        r+= '<div class="field"><label for="password_open">Password OPEN</label>'\
                '<input type="text" name="password_open" value="'+password_open+'"></input></div>\n'

        r+= '<button name="action" value="add_system">add gateway</button>\n'\
            '</form>\n'\
            '</body></html>'
        request.html_response(r)

    def do_GET(self, request):
        # initialize variables
        self.gateway         = ""
        self.openwebnet_port = ""
        self.password_open   = ""

        # do the deed
        nb_systems = len(config.config)
        if nb_systems == 0:
            # we have no systems configured, present the initial setup page
            self.generate_basic_form(request)
        else:
            # we already have a system, present the page integrated in the menus
            pass

    def is_ipv4 (self, value):
        # check if ipv4
        m = re.match("^(\d{1,3})\.(\d{1,3})\.(\d{1,3}).(\d{1,3})$", value)
        if m is not None:
            for v in m.groups():
                # should not fail at this point, also, values should only be positive integers
                v = int(v)
                if v>256:
                    return False
            return True
        return False
   
    def is_domain (self, value):
        names = value.split('.')
        if len(names)==0:
            return False
        myOpenLayer1.system_logger.log(unicode(names))
        for n in names:
            # TODO: check against the dns spec
            m = re.match("^[a-z][a-z0-9\-_]{0,62}$", n.lower())
            if m is None:
                return False
            myOpenLayer1.system_logger.log(n)
        return True

    def is_ipv4_or_domain (self, value):
        return self.is_ipv4(value) or self.is_domain(value)

    def is_port (self, value):
        m = re.match("^\d{1,5}$", value)
        if m is not None:
            v = int(value)
            if v>65535:
                return False
            return True
        return False

    def is_password_open (self, value):
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
            self.errors['gateway'] = "Expected value for gateway is IPv4 or domain name"
        if self.openwebnet_port is None or not self.is_port(self.openwebnet_port):
            self.errors['openwebnet_port'] = "Expected value for port is an integer from 1 to 65535, default value is 20000"
        if self.password_open is None or not self.is_password_open(self.password_open):
            self.errors['password_open'] = "Expected value for Password OPEN is 1 to 10 digits from 0 to 9"
        if len(self.errors.keys())>0:
            self.generate_basic_form(request)
            return

        request.html_response('<pre>ok\n%s\n%s\n%s\n%s</pre>'% (self.action, self.gateway, self.openwebnet_port, self.password_open))

#--------------------------------------------------------------------------------------------------
#
#
#

ROUTES =    [
                [ "^/$", OW_index ],
                [ "^/add_system(.*)$", OW_add_system ],
            ]

#--------------------------------------------------------------------------------------------------
#
#
#

class OpenWebHandler (BaseHTTPServer.BaseHTTPRequestHandler, object):

    def log (self, code=None, size=None, msg=None):
        srv = '['+unicode(self.server.server_name)+':'+unicode(self.server.server_port)+' WEB]'
        if msg is None:
            req = self.address_string()+' '+self.command+' '+unicode(self.path)
            res = unicode(code)
            if size is not None:
                res += ' '+unicode(size)
            msg = req+' '+res
        else:
            srv=srv[:-1]+'_ERROR]'
        myOpenLayer1.system_logger.log (srv+' '+msg)
    
    def log_request (self, code=None, size=None):
        self.log(code, size)

    def log_error (self, format, *args):
        self.log(None, None, format%args)

    def redirect(self, url):
        self.send_response(302)
        self.send_header('Location', url)
        self.end_headers()

    def html_response(self, html, more_headers = None):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html)

    def find_route(self):
        for r in ROUTES:
            e, c = r
            m = re.match(e, self.path)
            if m is not None:
                g = m.groups()
                if len(g)>0:
                    myOpenLayer1.system_logger.log(unicode(m.groups()))
                o = c()
                return o
        self.send_error(404)
        return None

    def do_request(self):
        o = self.find_route()
        if o is None:
            return
        mname = 'do_'+self.command
        if not hasattr(o, mname):
            self.send_error(501, "Unsupported method (%r)" % self.command)
            return
        method = getattr(o, mname)
        method(self)
    
    def do_GET(self):
        self.do_request()

    def do_POST(self):
        if not self.parse_variables():
            # response already sent in this case
            return 
        self.do_request()

    #----------------------------------------------------------------------------------------------
    # variables management

    def parse_variables_string(self, data):
        # step 1: split at '&' that are not '&amp;'
        start = 0
        blocks = []
        while True:
            pos = data.find('&', start)
            if pos != -1:
                t = data[pos:pos+4]
                if t == '&amp;':
                    # continue  
                    start = pos+5
                else:
                    b = data[0:pos]
                    data = data[pos+1:]
                    blocks.append(b)
                    start = 0
            else:
                # last variable
                blocks.append(data)
                break
        for b in blocks:
            pos = b.find('=')
            if pos != -1:
                k = urllib.unquote(b[0:pos])
                v = urllib.unquote_plus(b[pos+1:])
                if len(k)>2 and k[-2:]=='[]':
                    k = k[:-2]
                    try:
                        tv = self.variables[k]
                    except KeyError as e:
                        tv = []
                    tv.append(v)
                    v = tv
                self.variables[k] = v

    def parse_url_variables(self):
        self.variables={}
    
    def parse_post_urlencoded_variables(self):
        try:
            l = self.headers['content-length']
        except KeyError as e:
            self.send_error(501, "unable to find content length for posted data")
            return False
        # limit check on length
        d = self.rfile.read(int(l))
        # parse variable stream
        self.parse_variables_string(d)
        return True

    def parse_variables(self):
        self.parse_url_variables()
        try: 
            t = self.headers['content-type']
        except KeyError as e:
            pass
        if t == 'application/x-www-form-urlencoded':
            return self.parse_post_urlencoded_variables()
        # unknown type, skip
        myOpenLayer1.system_logger.log('unknown content-type: '+t)
        return True

    def get_variable(self, name):
        if name not in self.variables.keys():
            self.send_error(400, "expected a variable named \""+name+"\"")
            return None
        return self.variables[name]

    def quote_value(self, value):
        v = ""
        for c in value:
            if c == "<":
                v+="&lt;"
            elif c == ">":
                v+="&gt;"
            elif c == "&":    
                v+="&amp;"
            elif c == "\"":
                v+="&quot;"
            else:
                v+=c
        return v

#--------------------------------------------------------------------------------------------------
#
# TODO: ssl mode
#
# import BaseHTTPServer, SimpleHTTPServer
# import ssl
#
# httpd = BaseHTTPServer.HTTPServer(('localhost', 4443), SimpleHTTPServer.SimpleHTTPRequestHandler)
# httpd.socket = ssl.wrap_socket (httpd.socket, certfile='path/to/localhost.pem', server_side=True)
# httpd.serve_forever()
#

class OpenWeb (BaseHTTPServer.HTTPServer, object):
    def __init__ (self, address):
        super(OpenWeb, self).__init__(address, OpenWebHandler)
        myOpenLayer1.system_logger.log ('['+unicode(self.server_name)+':'+unicode(self.server_port)+' WEB] starting')
   
    def connect (self):
        pass
    
    def recv (self):
        self._handle_request_noblock()

    @property
    def sock(self):
        return self.socket
    
if __name__ == '__main__':
    addr = ('', 8000)
    srv = OpenWeb(addr)
    import myOpenLayer1
    system_loop = myOpenLayer1.MainLoop(myOpenLayer1.system_logger)
    print srv.sock.fileno()
    system_loop.add_socket (srv)
    system_loop.run ()
