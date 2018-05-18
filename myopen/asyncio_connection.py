# -*- coding: utf-8 -*-

import asyncio
import re

from myopen.asyncio_socket import AsyncIOSock
from myopen.openpass import ownCalcPass
from core.logger import *

__all__ = [
    'MODE_COMMAND', 'MODE_MONITOR',
    'AsyncIOOWNConnection'
]

MODE_COMMAND = 0
MODE_MONITOR = 1


class AsyncIOOWNConnection(object):
    SOCKET_MODES = ('*99*0##', '*99*1##', )
    MODE_COLORS = (COLOR_LT_BLUE, COLOR_LT_GREEN)
    MODE_NAMES = ('CMD', 'MON', )

    ACK = '*#*1##'

    def __init__(self, host, port, passwd, queue, mode,
                 log=None, loop=None):
        self.host = host
        self.port = port
        self.passwd = passwd
        self.queue = queue
        self.mode = mode
        self.loop = loop
        self._run = False
        if self.loop is None:
            self.loop = asyncio.get_event_loop()
        self.is_ready = asyncio.Event(loop=self.loop)
        if log is None:
            hdr = '[%s:%d %s]' % \
                (self.host, self.port, self.MODE_NAMES[self.mode])
            self.log = \
                get_logger(header=hdr,
                           color=self.MODE_COLORS[self.mode])
        else:
            self.log = log

    async def run(self):
        self._run = True
        self.sock = AsyncIOSock(self.host, self.port, log=self.log)
        # start with the login procedure
        while self._run:
            if not self.sock.connected:
                self.log('not connected')
                self.is_ready.clear()
                self.msg_handler = self.state_start
                await self.sock.connect()
            else:
                self.log('connected, waiting for packet')
                try:
                    msg = await self.get_packet()
                except ConnectionAbortedError:
                    continue
                await self.msg_handler(msg)
        self.log('AsyncIOOWNConnection.run : %s the end' % (str(self)))

    def stop(self):
        self.log('stop requested')
        self.sock.stop()
        self._run = False

    async def get_packet(self):
        msg = await self.sock.get_packet()
        return msg

    async def send_packet(self, pkt):
        await self.sock.send_packet(pkt)

    async def state_start(self, msg):
        if msg == self.ACK:
            self.msg_handler = self.state_login
            cmd_msg = self.SOCKET_MODES[self.mode]
            await self.send_packet(cmd_msg)
        else:
            self.log('we didn\'t get ACK')

    async def state_login(self, msg):
        ops_m = re.match(r'\*#(\d+)##', msg)
        nonce = ops_m.groups()[0]
        passwd = ownCalcPass(self.passwd, nonce)
        passwd_msg = ('*#%s##' % (passwd))
        self.msg_handler = self.state_auth
        await self.send_packet(passwd_msg)

    async def state_auth(self, msg):
        if msg == self.ACK:
            self.is_ready.set()
            self.msg_handler = self.state_dispatch

    async def state_dispatch(self, msg):
        await self.queue.put((msg, self.mode, ))
