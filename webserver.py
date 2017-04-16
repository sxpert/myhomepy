#!/usr/bin/python
# myOpenApplication webserver

import os, sys, re, shutil
from threading import Thread
import urllib
import myOpenLayer1
import config
import BaseHTTPServer
import mimetypes
import cgi
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

#--------------------------------------------------------------------------------------------------
#
#
#

class OpenWebHandler(BaseHTTPServer.BaseHTTPRequestHandler, object):

    @property
    def _srv(self):
        return '['+unicode(self.server.server_name)+':'+unicode(self.server.server_port)+' WEB]'

    def __log(self, msg):
        myOpenLayer1.SYSTEM_LOGGER.log(msg)

    def _log(self, msg):
        self.__log(self._srv+' '+msg)

    def _log_error(self, msg):
        self.__log((self._srv[:-1]+'_ERROR]')+' '+msg)


    def log(self, code=None, size=None, msg=None):
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
            self._log(msg)
        else:
            self._log_error(msg)

    def log_request(self, code=None, size=None):
        self.log(code, size)

    def log_error(self, format, *args):
        self.log(None, None, format%args)

    #----------------------------------------------------------------------------------------------
    # responses

    def redirect(self, url):
        self.send_response(302)
        self.send_header('Location', url)
        self.end_headers()

    def html_response(self, html, more_headers=None):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html)

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
            ctype += "; charset=%s"%sys.getfilesystemencoding()
        try:
            f = open(destpath, 'rb')
        except IOError:
            self.send_error(404)
            return None
        self.send_response(200)
        self.send_header("Content-type", ctype)
        fs = os.fstat(f.fileno())
        self.send_header("Content-length", unicode(fs[6]))
        self.send_header("Last-modified", self.date_time_string(fs.st_mtime))
        self.end_headers()
        shutil.copyfileobj(f, self.wfile)
        f.close()


    def directory_list_response(self, basedir, path):
        self.log("basedir : '%s' path : '%s'"%(basedir, path))
        basepath = os.path.abspath(os.path.dirname(sys.argv[0]))
        destpath = os.path.join(basepath, basedir, path)
        self.log("destpath : '%s'"%(destpath))
        try:
            l = os.listdir(destpath)
        except os.error:
            self.send_error(404, 'No permission to list directory')
            return None
        l.sort(key=lambda a: a.lower())
        f = StringIO()
        displaypath = cgi.escape(urllib.unquote(self.path))
        f.write('<!DOCTYPE html>')
        f.write("<html>\n<title>Directory listing for %s</title>\n"%displaypath)
        f.write("<body>\n<h2>Directory listing for %s</h2>\n"%displaypath)
        f.write("<hr>\n<ul>\n")
        for name in l:
            fullname = os.path.join(destpath, name)
            displayname = linkname = name
            if os.path.isdir(fullname):
                displayname = name + '/'
                linkname = name + '/'
            if os.path.islink(fullname):
                displayname = name + '@'
            f.write('<li><a href="%s">%s</a>\n'%(urllib.quote(linkname), cgi.escape(displayname)))
        f.write("</ul>\n<hr>\n</body>\n</html>\n")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        encoding = sys.getfilesystemencoding()
        self.send_header("Content-type", "text/html; charset=%s"%encoding)
        self.send_header("Content-length", unicode(length))
        self.end_headers()
        shutil.copyfileobj(f, self.wfile)
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

    #----------------------------------------------------------------------------------------------

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
                        self.__log(unicode(m.groups()))
                    o = c()
                    return o
            if self.server.default is not None:
                # handle default route
                o = self.server.default ()
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

class OpenWeb(Thread):
    def __init__(self, address):
        self.log("initializing thread")
        Thread.__init__(self)
        self.address = address
        self.routes = None
        self.default = None
        self.httpd = None
        self.start()

    def run(self):
        self.log("starting thread")
        self.httpd = BaseHTTPServer.HTTPServer(self.address, OpenWebHandler)
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
            server_name = unicode(self.httpd.server_name)
            server_port = unicode(self.httpd.server_port)
            server = "%s:%s "% (server_name, server_port)
        except AttributeError:
            server = ""
        message = unicode(message)
        myOpenLayer1.SYSTEM_LOGGER.log('[%sWEB] %s'% (server, message))

    def register_routes(self, routes):
        self.routes = routes

    def default_route(self, dr):
        self.default = dr

    def stop(self):
        self.httpd.shutdown()
    
#    def connect(self):
#        pass

#    def recv(self):
#        from socket import error as SocketError
#        import errno
#        try:
#            self._handle_request_noblock()
#        except SocketError as e:
#            # ignore connection reset by peer...
#            if e.errno != errno.ECONNRESET:
#                raise
#            else:
#                self.log('client connection aborted')
#            pass


#    @property
#    def sock(self):
#        return self.socket

if __name__ == '__main__':
    addr = ('', 8000)
    srv = OpenWeb(addr)
    import myOpenLayer1
    system_loop = myOpenLayer1.MainLoop(myOpenLayer1.SYSTEM_LOGGER)
    print srv.sock.fileno()
    system_loop.add_socket(srv)
    system_loop.run()
