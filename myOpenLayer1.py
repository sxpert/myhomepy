#!/usr/bin/python2.7 -3
#-*- coding: utf-8 -*-

#
# (c) Raphael Jacquot 2014
# Licenced under the terms of the GNU GPL v3.0 or later
#

from __future__ import print_function

# system includes
import sys, select, socket, string, types, re, time, errno
import datetime
# application includes
import myOpenPass

DEBUG  = True
logfile = 'myopenlog-2.log'

#--------------------------------------------------------------------------------------------------
#
# System Logger
#

class Logger (object) :
    def __init__ (self, logfile) :
        self.logfile = logfile

    def log (self, msg) :
        # generate datetime string
        d = datetime.datetime.today()
        ds = "%04d-%02d-%02d %02d:%02d:%02d"%(d.year,d.month,d.day,d.hour,d.minute,d.second)
        logmsg = ds+' '+msg
        print(logmsg)
        try :
            lf = open(self.logfile,"a+")
            lf.write(logmsg+'\n')
            lf.close()
        except :
            pass

system_logger = Logger (logfile)

#--------------------------------------------------------------------------------------------------
#
# System main loop, handles events
#

class MainLoop (object) :
    # default timeout 200ms
    def __init__ (self, logger, timeout = 0.2) :
        self.servers = []
        self.sockets = {}
        self.timers = []
        self.logger = logger
        self.timeout = timeout 
        self.poller = select.epoll()

    def add_socket (self, socket):
        # get socket to connect
        socket.connect()
        if socket.sock is not None :
            fd = socket.sock.fileno()
            self.sockets[fd] = socket
            self.poller.register(socket.sock, select.EPOLLIN | select.EPOLLPRI | select.EPOLLHUP | select.EPOLLERR | select.EPOLLET)
        else :
            self.logger.log ('unable to add socket to poller, sock==None')

    def add_server (self, server):
        if server not in self.servers:
            self.servers.append(server)
        self.logger.log(unicode(self.servers))

    def wait_servers (self):
        for s in self.servers:
            self.logger.log("waiting on server "+unicode(s))
            s.stop()
            s.join()
        self.logger.log(unicode("all remaining servers stopped"))

    def remove_socket (self, socket) :
        if socket is not None :
            if socket.sock is not None :
                self.poller.unregister (socket.sock)
                fd = socket.sock.fileno()
                del self.sockets[fd]

    def add_timer (self, ts, callback):
        self.timers.append((ts,callback))
        self.timers = sorted(self.timers, key=lambda timer: timer[0])

    def run (self) :
        while True :
            if self.sockets is not None :
                t = self.timeout
            else :
                # 60 seconds probably too long
                t = 60.0;
            try :
                # should try epoll ;-)
                events = self.poller.poll(t)
                if len(events) > 0 :
                    for e in events :
                        fd, flags = e
                        s = self.sockets[fd]
                        if flags & (select.EPOLLIN | select.EPOLLPRI) :
                            try: 
                                s.recv()
                            except socket.error as e :
                                s.log (unicode(e))
                                if e.errno == errno.ETIMEDOUT :
                                    s.close()
                        elif flags & select.EPOLLHUP :
                            self.logger.log ('socket '+str(s)+' is hanged-up')
                            # remove from poller and reconnect
                            self.poller.unregister (s.sock)
                            del self.sockets[fd]
                            s.reconnect(self)
                        elif flags & select.EPOLLERR :
                            self.logger.log ('socket '+str(s)+' is in error state')
                            # remove from poller and reconnect
                            self.poller.unregister (s.sock)
                            del self.sockets[fd]
                            s.reconnect(self)
                # handle timers
                while len(self.timers)>0 :
                    t = self.timers[0]
                    ts = t[0]
                    now = time.time()
                    if now<ts :
                        break
                    self.timers = self.timers[1:]
                    t[1]()
                # check if one of the socket is disconnected
                for fd in self.sockets.keys() :
                    s = self.sockets[fd]
                    if s.sock is None :
                        self.logger.log ('socket '+unicode(fd)+' disconnected')
                        s.connect ()
                        if s.sock is not None:
                            newfd = s.sock.fileno()
                            if fd != newfd :
                                self.logger.log ('socket '+unicode(fd)+' connected with fd '+unicode(newfd))
                        else:
                            # sleep some...
                            pass
            except KeyboardInterrupt as e:
                self.logger.log ("program exit")
                self.wait_servers()
                sys.exit(0)

#--------------------------------------------------------------------------------------------------
#
# Layer 1 : tcp socket handling
#

class OwnSocket (object) :
    COMMAND = 1
    MONITOR = 2
    MODES = {
        COMMAND: 'CMD',
        MONITOR: 'MON'
    }
    NONE    = 0
    LOGGING = 1
    AUTH    = 2
    LOGGED  = 3
    FAILED  = 4

    NACK    = '*#*0##'
    ACK     = '*#*1##'

    def __init__ (self, address, port, passwd, mode) :
        self.address = address
        self.port = port
        self.passwd = passwd
        self.mode = mode
        self.buf = ''
        self.sock = None
        self.state = self.NONE
        self.ready_callback = None
        self.data_callback = None

    def log (self, msg) :
        col_in = '\033[92m'
        col_out = '\033[0m'
        if self.mode == self.COMMAND:
            col_in = '\033[94m'
        m = '['+self.address+':'+str(self.port)+' '+self.MODES[self.mode]+'] '+col_in+msg+col_out
        system_logger.log(m)

    def connect (self) :
        self.state = self.NONE
        self.sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
        # set keepalive options
        self.sock.setsockopt (socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.sock.setsockopt (socket.SOL_TCP, socket.TCP_KEEPIDLE, 1)
        self.sock.setsockopt (socket.SOL_TCP, socket.TCP_KEEPINTVL, 1)
        self.sock.setsockopt (socket.SOL_TCP, socket.TCP_KEEPCNT, 2)
        self.log ("Initializing connection to "+unicode(self.address)+" port "+unicode(self.port))
        try :
            self.sock.connect ((self.address, self.port))
        except KeyboardInterrupt as e:
            self.log ("program exit")
            sys.exit(0)
        except socket.error as e :
            self.sock = None
            self.log ("connection error, sleeping some")
            # this should setup some timer
            return
        self.sock.setblocking (0)

    def close (self) :
        if self.sock is not None : 
            self.log ('OwnSocket : Closing socket')
            self.sock.close()
            self.sock = None

    def reconnect (self, mainloop) :
        # attempt to reconnect the socket
        self.log ("attempting to reconnect")
        self.close()

    def recv (self) :
        data = self.sock.recv(4096)
        self.buf += data 
        while True :
            p = self.buf.find ('##')
            if p==-1 :
                 return
            msg = self.buf[0:p+2]
            self.buf = self.buf[(p+2):]
            if self.state==self.NONE :
                if msg==self.ACK :
                    self.set_socket_mode()
                    return
                else :
                    self.log('Invalid message received : '+msg)
                    return
            elif self.state==self.LOGGING :
                p = re.compile('\*#(\d+)##')
                m = p.match(msg)
                if m is not None :
                    nonce = m.group(1)
                    self.send_response (nonce)
                else :
                    self.log ('Unable to find Nonce in message '+msg+'##')
                return
            elif self.state==self.AUTH :
                if msg==self.ACK :
                    self.log ('successfully connected')
                    self.state=self.LOGGED
                    if self.ready_callback is not None :
                        self.ready_callback(self)
                else:
                    self.log ('unable to log in')
                    self.state=self.FAILED
                return
            # TODO: do things with messages
            if self.data_callback is not None :
                self.data_callback(msg)
            else :
                self.log('<-RX '+unicode(msg))

    def send (self, msg):
        self.log ('TX-> '+unicode(msg)) 
        self.sock.send(msg)

    def set_socket_mode (self) :
        self.log('initializing connection')
        if self.mode == self.COMMAND :
            self.send('*99*0##')
            self.state = self.LOGGING
        elif self.mode == self.MONITOR :
            self.send('*99*1##')
            self.state = self.LOGGING
        else :
            self.log ("unknown connection type : "+str(self.mode))

    def send_response (self, nonce) :
        self.log ('got nonce '+nonce)
        p = '*#'+str(myOpenPass.ownCalcPass (self.passwd, nonce))+'##'
        self.log ('logging in with password packet '+p)
        self.state = self.AUTH
        self.send (p)

    def set_ready_callback (self, callback) :
        self.ready_callback = callback

    def set_data_callback (self, callback) :
        self.data_callback = callback

#--------------------------------------------------------------------------------------------------
#
# test program
#

if __name__ == '__main__' :
    import config
    system_loop = MainLoop(system_logger)
    # test program
    s = OwnSocket(config.host,config.port,config.password,OwnSocket.MONITOR)
    system_loop.add_socket(s)
    system_loop.run()
