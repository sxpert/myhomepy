# -*- coding: utf-8 -*-

import asyncio
import asyncio.events as events
import logging
import platform
import socket
from asyncio.streams import FlowControlMixin


class OWNProtocol(asyncio.Protocol):
    def __init__(self, reader, log=None, loop=None):
        self.log = log
        if self.log is None:
            self.log = self._log
        self._loop = loop
        if loop is None:
            self._loop = asyncio.get_event_loop()
        self.transport = None
        self._connected = False
        self._reader = reader

    def _log(self, msg):
        print(msg)

    @property
    def is_connected(self):
        return self._connected

    def setup_socket(self):
        sock = self.transport.get_extra_info('socket')
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        system = platform.system()
        if system == 'Linux':
            TCP_KEEPIDLE = getattr(socket, 'TCP_KEEPIDLE')
            sock.setsockopt(socket.SOL_TCP, TCP_KEEPIDLE, 1)
            TCP_KEEPINTVL = getattr(socket, 'TCP_KEEPINTVL')
            sock.setsockopt(socket.SOL_TCP, TCP_KEEPINTVL, 1)
            TCP_KEEPCNT = getattr(socket, 'TCP_KEEPCNT')
            sock.setsockopt(socket.SOL_TCP, TCP_KEEPCNT, 2)
        sock.settimeout(1)
        sock.setblocking(0)

    def connection_made(self, transport):
        self.transport = transport
        self.setup_socket()
        self._connected = True
        self._connection_lost = False

    def data_received(self, data):
        self._reader.feed_data(data)

    def connection_lost(self, exc):
        self.log('connection lost')
        self._connected = False
        self._connection_lost = True

    async def _drain_helper(self):
        # does nothing
        await asyncio.sleep(0, loop=self._loop)
