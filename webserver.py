#!/usr/bin/python
# myOpenApplication webserver

import myOpenLayer1
import BaseHTTPServer


class OpenWebHandler (BaseHTTPServer.BaseHTTPRequestHandler, object):

    def log (self):
        msg = '['+unicode(self.server.server_name)+':'+unicode(self.server.server_port)+' WEB] '
        msg+= self.address_string()+' '+self.command+' '+unicode(self.path)
        myOpenLayer1.system_logger.log (msg)

    def do_GET(self):
        self.log()


        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write('Hello, world!')

class OpenWeb (BaseHTTPServer.HTTPServer, object):
    def __init__ (self, address):
        super(OpenWeb, self).__init__(address, OpenWebHandler)
   
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
