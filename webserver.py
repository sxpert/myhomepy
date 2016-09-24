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

class OW_index (object):
    def do_GET(self, request):
        nb_systems = len(config.config)
        if nb_systems == 0: 
            request.redirect ('/add_system')
            return
        request.html_response('<html><body>'+unicode(len(config.config))+' systems configured</body></html>')

class OW_add_system (object):
    def do_GET(self, request):
        nb_systems = len(config.config)
        if nb_systems == 0:
            # we have no systems configured, present the initial setup page
            request.html_response('<!DOCTYPE html>\n'+
                '<html><head>'+
                '<style type="text/css">'+
                '.field { display: block; margin-bottom: 1pt; }'+
                'label { display: inline-block; width: 10em; }'+
                '</style>'+
                '</head><body>'+
                '<form method="post">'+
                    '<div class="field"><label for="gateway">IP ou nom DNS de la passerelle</label><input type="text" name="gateway"></input></div>'+
                    '<div class="field"><label for="openwebnet_port">Port OpenWebNet</label><input type="text" name="openwebnet_port"></input></div>'+
                    '<div class="field"><label for="password_open">Password OPEN</label><input type="text" name="password_open"></input></div>'+
                    '<button name="action" value="add_system">add gateway</button>'+
                '</form>'+
                '</body></html>')
        else:
            # we already have a system, present the page integrated in the menus
            pass

    def do_POST(self, request):
        # check variables for stuff
        action = request.get_variable('action')
        if action is not None and action != 'add_system':
            request.send_error(400, "unexpected value for \"action\"")
            return
        gateway = request.get_variable('gateway')
        openwebnet_port = request.get_variable('openwebnet_port')
        password_open = request.get_variable('password_open')

        request.html_response('<pre>ok\n%s\n%s\n%s\n%s</pre>'% (action, gateway, openwebnet_port, password_open))

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
