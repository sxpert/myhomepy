# -*- coding: utf-8 -*-
import select

class GenericPoller(object):
    PT_EPOLL = 0
    PT_POLL = 1
    POLLERS = ((PT_EPOLL, 'epoll', ),
               (PT_POLL, 'poll', ))

    _log = None
    poller_type = None
    poller_func = None
    poller = None

    EPOLLIN = None
    EPOLLPRI = None
    EPOLLHUP = None
    EPOLLERR = None
    EPOLLET = None

    POLL_REGISTER_FLAGS = None

    def __init__(self, logger=None):
        self._log = logger
        select_module = dir(select)
        for p_index, p_poller in self.POLLERS:
            if p_poller in select_module:
                self.poller_type = p_index
                self.poller_func = getattr(select, p_poller)
                break
        if self.poller_type is None:
            self._log("ERROR: unable to find a poll function in select module")
            return
        if self.poller_type == self.PT_EPOLL:
            self.EPOLLIN = self.find_flag('EPOLLIN')
            self.EPOLLPRI = self.find_flag('EPOLLPRI')
            self.EPOLLHUP = self.find_flag('EPOLLHUP')
            self.EPOLLERR = self.find_flag('EPOLLERR')
            self.EPOLLET = self.find_flag('EPOLLET')
        if self.poller_type == self.PT_POLL:
            self.EPOLLIN = self.find_flag('POLLIN')
            self.EPOLLPRI = self.find_flag('POLLPRI')
            self.EPOLLHUP = self.find_flag('POLLHUP')
            self.EPOLLERR = self.find_flag('POLLERR')
            self.EPOLLET = self.find_flag('POLLET')
        self.POLL_REGISTER_FLAGS = self.EPOLLIN | self.EPOLLPRI | \
                                   self.EPOLLHUP | self.EPOLLERR | \
                                   self.EPOLLET
        self.poller = self.poller_func()

    def find_flag(self, flag_name):
        if flag_name in dir(select):
            v = getattr(select, flag_name)
            return v
        return 0

    def register(self, fd):
        return self.poller.register(fd, self.POLL_REGISTER_FLAGS)
          
    def poll(self, timeout):
        return self.poller.poll(timeout)
        
    def unregister(self, fd):
        return self.poller.unregister(fd)
