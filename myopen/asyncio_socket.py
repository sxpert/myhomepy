# -*- coding: utf-8 -*-

import asyncio
import asyncio.events as events
import platform
import socket
from asyncio.streams import (_DEFAULT_LIMIT, StreamReader,
                             StreamReaderProtocol, StreamWriter)

from core.logger import LOG_ERROR, LOG_INFO


class AsyncIOSock(object):
    def __init__(self, host, port, loop=None, log=None):
        self.host = host
        self.port = port
        self.loop = loop
        if self.loop is None:
            self.loop = asyncio.get_event_loop()
        self.log = log
        self.connected = False
        self.sock = None

    async def _sock_connect(self, sock):
        # catch socket.gaierror
        _had_msg = False
        while not self.connected:
            try:
                if not _had_msg:
                    self.log('attempt socket connection')
                await self.loop.sock_connect(sock, (self.host, self.port))
            except (socket.gaierror, socket.timeout):
                if not _had_msg:
                    _had_msg = True
                    self.log('unable to connect to %s:%d'
                             % (self.host, self.port))
                await asyncio.sleep(.5)
                continue
            self.log('connected to %s:%d'
                     % (self.host, self.port))
            self.connected = True

    async def _gen_sock(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
        await self._sock_connect(sock)
        self.log('should be connected')
        self.connected = True
        return sock

    def stop(self):
        if self.sock is not None:
            self.log('socket shutdown', LOG_INFO)
            try:
                self.sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            self.log('socket close', LOG_INFO)
            self.sock.close()

    async def readuntil(self, sep=b'##'):
        pos = 0
        done = False
        pkt = b''
        while not done:
            sep_at_pos = bytes(sep[pos:pos+1])
            try:
                b = await self.loop.sock_recv(self.sock, 1)
            except TimeoutError:
                self.log('timeout reading char')
                self.connected = False
                raise ConnectionAbortedError
            if b == sep_at_pos:
                pos += 1
                if pos >= len(sep):
                    done = True
            else:
                pos = 0
            pkt += b
        return pkt

    async def write(self, pkt):
        await self.loop.sock_sendall(self.sock, pkt)

    async def connect(self):
        self.sock = await self._gen_sock()

    async def get_packet(self):
        msg = await self.readuntil()
        msg = msg.decode(encoding='ascii')
        self.log('<= %s' % (msg))
        return msg

    async def send_packet(self, msg):
        self.log('=> %s' % (msg))
        msg = msg.encode(encoding='ascii')
        await self.write(msg)
