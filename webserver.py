#!/usr/bin/python
# myOpenApplication webserver

import re
import urllib
import myOpenLayer1
import config
import BaseHTTPServer

#--------------------------------------------------------------------------------------------------
#
#
#

class OpenWebHandler (BaseHTTPServer.BaseHTTPRequestHandler, object):

    def log (self, code=None, size=None, msg=None):
        srv = '['+unicode(self.server.server_name)+':'+unicode(self.server.server_port)+' WEB]'
        if msg is None:
            if self.command is None:
                # note: there is no path to display
                req = self.address_string()+' [Unknown Command] '
            else:
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
        if self.server.routes is None:
            return None
        for r in self.server.routes :
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
        self.routes = None
        super(OpenWeb, self).__init__(address, OpenWebHandler)
        myOpenLayer1.system_logger.log ('['+unicode(self.server_name)+':'+unicode(self.server_port)+' WEB] starting')
   
    def register_routes(self, routes):
        self.routes = routes

    def connect (self):
        pass
    
    def recv (self):
        from socket import error as SocketError
        import errno
        try:
            self._handle_request_noblock()
        except SocketError as e:
            # ignore connection reset by peer...
            if e.errno != errno.ECONNRESET:
                raise
            pass


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
