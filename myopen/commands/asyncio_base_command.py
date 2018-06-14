# -*- coding: utf-8 -*-
from myopen.message import Message

__all__ = ['BaseCommand']


class BaseCommand(object):

    def __init__(self, system, params=None, callback=None):
        self.system = system
        self.log = system.log
        self.msg_handler = None
        self._ended = False
        self.params = params
        self.callback = callback

    @property
    def is_done(self):
        return self._ended

    def start(self):
        # self.log('%s does nothing' % self.__class__.__name__)
        pass

    def send(self, msg):
        self.system.gateway.send(msg)

    def dispatch(self, msg):
        """
        receives a Message instance
        """
        if self.msg_handler is not None:
            return self.msg_handler(msg)  # pylint: disable=E1102
        return self.default_msg_handler(msg)

    def default_msg_handler(self, msg):
        self.log('BaseCommand.default_msg_handler : %s' % (str(msg)))
        return False

    def end(self):
        self._ended = True
        self.log('BaseCommand.end %s' % (str(self._ended)))
        if self.callback is not None and callable(self.callback):
            self.log('BaseCommand.end : calling callback %s' % str(self.callback))
            self.callback(logger=self.log)
            self.log('BaseCommand.end : callback done')
        # request the end of the command connection
        return True
