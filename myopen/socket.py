#!/usr/bin/python3
# -*- coding: utf-8 -*-

# #!/usr/bin/python2.7 -3

#
# (c) Raphael Jacquot 2014
# Licenced under the terms of the GNU GPL v3.0 or later
#

import errno
import re
import socket
import sys
import time
from threading import Thread

from core.logger import SYSTEM_LOGGER
from core.poller import GenericPoller
from core.tasklist import TaskList

from . import openpass

# --------------------------------------------------------------------------------------------------
#
# Layer 1 : tcp socket handling
#

class OWNSocket(Thread):
    COMMAND = 1
    MONITOR = 2
    MODES = {
        COMMAND: 'CMD',
        MONITOR: 'MON'
    }
    NONE = 0
    LOGGING = 1
    AUTH = 2
    LOGGED = 3
    FAILED = 4

    NACK = '*#*0##'
    ACK = '*#*1##'

    _main_loop = None
    _tasks = None
    _callback = None

    address = '192.168.1.35'
    auto_reconnect = True
    buf = ''
    cnxfailcnt = 0
    mode = None
    poller = None
    port = 20000
    passwd = '12345'
    sock = None
    sockfd = None
    state = NONE
    stopping = False
    timeout = 0.2
    
    def __init__(self, address, port, passwd, mode=None,
                 timeout=0.2, auto_reconnect=True):
        self.address = address
        self.port = port
        self.passwd = passwd
        if mode is not None:
            self.mode = mode
        self.auto_reconnect = auto_reconnect
        self.timeout = timeout
        self._tasks = TaskList(self)
        self.log('OWNSocket.__init__: %s' % (str(self._tasks._tasks)))
        super().__init__()

    def create_clone(self, mode):
        new_socket = OWNSocket(self.address,
                               self.port,
                               self.passwd,
                               mode,
                               self.timeout)
        return new_socket

    def stop(self):
        self.stopping = True

    def run(self):
        while not self.stopping:
            if self.poller is None:
                self.poller = GenericPoller(self.log)
                
            if self.sock is not None or self.cnxfailcnt < 3:
                timeout = self.timeout
            else:
                # 60 seconds probably too long
                timeout = 5.0
            if self.sock is None:
                self.connect()
                # setup poller object after connecting
                if self.sock is not None:
                    self.poller.register(self.sockfd)
                else:
                    self.log('unable to add socket to poller, sock==None')
                    try:
                        time.sleep(timeout)
                    except KeyboardInterrupt:
                        self.log('KeyboardInterrupt while waiting for '
                                 'network event')
                        self.stopping = True
            else:
                try:
                    events = self.poller.poll(timeout)
                    if len(events) > 0:
                        for event in events:
                            filedesc, flags = event
                            if self.sockfd != filedesc:
                                self.log('problem, socket\'s fd (%d) is'
                                         ' different from given fd (%d)' % (
                                             self.sockfd, filedesc,))
                            else:
                                if flags & (self.poller.EPOLLIN | self.poller.EPOLLPRI):
                                    try:
                                        self.recv()
                                    except socket.error as e:
                                        self.log(str(e))
                                        if e.errno == errno.ETIMEDOUT:
                                            self.close()
                                elif flags & self.poller.EPOLLHUP:
                                    self.log('socket '+str(self) +
                                             ' is hanged-up')
                                    # remove from poller and reconnect
                                    self.poller.unregister(self.sockfd)
                                    self.reconnect()
                                elif flags & self.poller.EPOLLERR:
                                    self.log('socket '+str(self) +
                                             ' is in error state')
                                    # remove from poller and reconnect
                                    self.poller.unregister(self.sockfd)
                                    self.reconnect()
                    else:
                        # check if socket is disconnected
                        try:
                            data = self.sock.recv(1, socket.MSG_PEEK)
                        except IOError as error:
                            if error.errno == errno.EWOULDBLOCK:
                                # nothing to be read, pass
                                pass
                            else:
                                self.log(str(error))
                        else:
                            if len(data) == 0:
                                self.log('socket disconnected')
                                self.poller.unregister(self.sockfd)
                                if self.auto_reconnect:
                                    self.reconnect()
                                else:
                                    self.log('disconnecting socket')

                                    self.stopping = True
                        # look for things to do in the queue
                        self._tasks.execute_next()

                        # no event, check timers
                        # handle timers
                        # while len(self.timers) > 0:
                        #     t = self.timers[0]
                        #     ts = t[0]
                        #     now = time.time()
                        #     if now < ts:
                        #         break
                        #     self.timers = self.timers[1:]
                        #     t[1]()
                        pass
                except IOError as error:
                    if error.errno == 4:
                        # just ignore this
                        self.log('Interrupted System Call')
                        pass
                except KeyboardInterrupt:
                    # should not happen, normally caught by the main loop class
                    self.log("Keyboard Interrupt in %s thread"
                             % (self.__class__.__name__))
                    self.stopping = True

        self.log('do we have a callback function ?')
        if callable(self._callback):
            self._callback() # pylint: disable=E1102
        else:
            self.log('callback was not callable')
            try:
                r = getattr(self._callback, 'run')
            except AttributeError as e:
                self.log(str(e))
            else:
                r()

        self.log("quitting task %s" % (str(self)))

    @property
    def mainloop(self):
        return self._main_loop

    @mainloop.setter
    def mainloop(self, value):
        self._main_loop = value

    def log(self, msg):
        col_in = '\033[92m'
        col_out = '\033[0m'
        if self.mode == self.COMMAND:
            col_in = '\033[94m'
        if self._main_loop is not None:
            _ident = '%d' % (self._main_loop.get_index(self))
        else:
            _ident = '<new>'
        _msg = '[%s:%d %s-%s] %s%s%s' % (
            self.address,
            self.port,
            self.MODES[self.mode],
            _ident,
            col_in,
            str(msg),
            col_out
        )
        SYSTEM_LOGGER.log(_msg)

    def connect(self):
        self.state = self.NONE
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # set keepalive options

        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        keepidle_supported = True
        try:
            self.sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPIDLE, 1)
        except AttributeError:
            # suspect we're on a platform that doesn't support this
            # for instance, Mac OS X
            keepidle_supported = False
            # self.log("Running on a platform that doesn't suport KEEPIDLE")
        if not keepidle_supported :    
            self.sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPINTVL, 1)
            self.sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPCNT, 2)
        else:
            # self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPALIVE, 2)
            pass
        
        # set socket as non-blocking (to avoid the idiotic timeout on connect)
        self.log("Initializing connection to " + str(self.address) +
                 " port " + str(self.port))
        try:
            self.sock.settimeout(1)
            self.sock.connect((self.address, self.port))
        except KeyboardInterrupt:
            self.log("program exit")
            sys.exit(0)
        except socket.error:
            self.sock = None
            self.cnxfailcnt += 1
            self.log("connection error, sleeping some")
            # this should setup some timer
            return
        self.cnxfailcnt = 0
        self.sockfd = self.sock.fileno()
        self.sock.setblocking(0)

    def close(self):
        if self.sock is not None:
            self.log('%s : Closing socket' % (self.__class__.__name__))
            self.sock.close()
            self.sock = None
            self.sockfd = None

    def reconnect(self):
        # attempt to reconnect the socket
        self.log("attempting to reconnect")
        self.close()

    def recv(self):
        data = self.sock.recv(4096)
        self.buf += data.decode('latin1')
        while True:
            position = self.buf.find('##')
            if position == -1:
                return
            msg = self.buf[0:position+2]
            self.log(msg)
            self.buf = self.buf[(position+2):]
            if self.state == self.NONE:
                if msg == self.ACK:
                    self.set_socket_mode()
                    return
                else:
                    self.log('Invalid message received : '+msg)
                    return
            elif self.state == self.LOGGING:
                nonce_re = re.compile(r'\*#(\d+)##')
                m = nonce_re.match(msg)
                if m is not None:
                    nonce = m.group(1)
                    self.send_response(nonce)
                else:
                    self.log('Unable to find Nonce in message '+msg+'##')
                return
            elif self.state == self.AUTH:
                if msg == self.ACK:
                    self.log('successfully connected')
                    self.state = self.LOGGED
                    self.ready_callback()
                else:
                    self.log('unable to log in')
                    self.state = self.FAILED
                return
            self.data_callback(msg)

    def send(self, msg):
        self.log('TX-> '+str(msg))
        self.sock.send(msg.encode('latin1'))

    def set_socket_mode(self):
        self.log('initializing connection')
        if self.mode == self.COMMAND:
            self.send('*99*0##')
            self.state = self.LOGGING
        elif self.mode == self.MONITOR:
            self.send('*99*1##')
            self.state = self.LOGGING
        else:
            self.log("unknown connection type : "+str(self.mode))

    def send_response(self, nonce):
        self.log('got nonce '+nonce)
        password_message = '*#%s##' % (
            str(openpass.ownCalcPass(self.passwd, nonce)))
        self.log('logging in with password packet '+password_message)
        self.state = self.AUTH
        self.send(password_message)

    def ready_callback(self):
        pass

    def data_callback(self, msg):
        self.log('<-RX '+str(msg))

    def push_task(self, task, wait=True, callback=None, params=None):
        return self._tasks.push(task, wait, callback, params)