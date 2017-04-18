#!/usr/bin/python3
#-*- coding: utf-8 -*-

##!/usr/bin/python2.7 -3

#
# (c) Raphael Jacquot 2014
# Licenced under the terms of the GNU GPL v3.0 or later
#

from __future__ import print_function

# system includes
import sys
import select
import socket
import re
import time
import errno
import datetime
# application includes
import myOpenPass
from threading import Thread

DEBUG = True
LOGFILE = 'myopenlog-2.log'

#--------------------------------------------------------------------------------------------------
#
# System Logger
#

class Logger(object):
    def __init__(self, logfile):
        self.logfile = logfile

    def log(self, msg):
        # generate datetime string
        current_date = datetime.datetime.today()
        date_string = "%04d-%02d-%02d %02d:%02d:%02d"%(
            current_date.year,
            current_date.month,
            current_date.day,
            current_date.hour,
            current_date.minute,
            current_date.second)
        logmsg = date_string+' '+msg
        print(logmsg)
        try:
            # TODO: syslog ?
            log_file = open(self.logfile, "a+")
            log_file.write(logmsg+'\n')
            log_file.close()
        except:
            pass

SYSTEM_LOGGER = Logger(LOGFILE)

#--------------------------------------------------------------------------------------------------
#
# System main loop, handles events
#

class MainLoop(object):
    """
    main program loop
    manages threads
    """
    def __init__(self, logger, timeout=0.2):
        self.tasks = []
        self.timers = []
        self.stopped = False
        self.logger = logger
        self.timeout = timeout

    def add_task(self, task):
        print("adding task "+unicode(task))
        self.tasks.append(task)


    def wait_all(self):
        """
        stops all registered tasks,
        then joins them
        """
        for task in self.tasks:
            self.logger.log("waiting on server "+unicode(task))
            task.stop()
            task.join()
        self.logger.log(unicode("all remaining servers stopped"))

    def run(self):
        """
        main program loop.
        handles keyboard interrupt, stops all other threads in that case
        """
        # start all registered tasks
        for task in self.tasks:
            if not task.is_alive():
                task.start()
        try:
            print("running thread")
            while not self.stopped:
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.log("^C forcing program exit")
            self.wait_all()
            sys.exit(0)

#--------------------------------------------------------------------------------------------------
#
# Layer 1 : tcp socket handling
#

class OwnSocket(Thread):
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

    def __init__(self, address, port, passwd, mode, timeout = 0.2):
        self.address = address
        self.port = port
        self.passwd = passwd
        self.mode = mode
        self.buf = ''
        self.sock = None
        self.sockfd = None
        self.state = self.NONE
        self.ready_callback = None
        self.data_callback = None
        self.stopping = False
        self.timeout = timeout
        self.poller = select.epoll()
        Thread.__init__(self)

    def stop(self):
        self.stopping = True

    def run(self):
        while not self.stopping:
            if self.sock is None:
                self.connect()
                # setup poller object after connecting
                if self.sock is not None:
                    self.sockfd = self.sock.fileno()
                    self.poller.register(self.sockfd,
                                         select.EPOLLIN | select.EPOLLPRI |
                                         select.EPOLLHUP | select.EPOLLERR | select.EPOLLET)
                else:
                    self.log('unable to add socket to poller, sock==None')
            else:
                if self.sock is not None:
                    timeout = self.timeout
                else:
                    # 60 seconds probably too long
                    timeout = 60.0
                try:
                    events = self.poller.poll(timeout)
                    if len(events) > 0:
                        for event in events:
                            filedesc, flags = event
                            if self.sockfd != filedesc:
                                self.log('problem, socket\'s fd (%d) is'\
                                         ' different from given fd (%d)'%(
                                             self.sockfd, filedesc,))
                            else:
                                # filedesc should be the same as the socket's fd
                                if flags & (select.EPOLLIN | select.EPOLLPRI):
                                    try:
                                        self.recv()
                                    except socket.error as e:
                                        self.log(unicode(e))
                                        if e.errno == errno.ETIMEDOUT:
                                            self.close()
                                elif flags & select.EPOLLHUP:
                                    self.log('socket '+str(self)+' is hanged-up')
                                    # remove from poller and reconnect
                                    self.poller.unregister(self.sockfd)
                                    self.reconnect()
                                elif flags & select.EPOLLERR:
                                    self.log('socket '+str(self)+' is in error state')
                                    # remove from poller and reconnect
                                    self.poller.unregister(self.sockfd)
                                    self.reconnect()
                except KeyboardInterrupt:
                    # should not happen, normally caught by the main loop class
                    self.log("Keyboard Interrupt in OWNSocket thread")
#                 # handle timers
#                 while len(self.timers) > 0:
#                     t = self.timers[0]
#                     ts = t[0]
#                     now = time.time()
#                     if now < ts:
#                         break
#                     self.timers = self.timers[1:]
#                     t[1]()

    def log(self, msg):
        col_in = '\033[92m'
        col_out = '\033[0m'
        if self.mode == self.COMMAND:
            col_in = '\033[94m'
        _msg = '['+self.address+':'+str(self.port)+' '+self.MODES[self.mode]+'] '+col_in+msg+col_out
        SYSTEM_LOGGER.log(_msg)

    def connect(self):
        self.state = self.NONE
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # set keepalive options
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPIDLE, 1)
        self.sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPINTVL, 1)
        self.sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPCNT, 2)
        self.log("Initializing connection to "+unicode(self.address)+" port "+unicode(self.port))
        try:
            self.sock.connect((self.address, self.port))
        except KeyboardInterrupt:
            self.log("program exit")
            sys.exit(0)
        except socket.error:
            self.sock = None
            self.log("connection error, sleeping some")
            # this should setup some timer
            return
        self.sock.setblocking(0)

    def close(self):
        if self.sock is not None:
            self.log('OwnSocket : Closing socket')
            self.sock.close()
            self.sock = None
            self.sockfd = None

    def reconnect(self):
        # attempt to reconnect the socket
        self.log("attempting to reconnect")
        self.close()

    def recv(self):
        data = self.sock.recv(4096)
        self.buf += data
        while True:
            position = self.buf.find('##')
            if position == -1:
                return
            msg = self.buf[0:position+2]
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
                    if self.ready_callback is not None:
                        self.ready_callback(self)
                else:
                    self.log('unable to log in')
                    self.state = self.FAILED
                return
            if self.data_callback is not None:
                self.data_callback(msg)
            else:
                self.log('<-RX '+unicode(msg))

    def send(self, msg):
        self.log('TX-> '+unicode(msg))
        self.sock.send(msg)

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
        password_message = '*#'+str(myOpenPass.ownCalcPass(self.passwd, nonce))+'##'
        self.log('logging in with password packet '+password_message)
        self.state = self.AUTH
        self.send(password_message)

    def set_ready_callback(self, callback):
        """
        sets the callback for when the connection is ready
        """
        self.ready_callback = callback

    def set_data_callback(self, callback):
        """
        sets the data callback
        """
        self.data_callback = callback

#--------------------------------------------------------------------------------------------------
#
# test program
#

if __name__ == '__main__':
    import config
    SYSTEM_LOOP = MainLoop(SYSTEM_LOGGER)
    # test program
    OWN_SOCK = OwnSocket(config.host, config.port, config.password, OwnSocket.MONITOR)
    SYSTEM_LOOP.add_socket(OWN_SOCK)
    SYSTEM_LOOP.run()
