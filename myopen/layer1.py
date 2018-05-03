#!/usr/bin/python3
# -*- coding: utf-8 -*-

# #!/usr/bin/python2.7 -3

#
# (c) Raphael Jacquot 2014
# Licenced under the terms of the GNU GPL v3.0 or later
#

from __future__ import print_function

import datetime
import errno
import re
import select
import socket
# system includes
import sys
import time
from threading import Thread

# application includes
from . import openpass

DEBUG = True
LOGFILE = 'myopenlog-2.log'


# --------------------------------------------------------------------------------------------------
#
# System Logger
#

class Logger(object):
    def __init__(self, logfile):
        self.logfile = logfile

    def log(self, msg):
        # generate datetime string
        current_date = datetime.datetime.today()
        date_string = "%04d-%02d-%02d %02d:%02d:%02d" % (
            current_date.year,
            current_date.month,
            current_date.day,
            current_date.hour,
            current_date.minute,
            current_date.second)
        if type(msg) is not str:
            msg = str(msg)
        logmsg = '%s %s' % (date_string, msg)
        print(logmsg)
        try:
            # TODO: syslog ?
            log_file = open(self.logfile, "a+")
            log_file.write(logmsg+'\n')
            log_file.close()
        except:
            pass

SYSTEM_LOGGER = Logger(LOGFILE)


# --------------------------------------------------------------------------------------------------
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

    def log(self, msg):
        col_in = '\033[91m'
        col_out = '\033[0m'
        self.logger.log('[LOOP] ' + col_in + msg + col_out)

    def add_task(self, task):
        self.log("adding task "+str(task))
        self.tasks.append(task)

    def wait_all(self):
        """
        stops all registered tasks,
        then joins them
        """
        for task in self.tasks:
            self.logger.log("waiting on server "+str(task))
            task.stop()
            try:
                task.join()
            except KeyboardInterrupt:
                pass
        self.log(str("all remaining servers stopped"))

    def run(self):
        """
        main program loop.
        handles keyboard interrupt, stops all other threads in that case
        """
        # start all registered tasks
        for task in self.tasks:
            # try starting the task
            try:
                task.start()
            except RuntimeError:
                # hah, task already started, ignore
                pass
        try:
            self.log("running main loop")
            while not self.stopped:
                time.sleep(1)
                # cleanup dead threads
                tasklist = []
                changed = False
                for t in self.tasks:
                    if not t.is_alive():
                        self.log("task %s is dead" % (str(t)))
                        t.join(0.1)
                        changed = True
                    else:
                        tasklist.append(t)
                if changed:
                    # self.log("task list %s" % (str(tasklist)))
                    self.tasks = tasklist
        except KeyboardInterrupt:
            self.log("^C forcing program exit")
            self.wait_all()
            sys.exit(0)


# --------------------------------------------------------------------------------------------------
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

    def __init__(self, address, port, passwd, mode,
                 timeout=0.2, auto_reconnect=True):
        self.address = address
        self.port = port
        self.passwd = passwd
        self.mode = mode
        self.auto_reconnect = auto_reconnect
        self.buf = ''
        self.sock = None
        self.sockfd = None
        self.state = self.NONE
        self.ready_callback = None
        self.data_callback = None
        self.stopping = False
        self.timeout = timeout
        self.cnxfailcnt = 0
        self.poller = select.epoll()
        super().__init__()

    def create_clone(self, mode):
        new_socket = OwnSocket(self.address,
                               self.port,
                               self.passwd,
                               mode,
                               self.timeout)
        return new_socket

    def stop(self):
        self.stopping = True

    def run(self):
        while not self.stopping:
            if self.sock is not None or self.cnxfailcnt < 3:
                timeout = self.timeout
            else:
                # 60 seconds probably too long
                timeout = 5.0
            if self.sock is None:
                self.connect()
                # setup poller object after connecting
                if self.sock is not None:
                    self.poller.register(self.sockfd,
                                         select.EPOLLIN | select.EPOLLPRI |
                                         select.EPOLLHUP | select.EPOLLERR |
                                         select.EPOLLET)
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
                                # self.log("flags: "+bin(flags)[2:])
                                if flags & (select.EPOLLIN | select.EPOLLPRI):
                                    try:
                                        self.recv()
                                    except socket.error as e:
                                        self.log(str(e))
                                        if e.errno == errno.ETIMEDOUT:
                                            self.close()
                                elif flags & select.EPOLLHUP:
                                    self.log('socket '+str(self) +
                                             ' is hanged-up')
                                    # remove from poller and reconnect
                                    self.poller.unregister(self.sockfd)
                                    self.reconnect()
                                elif flags & select.EPOLLERR:
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
                    self.log("Keyboard Interrupt in OWNSocket thread")
                    self.stopping = True
        self.log("quitting task %s" % (str(self)))

    def log(self, msg):
        col_in = '\033[92m'
        col_out = '\033[0m'
        if self.mode == self.COMMAND:
            col_in = '\033[94m'
        _msg = '[' + self.address + ':' + str(self.port) + ' ' + \
            self.MODES[self.mode] + '] ' + col_in + msg + col_out
        SYSTEM_LOGGER.log(_msg)

    def connect(self):
        self.state = self.NONE
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # set keepalive options
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPIDLE, 1)
        self.sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPINTVL, 1)
        self.sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPCNT, 2)
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
                    if self.ready_callback is not None:
                        self.ready_callback()
                else:
                    self.log('unable to log in')
                    self.state = self.FAILED
                return
            if self.data_callback is not None:
                self.data_callback(msg)
            else:
                self.log('<-RX '+str(msg))

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


class CommandDialog(OwnSocket):
    def __init__(self, clone):
        super().__init__(clone.address,
                         clone.port,
                         clone.passwd,
                         self.COMMAND,
                         clone.timeout,
                         # auto_reconnect is false
                         False)
        self.ready_callback = self.dialog_ready
        self.data_callback = self.dialog_data

    def dialog_ready(self):
        self.log("DIALOG: ready")

    def dialog_data(self, msg):
        self.log("DIALOG: msg")

# --------------------------------------------------------------------------------------------------
#
# test program
#

if __name__ == '__main__':
    import config
    SYSTEM_LOOP = MainLoop(SYSTEM_LOGGER)
    # test program
    OWN_SOCK = OwnSocket(config.host,
                         config.port,
                         config.password,
                         OwnSocket.MONITOR)
    SYSTEM_LOOP.add_socket(OWN_SOCK)
    SYSTEM_LOOP.run()
