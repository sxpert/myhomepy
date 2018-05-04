#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# myOpenApplication webserver

import cgi
import http.server
import json
import mimetypes
import os
import re
import shutil
import socket
import socketserver
import ssl
import sys
import traceback
import urllib
from io import StringIO
from threading import Thread


# --------------------------------------------------------------------------------------------------
#
#
#

class OpenWebHandler(http.server.BaseHTTPRequestHandler, object):

    def __init__(self, request, client_address, server):
        self.server = server
        self.config = server.web.app.config
        super().__init__(request, client_address, server)

    @property
    def _srv(self):
        return '[%s:%s WEB]' % (str(self.server.server_name),
                                str(self.server.server_port))

    def __log(self, msg):
        self.server.web.app.system_logger.log(msg)

    def _log(self, msg):
        self.__log('%s %s' % (str(self._srv), str(msg)))

    def _log_error(self, msg):
        self.__log((self._srv[:-1]+'_ERROR]')+' '+msg)

    def log(self, code=None, size=None, msg=None):
        if msg is None:
            if self.command is None:
                # note: there is no path to display
                req = self.address_string()+' [Unknown Command] '
            else:
                req = self.address_string()+' '+self.command+' '+str(self.path)
            res = str(code)
            if size is not None:
                res += ' '+str(size)
            msg = req+' '+res
            self._log(msg)
        else:
            self._log_error(msg)

    def log_request(self, code=None, size=None):
        self.log(code, size)

    def log_error(self, format, *args):
        self.log(None, None, format % args)

    # ----------------------------------------------------------------------------------------------
    # responses

    def redirect(self, url):
        self.send_response(302)
        self.send_header('Location', url)
        self.end_headers()

    def html_response(self, html, more_headers=None):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def json_response(self, json_data):
        try:
            json_string = json.dumps(json_data)
        except Exception as error:
            print("Error while dumping data to json format")
            exc_type, exc_value, exc_traceback = sys.exc_info()
            for traceback_line in traceback.format_tb(exc_traceback):
                print(traceback_line)
            print(str(exc_type.__name__)+" : "+str(exc_value))
            self.send_error(500)
        else:
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json_string.encode('utf-8'))

    def file_response(self, basedir, path):
        """
        this method responds with the contents of the file which is given
        in the path argument. Lookups are limited to the contents of the
        basedir directory and its subdirectories
        if path points to a directory, displays the list of files in the
        directory
        """
        # remove all traces of '/' at the begining of the path,
        # this prevents doing things like //etc/
        while len(path) > 0 and path[0] == '/':
            path = path[1:]
        basepath = os.path.abspath(os.path.dirname(sys.argv[0]))
        destpath = os.path.join(basepath, basedir, path)
        if os.path.isdir(destpath):
            if len(path) > 0 and not path.endswith('/'):
                # redirect to proper path
                return self.redirect(path+'/')
            for index in 'index.html', 'index.htm':
                full_index = os.path.join(destpath, index)
                if os.path.exists(full_index):
                    path = os.path.join(path, index)
                    destpath = full_index
                    break
            else:
                return self.directory_list_response(basedir, path)
        ctype = self.guess_type(destpath)
        if ctype == "text/html":
            ctype += "; charset=%s" % sys.getfilesystemencoding()
        try:
            f = open(destpath, 'rb')
        except IOError:
            self.send_error(404)
            return None
        self.send_response(200)
        self.send_header("Content-type", ctype)
        fs = os.fstat(f.fileno())
        self.send_header("Content-length", str(fs[6]))
        self.send_header("Last-modified", self.date_time_string(fs.st_mtime))
        self.end_headers()
        shutil.copyfileobj(f, self.wfile)
        f.close()

    def directory_list_response(self, basedir, path):
        self.log("basedir : '%s' path : '%s'" % (basedir, path))
        basepath = os.path.abspath(os.path.dirname(sys.argv[0]))
        destpath = os.path.join(basepath, basedir, path)
        self.log("destpath : '%s'" % (destpath))
        try:
            l = os.listdir(destpath)
        except os.error:
            self.send_error(404, 'No permission to list directory')
            return None
        l.sort(key=lambda a: a.lower())
        f = StringIO()
        displaypath = cgi.escape(urllib.parse.unquote(self.path))
        f.write('<!DOCTYPE html>')
        f.write("<html>\n<title>Directory listing for %s</title>\n" %
                displaypath)
        f.write("<body>\n<h2>Directory listing for %s</h2>\n" % displaypath)
        f.write("<hr>\n<ul>\n")
        for name in l:
            fullname = os.path.join(destpath, name)
            displayname = linkname = name
            if os.path.isdir(fullname):
                displayname = name + '/'
                linkname = name + '/'
            if os.path.islink(fullname):
                displayname = name + '@'
            f.write('<li><a href="%s">%s</a>\n' %
                    (urllib.parse.quote(linkname), cgi.escape(displayname)))
        f.write("</ul>\n<hr>\n</body>\n</html>\n")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        encoding = sys.getfilesystemencoding()
        self.send_header("Content-type", "text/html; charset=%s" % encoding)
        self.send_header("Content-length", str(length))
        self.end_headers()
        self.wfile.write(f.getvalue().encode('utf-8'))
        f.close()

    def guess_type(self, path):
        import posixpath
        base, ext = posixpath.splitext(path)
        if ext in self.extension_map:
            return self.extension_map[ext]
        ext = ext.lower()
        if ext in self.extension_map:
            return self.extension_map[ext]
        else:
            return self.extension_map['']

    if not mimetypes.inited:
        mimetypes.init()
    extension_map = mimetypes.types_map.copy()
    extension_map.update({
        '': 'application/octet-stream',
        '.py': 'text/plain',
        '.h': 'text/plain',
        '.c': 'text/plain'
    })

    # ----------------------------------------------------------------------------------------------

    def find_route(self):
        if self.server.routes is None:
            return None
        else:
            for r in self.server.routes:
                e, c = r
                m = re.match(e, self.path)
                if m is not None:
                    g = m.groups()
                    if len(g) > 0:
                        self.__log("find_route : [match groups] %s" %
                                   (str(m.groups())))
                    o = c()
                    return o
            if self.server.default is not None:
                # handle default route
                o = self.server.default()
                return o
            self.send_error(404)
            return None

    def do_request(self):
        # if self.config is None:
        #     self.config = config
        o = self.find_route()
        if o is None:
            return
        mname = 'do_'+self.command
        if not hasattr(o, mname):
            self.send_error(501, "Unsupported method (%r)" % self.command)
            return
        method = getattr(o, mname)
        try:
            method(self)
        except Exception as error:
            print("ERROR WHILE do_request : ")
            exc_type, exc_value, exc_traceback = sys.exc_info()
            for traceback_line in traceback.format_tb(exc_traceback):
                print(traceback_line)
            print(str(exc_type.__name__)+" : "+str(exc_value))
            print("sending 500 error")
            self.send_error(500)

    def do_GET(self):
        self.do_request()

    def do_POST(self):
        if not self.parse_variables():
            # response already sent in this case
            return
        self.do_request()

    # ----------------------------------------------------------------------------------------------
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
                k = urllib.parse.unquote(b[0:pos])
                v = urllib.parse.unquote_plus(b[pos+1:])
                if len(k) > 2 and k[-2:] == '[]':
                    k = k[:-2]
                    try:
                        tv = self.variables[k]
                    except KeyError as e:
                        tv = []
                    tv.append(v)
                    v = tv
                self.variables[k] = v

    def parse_url_variables(self):
        self.variables = {}

    def parse_post_urlencoded_variables(self):
        try:
            l = self.headers['content-length']
        except KeyError as e:
            self.send_error(501,
                            "unable to find content length for posted data")
            return False
        # limit check on length
        d = self.rfile.read(int(l))
        # parse variable stream
        # note: d is bytes
        self.parse_variables_string(d.decode('utf-8'))
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
        self.__log('unknown content-type: '+t)
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
                v += "&lt;"
            elif c == ">":
                v += "&gt;"
            elif c == "&":
                v += "&amp;"
            elif c == "\"":
                v += "&quot;"
            else:
                v += c
        return v


# --------------------------------------------------------------------------------------------------
#
# TODO: ssl mode
#
# import BaseHTTPServer, SimpleHTTPServer
# import ssl
#
# httpd = BaseHTTPServer.HTTPServer(('localhost', 4443),
#                                   SimpleHTTPServer.SimpleHTTPRequestHandler)
# httpd.socket = ssl.wrap_socket (httpd.socket,
#                                 certfile='path/to/localhost.pem',
#                                 server_side=True)
# httpd.serve_forever()
#

#
#
# web server object
#

class OWNHTTPServer(socketserver.TCPServer):
    web = None
    allow_reuse_address = 1    # Seems to make sense in testing environment

    def __init__(self,
                 server_address,
                 RequestHandlerClass,
                 bind_and_activate=True,
                 web=None):
        self.web = web
        super().__init__(server_address, RequestHandlerClass, False)

        # do ssl initialization here
        tls_ok = False
        if self.web is not None:
            config = self.web.app.config
            if config.tls.available:
                self.log("we'll be using TLS")
                key_file = config.tls.key
                cert_file = config.tls.cert
                self.socket = ssl.wrap_socket(self.socket,
                                              keyfile=key_file,
                                              certfile=cert_file,
                                              cert_reqs=ssl.CERT_NONE)
                tls_ok = True
        if not tls_ok:
            self.log("WARNING: All web communications are in CLEARTEXT")

        if bind_and_activate:
            try:
                self.server_bind()
                self.server_activate()
            except:
                self.server_close()
                raise

    def log(self, message):
        if self.web is None:
            print(message)
            return
        self.web.log(message)

    def process_request(self, request, client_address):
        """Call finish_request.
        TODO: Override to catch errno 32 in finish request
        """
        self.finish_request(request, client_address)
        self.shutdown_request(request)

    def server_bind(self):
        """Override server_bind to store the server name."""
        socketserver.TCPServer.server_bind(self)
        host, port = self.socket.getsockname()[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port


#
#
# web server thread
#

class OpenWeb(Thread):
    app = None
    address = None
    routes = None
    default = None
    httpd = None

    def __init__(self, app, address):
        self.app = app
        self.log("initializing webserver thread")
        Thread.__init__(self)
        self.address = address

    def run(self):
        self.log("starting Webserver thread")
#        self.httpd = BaseHTTPServer.HTTPServer(self.address, OpenWebHandler)
        self.httpd = OWNHTTPServer(self.address, OpenWebHandler, web=self)
        if self.routes is None:
            self.log("error, no routes set")
            return
        if self.default is None:
            self.log("error, no default set")
            return
        self.httpd.routes = self.routes
        self.httpd.default = self.default
        self.httpd.serve_forever()

    def log(self, message):
        try:
            server_name = str(self.httpd.server_name)
            server_port = str(self.httpd.server_port)
            server = "%s:%s " % (server_name, server_port)
        except AttributeError:
            server = ""
        message = str(message)
        if self.app is None:
            print(message)
            return
        self.app.system_logger.log('[%sWEB] %s' % (server, message))

    def register_routes(self, routes):
        self.routes = routes
        self.log("%d Routes initialized" % (len(routes)))
        self.start()

    def default_route(self, dr):
        self.default = dr

    def stop(self):
        self.httpd.shutdown()
